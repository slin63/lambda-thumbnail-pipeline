OUT="./thumbs-lambda.zip"
TEMP="../temp/"

cp -R . $TEMP

# Install dependencies to function project
pip install -r requirements.txt -t $TEMP

# Add permissions
chmod -R 755 $TEMP.

# Build deployment package
zip -r $OUT $TEMP. -x '*.git*' -x 'env/*'

# Verify deployment package
unzip -l $OUT

echo "Output lambda package to $OUT. Removing $TEMP"
rm -rf $TEMP
