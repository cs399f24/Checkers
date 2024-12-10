# Checkers Game Deployment

An online Checkers game that utilizes AWS resources for hosting and storage.

## Contributors

- **Jeffery Eisenhardt** - [eisenhardtj](https://github.com/eisenhardtj)
- **Trevor Gray** - [trevor-gray17](https://github.com/trevor-gray17)
- **Brandon Yang** - [CloudUki](https://github.com/CloudUki)
- **Nathaniel Hajel** - [nateh17](https://github.com/nateh17)

---

## Overview

This project is an online Checkers game built with Flask and Flask-SocketIO for real-time communication.

## Features

- Real-time game updates with Flask-SocketIO
- Option to start a new game or continue a game in progress
- Deployed with AWS Amplify
- Game State data stored in DynamoDB

## Deployment Instructions

### 1. Launch an EC2 Instance

1. **Log in to AWS**: Go to [AWS Management Console](https://aws.amazon.com) and sign in.
2. **Navigate to EC2**: Use the search bar to find and access the EC2 Dashboard.
3. **Launch a New Instance**:
   - Click "Launch Instance" and select **Amazon Linux 2 AMI**.
   - Choose `t2.micro` (free tier eligible) as the instance type.
4. **Configure Security Group**:
   - Allow **SSH** (Port 22) for remote access.
   - Allow **HTTP** (Port 80) for web traffic.
   - Add an inbound rule for **Port 8080** (used by the application server).
5. **Review and Launch**: Confirm settings, then launch. Download the key pair (.pem file) when prompted and store it securely.

### 2. Connect to Your EC2 Instance

1. **Open a Terminal** on your local machine.
2. Navigate to the directory where your key pair (.pem file) is saved.
3. Connect to your EC2 instance using SSH:
   ```sh
   ssh -i "your-key-pair.pem" ec2-user@your-ec2-public-dns

### 3. Change Bucket Name

1. After the instance is created, you want to edit the index.html and replace the s3 bucket names with the name of your bucket. 
    - `cd templates`
    - `nano index.html`
2. Then `sudo chmod +x deploy.sh` and then run the deploy script with `./deploy.sh`
