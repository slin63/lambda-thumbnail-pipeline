import os
import boto3

from json import loads, dumps
from helpers.progress import ProgressPercentage
from helpers import botoutils as bu
from helpers import images, logging


class C:
    UNPROCESSED = str(os.getenv("UNPROCESSED"))
    IMAGES = str(os.getenv("IMAGES"))
    TEMP = str(os.getenv("TEMP"))
    IMAGE_EXTENSIONS = ["jpg", "jpeg"]


logger = logging.get_logger("process_images_lambda")


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    s3r = boto3.resource("s3")

    processed = []
    # SQS triggers Lambda with event containing message payload and S3 records
    # Process messages by printing out body and optional author name
    for message in event["Records"]:
        records = loads(message["body"]).get("Records")
        if not records:
            raise Exception(
                f"No S3 records for this messageId {message['messageId']}"
            )

        # - Download original to tmp/album_name$file.ext
        #     and convert to thumbnail
        # - On thumbnail success, move original out
        #     of images/unprocessed/album_name into images/album_name/file.ext
        # - If image, upload thumbnail to images/album_name/image_thumb.jpg
        for s3record in records:
            bucket = s3record["s3"]["bucket"]["name"]
            s3_obj_key = s3record["s3"]["object"]["key"]
            if C.UNPROCESSED not in s3_obj_key:
                raise Exception(
                    f"Should only be receiving messages about unprocessed images, not: {s3_obj_key}"
                )

            if bu.process_file(
                s3, s3r, s3_obj_key, bucket, logger, C
            ):
                processed.append(s3_obj_key)

    return {
        "statusCode": 200,
        "body": dumps({"processed": processed}),
    }


# from helpers.mock_data import event as mock_event

# lambda_handler(mock_event, None)
