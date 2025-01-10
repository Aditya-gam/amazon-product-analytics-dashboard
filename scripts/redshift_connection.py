"""
redshift_connection.py

This script connects to the AWS Redshift cluster and provides a reusable function to run SQL queries.
It is designed for the "Amazon E-Commerce Product Analytics" project.

Usage:
    Import the `connect_to_redshift` and `run_query` functions to interact with the Redshift cluster.

Functions:
    - connect_to_redshift: Establishes a connection to the Redshift cluster.
    - run_query: Executes a given SQL query on the Redshift cluster.
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

REDSHIFT_HOST = os.getenv('REDSHIFT_HOST')
REDSHIFT_PORT = os.getenv('REDSHIFT_PORT')
REDSHIFT_DBNAME = os.getenv('REDSHIFT_DBNAME')
REDSHIFT_USER = os.getenv('REDSHIFT_USER')
REDSHIFT_PASSWORD = os.getenv('REDSHIFT_PASSWORD')


def connect_to_redshift():
    """
    Establishes a connection to the AWS Redshift cluster.

    Returns:
        conn (psycopg2.connection): Connection object to the Redshift cluster.
    """
    try:
        conn = psycopg2.connect(
            host=REDSHIFT_HOST,
            port=REDSHIFT_PORT,
            dbname=REDSHIFT_DBNAME,
            user=REDSHIFT_USER,
            password=REDSHIFT_PASSWORD
        )
        print("Connected to Redshift successfully.")
        return conn
    except Exception as e:
        print(f"Failed to connect to Redshift: {e}")
        raise


def run_query(query, params=None):
    """
    Executes a SQL query on the Redshift cluster.

    Args:
        query (str): The SQL query to execute.
        params (tuple, optional): Parameters to pass into the query. Defaults to None.

    Returns:
        list[dict]: Query result as a list of dictionaries (if applicable).
    """
    conn = None
    try:
        conn = connect_to_redshift()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if cur.description:  # If the query returns data
                result = cur.fetchall()
                return result
            else:
                conn.commit()
                return None
    except Exception as e:
        print(f"Error executing query: {e}")
        raise
    finally:
        if conn:
            conn.close()
            print("Connection closed.")
