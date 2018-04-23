# Include all libraries first
cd venv/lib/python3.6/site-packages
zip -r9 ../../../../package.zip *

# Include lambda code
cd ../../../..
zip -g package.zip *.py

# Deploy
aws events put-rule --name acre-daily-update --schedule-expression "cron(01 22 * * ? *)" --region us-east-2
aws events put-rule --name acre-daily-clean --schedule-expression "cron(01 00 * * ? *)" --region us-east-2
aws lambda update-function-code --function-name Acre-Daily --zip-file fileb://package.zip --region us-east-2
