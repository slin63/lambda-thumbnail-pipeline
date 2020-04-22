# lambda-thumbnail-pipeline

## Synchronizing entire directories with `awscli`
`aws s3 sync <directory> s3://<bucket_name>/images/unprocessed/`

## Preparing repository for lambda
from [here](https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/)
```
# Make temp directory
cp -R . ../temp/ && cd ../temp

# Add permissions
chmod -R 755 ./

# Build deployment package
rm ../thumbs-lambda.zip
zip -r ../thumbs-lambda.zip . -x '*.git*' -x 'env/*'

# Verify deployment package
unzip -l ../thumbs-lambda.zip

cd ../thumbs-lambda && rm -rf ../temp
```
Make sure to use the open-cv-headless layer from [Klayers](https://github.com/keithrozario/Klayers/blob/master/deployments/python3.7/arns/us-east-1.csv).
`arn:aws:lambda:us-east-1:113088814899:layer:Klayers-python37-opencv-python-headless:12`

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
- Reads files from an S3 bucket formatted: `images/unprocessed/<album_name>/file`
- Creates thumbnails for all files inside `/tmp/album_name$file`
    - `/tmp/` because it's the only writable directory in AWS Lambda
- Uploads thumbnails and original files to `images/<album_name>`

#### Running
1. `source env/bin/activate`
1. `source .env.default && python process_images_lambda.py`
