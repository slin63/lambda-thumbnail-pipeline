# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html

import boto3
import sys
import logging

from helpers.progress import ProgressPercentage
from helpers import botoutils as bu
from helpers import images
from pprint import pprint


formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler = logging.FileHandler("log.txt", mode="w")
handler.setFormatter(formatter)
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger("process_images")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(screen_handler)

logging = logger


class CONST:
    BUCKET = "knoppers.icu"
    UNPROCESSED = "images/unprocessed/"
    IMAGES = "images/"
    TEST_TXT = "requirements.txt"
    TEST_IMG = "1.jpg"
    IMAGE_EXTENSIONS = ["jpg", "jpeg"]
    TEMP = "tmp/"


logging.info(
    f"Checking for images in '{CONST.BUCKET}/{CONST.UNPROCESSED}'"
)

s3 = boto3.client("s3")
s3r = boto3.resource("s3")

# Grab unprocessed images, if any
# Filter out the base "directory".
to_process = s3.list_objects_v2(
    Bucket=CONST.BUCKET,
    Prefix=CONST.UNPROCESSED,
    MaxKeys=100,
)["Contents"]

# Remove files (image/description) not inside a parent album
# Expected format: images/raw/album_name/file.{jpg,jpeg}
to_process = list(
    filter(
        lambda x: len(x["Key"].split("/")) > 3, to_process
    )
)

# Track directory objects to clean up at the end.
directories = []

logging.info(
    f"{len(to_process)} objects found to process (including images, text, and directories)"
)

# - Download original to tmp/album_name$image.jpg and convert to thumbnail
# - On thumbnail success, move original out of images/raw/album_name into images/album_name/image.jpg
# - Upload thumbnail to images/album_name/image_thumb.jpg
for obj in to_process:
    is_directory = "." not in obj["Key"]
    # It's the actual directory. We'll clean this up at the end.
    if is_directory:
        directories.append(obj)
        continue

    album_name, filename, s3path = (
        *obj["Key"][len(CONST.UNPROCESSED) :].split("/"),
        obj["Key"],
    )
    filename_thumbs = f"{filename.split('.')[0]}_thumbs.{filename.split('.')[1]}"

    is_image = (
        obj["Key"].split(".")[1] in CONST.IMAGE_EXTENSIONS
    )

    # It's a description. Just move it to images/album_name
    if not is_image:
        out = f"{CONST.IMAGES}{album_name}/{filename}"
        bu.move_object(s3r, CONST.BUCKET, obj["Key"], out)
        logging.info(
            f"Moving non-image file {obj['Key']} to {out}"
        )
        continue

    logging.debug(
        f"Processing {s3path}. [is_image={is_image}] [is_directory={is_directory}]"
    )

    temp_file_name = CONST.TEMP + f"{album_name}${filename}"
    temp_file_thumbs_name = (
        CONST.TEMP + f"{album_name}${filename_thumbs}"
    )

    # Download file
    with open(temp_file_thumbs_name, "wb+") as f:
        s3.download_fileobj(
            CONST.BUCKET, s3path, f,
        )

        # Convert to thumbnail
        if not images.to_thumbnail(f):
            raise Exception(
                f"Thumbnail conversion failed for {f.name}!"
            )

        # Reset to top of file
        f.seek(0)

        # Upload thumbnail to images/album_name/image_thumb.jpg
        s3.upload_fileobj(
            f,
            CONST.BUCKET,
            f"{CONST.IMAGES}{album_name}/{filename_thumbs}",
            Callback=ProgressPercentage(CONST.TEST_TXT),
        )

        # Move original image to images/album_name/image.jpg, removing it from images/raw/
        bu.move_object(
            s3r,
            CONST.BUCKET,
            s3path,
            f"{CONST.IMAGES}{album_name}/{filename}",
        )

        logging.info(
            f"Successfully generated thumbnail and moved {s3path}."
        )

# Clear empty directories
for d in directories:
    s3r.Object(CONST.BUCKET, d["Key"]).delete()
    logging.info(f"Deleted directory: {d['Key']}")
