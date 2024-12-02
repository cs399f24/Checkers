import os
import boto3
from botocore.exceptions import NoCredentialsError
from git import Repo

# Initialize the S3 client
s3 = boto3.client('s3')

# S3 bucket name
S3_BUCKET_NAME = 'your-s3-bucket-name'

def delete_s3_files(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for item in response['Contents']:
                s3.delete_object(Bucket=bucket_name, Key=item['Key'])
                print(f"Deleted {item['Key']} from {bucket_name}.")
    except NoCredentialsError:
        print("AWS credentials not available.")
    except Exception as e:
        print(f"Error deleting files from S3: {e}")

def clone_or_pull_repo(repo_url, repo_path):
    # Clones the repository if it doesn't exist, or pulls the latest changes if it does
    if os.path.exists(repo_path):
        print(f"Repository already exists at {repo_path}. Pulling latest changes...")
        repo = Repo(repo_path)
        repo.remotes.origin.pull()
    else:
        print(f"Cloning repository from {repo_url} to {repo_path}...")
        Repo.clone_from(repo_url, repo_path)

def upload_files_to_s3(bucket_name, source_dir):
    # Uploads the files to the s3 bucket
    for root, _, files in os.walk(source_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, source_dir)
            s3_path = relative_path.replace("\\", "/")  # Ensure S3 uses forward slashes
            try:
                s3.upload_file(local_path, bucket_name, s3_path)
                print(f"Uploaded {local_path} to s3://{bucket_name}/{s3_path}.")
            except Exception as e:
                print(f"Error uploading {local_path} to S3: {e}")

def main():
    repo_url = 'https://github.com/cs399f24/checkers'
    repo_path = '~/checkers'
    static_folder_path = os.path.join(repo_path, 'static')

    clone_or_pull_repo(repo_url, repo_path)

    delete_s3_files(S3_BUCKET_NAME)

    upload_files_to_s3(S3_BUCKET_NAME, static_folder_path)

if __name__ == '__main__':
    main()