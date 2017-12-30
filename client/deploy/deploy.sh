# Get aws command lin
sudo apt-get install python-pip python-dev
sudo pip install -r $(pwd)/deploy/requirements.txt

# Run web pack and push the files to S3
npm run build
aws s3 sync dist s3://dev.acre.one
