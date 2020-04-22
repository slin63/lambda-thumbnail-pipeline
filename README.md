# lambda-thumbnail-pipeline

## process_images.py
- Reads files from an S3 bucket formatted: `images/unprocessed/<album_name>/files`
- Creates thumbnails for all files inside `album_name`
- Adds thumbnails and original files to `images/<album_name>`

#### Running
1. `source env/bin/activate`
1. `source .env && python process_images.py`
