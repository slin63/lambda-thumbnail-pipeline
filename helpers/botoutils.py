import os
import urllib.parse

from json import dumps
from helpers import images
from helpers.progress import ProgressPercentage
from botocore import exceptions


def move_object(s3, bucket, old, new):
    s3.Object(bucket, new).copy_from(
        CopySource=f"{bucket}/{old}"
    )
    s3.Object(bucket, old).delete()


def process_file(
    s3, s3r, s3_obj_key, bucket, logger, CONST
):
    is_directory = "." not in s3_obj_key
    in_album = len(s3_obj_key.split("/")) > 2
    s3_obj_key = urllib.parse.unquote_plus(s3_obj_key)

    # It's the actual directory OR it's outside of an album.
    # We don't need to do anything.
    if is_directory or not in_album:
        logger.info(
            f"{s3_obj_key} was a directory or not in an album. Skipping"
        )
        return True

    split_key = s3_obj_key[len(CONST.UNPROCESSED) :].split(
        "/"
    )
    if len(split_key) > 2:
        logger.info(
            f"{s3_obj_key} was a nested directory. Deleting."
        )
        try:
            obj = s3r.Object(bucket, s3_obj_key)
            obj.delete()
        except exceptions.ClientError as exc:
            if exc.response["Error"]["Code"] == "NoSuchKey":
                logger.info(
                    f"{s3path} not found. Message might be stale. Skipping"
                )
                return True

    album_name, filename, s3path = (*split_key, s3_obj_key)
    filename_thumbs = f"{filename.split('.')[0]}_thumbs.{filename.split('.')[1]}"

    is_image = (
        s3_obj_key.split(".")[1] in CONST.IMAGE_EXTENSIONS
    )

    # It's a description. Just move it to images/album_name
    if not is_image:
        out = f"{CONST.IMAGES}{album_name}/{filename}"

        try:
            if filename[0] != ".":
                move_object(s3r, bucket, s3_obj_key, out)
            else:
                logger.debug(f"Deleting dot file: {filename}")
                s3r.Object(bucket, s3_obj_key).delete()
        except exceptions.ClientError as exc:
            if exc.response["Error"]["Code"] == "NoSuchKey":
                logger.info(
                    f"{s3path} not found. Message might be stale. Skipping"
                )
                return True
        logger.info(
            f"Moving non-image file {filename} to {out}"
        )
        return True

    logger.debug(
        f"Processing {s3path}. [is_image={is_image}] [is_directory={is_directory}]"
    )

    temp_file_name = CONST.TEMP + f"{album_name}${filename}"
    temp_file_thumbs_name = (
        CONST.TEMP + f"{album_name}${filename_thumbs}"
    )

    # Download file
    with open(temp_file_thumbs_name, "wb+") as f:
        try:
            s3.download_fileobj(
                bucket, s3path, f,
            )
        except exceptions.ClientError as exc:
            if exc.response["Error"]["Code"] == "404":
                logger.info(
                    f"{s3path} not found. Message might be stale. Skipping"
                )
                return True

        # Convert to thumbnail
        if not images.to_thumbnail(
            temp_file_thumbs_name, CONST.THUMB_SIZE
        ):
            raise Exception(
                f"Thumbnail conversion failed for {f.name}!"
            )

        # Reset to top of file
        f.seek(0)

        # Upload thumbnail to images/album_name/image_thumb.jpg
        s3.upload_fileobj(
            f,
            bucket,
            f"{CONST.IMAGES}{album_name}/{filename_thumbs}",
            Callback=ProgressPercentage(f.name),
        )

        # Move original image to images/album_name/image.jpg, removing it from images/raw/
        move_object(
            s3r,
            bucket,
            s3path,
            f"{CONST.IMAGES}{album_name}/{filename}",
        )

        logger.info(
            f"Successfully generated thumbnail and moved {s3path}."
        )

    return True
