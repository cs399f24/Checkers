# Checkers Game

An online Checkers game that utilizes AWS resources for hosting and storage.

## Contributors

- **Jeffery Eisenhardt** - [eisenhardtj](https://github.com/eisenhardtj)
- **Trevor Gray** - [trevor-gray17](https://github.com/trevor-gray17)
- **Brandon Yang** - [CloudUki](https://github.com/CloudUki)
- **Nathaniel Hajel** - [nateh17](https://github.com/nateh17)

---

## Overview

This project is an online Checkers game built with AWS API Gateway and Flask-SocketIO for real-time communication.

## Features

- Real-time game updates with Flask-SocketIO
- AWS API Gateway communicates to AWS Lambda to store game data in AWS DynamoDB.
- Option to start a new game or continue a game in progress
- Deployed with AWS Amplify
- Game State data stored in DynamoDB

## Deployment Instructions

### 1. Create Fork of Repo
1. Go to the GitHub repository.
2. Click on the "Fork" button in the top-right corner to create a fork of the repository in your GitHub account.

### 2. Using AWS Amplify, connect the repo from GitHub
1. Log in to the [AWS Management Console](https://aws.amazon.com/).
2. Navigate to the AWS Amplify service.
3. Click on "Get Started" under "Deploy".
4. Connect to your GitHub account and select the forked repository.
5. Follow the prompts to configure the build and deploy settings.

### 3. Create the API Gateway
1. Navigate to the [API Gateway service](https://aws.amazon.com/api-gateway/) in the AWS Management Console.
2. Click on "Create API" and choose "REST API".
3. Follow the prompts to create a new API.
4. Define the necessary resources and methods for your API.
5. Deploy the API to a stage.

### 4. Create the Database
1. Navigate to the [DynamoDB service](https://aws.amazon.com/dynamodb/) in the AWS Management Console.
2. Click on "Create table".
3. Define the table name and primary key (e.g., `GameID`).
4. Configure the table settings as needed and create the table.

### 5. Create the Lambda
1. Navigate to the [Lambda service](https://aws.amazon.com/lambda/) in the AWS Management Console.
2. Click on "Create function".
3. Choose "Author from scratch" and provide a function name.
4. Set the runtime to Python 3.x.
5. Configure the function's execution role and permissions.
6. Add the necessary code to handle game state updates and retrieval.
7. Set up triggers for the API Gateway.

### 6. Clone the Forked Repo
1. Open a terminal on your local machine.
2. Clone the forked repository:
   ```sh
   git clone https://github.com/your-username/Checkers.git
   cd Checkers

### 7. Change Any Nescessary Links
1. Go to "index.html".
2. Scroll down to line 79.
3. Copy and paste the API Gateway url from AWS.
4. Make sure the url is between the quotations.

### 8. Push the Changes to AWS Amplify
```sh
git add .
git commit -m "Update configuration links"
git push origin main