#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    source .env
else
    echo ".env file not found. Please create one with the VPC_ID variable."
    exit 1
fi

# Check if VPC_ID is set
if [ -z "$VPC_ID" ]; then
    echo "VPC_ID is not set in the .env file. Please add it and try again."
    exit 1
fi

# Variables
SECURITY_GROUP_NAME="Checkers"
DESCRIPTION="Security group for Checkers application"

# Create the security group
SECURITY_GROUP_ID=$(aws ec2 create-security-group \
    --group-name $SECURITY_GROUP_NAME \
    --description "$DESCRIPTION" \
    --vpc-id $VPC_ID \
    --query 'GroupId' \
    --output text)

echo "Created security group with ID: $SECURITY_GROUP_ID"

# Allow SSH (Port 22)
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

echo "SSH (Port 22) rule added."

# Allow HTTP (Port 80)
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

echo "HTTP (Port 80) rule added."

# Allow application server traffic (Port 8080)
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 8080 \
    --cidr 0.0.0.0/0

echo "Application server (Port 8080) rule added."


# Save the security group ID to a file

# Allows execution permissions for the redeploy.sh

redeploy="redeploy.sh"
chmod +x $redeploy
