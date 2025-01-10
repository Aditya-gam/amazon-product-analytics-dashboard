"""
s3_upload.py

This script uploads files to an AWS S3 bucket via CLI arguments. 
It is designed for the "Amazon E-Commerce Product Analytics" project.

Usage:
    Run the script from the terminal as:
        python s3_upload.py <file_path> [<object_name>]

Example:
    python s3_upload.py data/example.csv uploads/example.csv
"""

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Use the credentials in the boto3 client
s3_client_conf = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)


def upload_file_to_s3(file_name, bucket_name, object_name=None):
    """
    Uploads a file to an S3 bucket.

    Args:
        file_name (str): The path to the file to upload.
        bucket_name (str): The name of the S3 bucket.
        object_name (str, optional): The S3 object name. Defaults to the file_name.

    Returns:
        bool: True if the file was uploaded successfully, False otherwise.
    """
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        s3_client = s3_client_conf
    except (NoCredentialsError, PartialCredentialsError):
        print("AWS credentials not found. Please configure your AWS CLI or provide them securely.")
        return False

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(
            f"File '{file_name}' successfully uploaded to '{bucket_name}/{object_name}'.")
        return True
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


if __name__ == "__main__":
    # Ensure the correct number of arguments
    if len(sys.argv) < 2:
        print(
            "Usage: python s3_upload.py <file_path> [<object_name>]")
        sys.exit(1)

    file_path = sys.argv[1]
    bucket_name = "amazon-product-analytics-dashboard"
    object_name = sys.argv[2] if len(sys.argv) > 2 else None

    # Upload the file
    success = upload_file_to_s3(file_path, bucket_name, object_name)
    if success:
        print("Upload completed successfully.")
    else:
        print("Upload failed.")
