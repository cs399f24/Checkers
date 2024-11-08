#!/bin/bash

# Update and install necessary packages
sudo yum update -y
sudo yum install -y git awscli  # Install awscli for S3 interaction

# Specify the S3 bucket name
S3_BUCKET="checkers-game-cs399"

# Ensure the AWS CLI is configured
aws configure set default.region us-west-2  # Adjust region if needed
aws configure set default.output json

# Clone the repository into a temporary directory
TEMP_DIR="/tmp/Checkers"
git clone https://github.com/cs399f24/Checkers.git "$TEMP_DIR"

# Sync the cloned repository to the specified S3 bucket
aws s3 sync "$TEMP_DIR" s3://$S3_BUCKET/Checkers/

# Clean up the temporary directory
rm -rf "$TEMP_DIR"

# Create a virtual environment and install requirements
cd "$TEMP_DIR" || exit
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


# Source environment variables from .evn file
# if [-f .env]; then
#     export $(cat .env | xargs)
# fi

# Run the application
python app.py

