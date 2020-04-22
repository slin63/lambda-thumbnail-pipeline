# lambda-thumbnail-pipeline

## Synchronizing entire directories with `awscli`
`aws s3 sync <directory> s3://<bucket_name>/images/unprocessed/`

## Configuring .env
```
# Prefix of files in folders to be processed
# e.g. images/unprocessed/album_name/image.jpg
export UNPROCESSED=images/unprocessed/

# Folder where you want processed files to be moved to
export IMAGES=images/

# Temp dir for lambda to process images
export TEMP=tmp/
```

## process_images.py
- Reads files from an S3 bucket formatted: `images/unprocessed/<album_name>/files`
- Creates thumbnails for all files inside `album_name`
- Adds thumbnails and original files to `images/<album_name>`

#### Running
1. `source env/bin/activate`
1. `source .env && python process_images_lambda.py`
