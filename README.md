# lambda-thumbnail-pipeline

## Synchronizing entire directories with `awscli`
`aws s3 sync <directory> s3://<bucket_name>/images/unprocessed/`

## Preparing repository for lambda
from [here](https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/)
1. Install dependencies to function project
    - `pip install -r requirements.txt -t ./`
1. Add permissions
    - `chmod -R 755 .`
1. Build deployment package
    - `zip -r ../thumbs-lambda.zip .`
1. Verify deployment package
    - `unzip -l ../thumbs-lambda.zip`

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
