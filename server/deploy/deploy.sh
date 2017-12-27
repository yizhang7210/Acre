bash $(pwd)/deploy/setup-eb.sh
echo n | eb init Acre --region us-east-2 # n is for not use code commit
eb deploy acre-dev-worker
