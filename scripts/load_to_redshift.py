# load_to_redshift.py

"""
This script uploads a cleaned dataset to an S3 bucket and loads it into an AWS Redshift cluster.
"""

import boto3
import pandas as pd
import os
import sys
from redshift_connection import run_query
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS and Redshift credentials
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = 'amazon-product-analytics-dashboard'
REDSHIFT_TABLE = 'amazon_products'

# Local and S3 paths
LOCAL_FILE_PATH = "data/processed/cleaned_amazon_products.csv"
S3_FILE_PATH = "uploads/processed/cleaned_amazon_products.csv"

# Function to upload file to S3


def upload_to_s3(local_path, bucket_name, s3_path):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    try:
        s3_client.upload_file(local_path, bucket_name, s3_path)
        print(f"File uploaded to S3: {bucket_name}/{s3_path}")
    except Exception as e:
        print(f"Failed to upload to S3: {e}")
        raise

# SQL to create Redshift table


def create_table():
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {REDSHIFT_TABLE} (
        Unnamed_0 FLOAT,
        name VARCHAR(500),
        main_category VARCHAR(100),
        sub_category VARCHAR(100),
        image VARCHAR(500),
        link VARCHAR(500),
        ratings FLOAT,
        no_of_ratings FLOAT,
        discount_price FLOAT,
        actual_price FLOAT,
        discount_percentage FLOAT,
        price_difference FLOAT,
        discount_category VARCHAR(50),
        rating_category VARCHAR(50)
    );
    """
    run_query(create_table_query)

# SQL to load data from S3 to Redshift


def load_data_to_redshift():
    copy_query = f"""
    COPY {REDSHIFT_TABLE}
    FROM 's3://{S3_BUCKET_NAME}/{S3_FILE_PATH}'
    IAM_ROLE 'arn:aws:iam::851725401997:role/service-role/AmazonRedshift-CommandsAccessRole-20250110T231821'
    FORMAT AS CSV
    DELIMITER ','
    IGNOREHEADER 1;
    """
    run_query(copy_query)

# Data integrity checks


def data_integrity_checks():
    checks = [
        "SELECT COUNT(*) FROM amazon_products;",
        "SELECT COUNT(DISTINCT link) FROM amazon_products;",
        "SELECT COUNT(*) FROM amazon_products WHERE ratings IS NULL;",
        "SELECT COUNT(*) FROM amazon_products WHERE discount_price > actual_price;",
    ]
    for check in checks:
        result = run_query(check)
        print(result)


if __name__ == "__main__":
    try:
        # Upload cleaned data to S3
        upload_to_s3(LOCAL_FILE_PATH, S3_BUCKET_NAME, S3_FILE_PATH)

        # Create the Redshift table
        create_table()

        # Load data from S3 to Redshift
        load_data_to_redshift()

        # Perform data integrity checks
        data_integrity_checks()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
