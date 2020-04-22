# lambda-thumbnail-pipeline

## process_images.py
- Reads files from an S3 bucket formatted: `images/unprocessed/<album_name>/files`
- Creates thumbnails for all files inside `album_name` and moves them to `images/<album_name>`

