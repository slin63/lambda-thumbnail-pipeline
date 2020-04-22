def move_object(s3, bucket, old, new):
    s3.Object(bucket, new).copy_from(
        CopySource=f"{bucket}/{old}"
    )
    s3.Object(bucket, old).delete()
