# clean_data.py

# Script for Cleaning Amazon Product Dataset

import pandas as pd
import numpy as np
import os
import sys

# Function to validate the input file


def validate_input_file(file_path):
    if not file_path.endswith('.csv'):
        raise ValueError("Input file must be a CSV file.")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

# Function to clean ratings and no_of_ratings columns


def handle_ratings(row):
    try:
        row['ratings'] = float(row['ratings']) if not pd.isnull(
            row['ratings']) else 0.0
    except (ValueError, TypeError):
        row['ratings'] = 0.0

    try:
        row['no_of_ratings'] = int(row['no_of_ratings'].replace(
            ',', '')) if not pd.isnull(row['no_of_ratings']) else 0
    except (ValueError, TypeError, AttributeError):
        row['no_of_ratings'] = 0

    if pd.isnull(row['ratings']) or pd.isnull(row['no_of_ratings']):
        row['ratings'] = 0.0
        row['no_of_ratings'] = 0

    return row

# Function to clean price columns


def clean_price_column(price):
    if isinstance(price, str):
        return float(price.replace('₹', '').replace(',', '').strip())
    elif pd.isnull(price):
        return np.nan
    else:
        return float(price)

# Function to handle missing prices


def handle_prices(row):
    if pd.isnull(row['discount_price']) and pd.isnull(row['actual_price']):
        return None
    elif pd.isnull(row['discount_price']):
        row['discount_price'] = row['actual_price']
    elif pd.isnull(row['actual_price']):
        row['actual_price'] = row['discount_price']

    if row['discount_price'] > row['actual_price']:
        row['discount_price'], row['actual_price'] = row['actual_price'], row['discount_price']

    if row['actual_price'] == 0:
        row['discount_price'], row['actual_price'] = 0.0001, 0.0001

    return row

# Function to categorize discounts


def categorize_discount(discount):
    if discount >= 50:
        return 'High Discount'
    elif discount >= 20:
        return 'Medium Discount'
    else:
        return 'Low Discount'

# Function to classify ratings


def classify_rating(rating):
    if rating >= 4.0:
        return 'Highly Rated'
    elif rating >= 2.5:
        return 'Moderately Rated'
    else:
        return 'Low Rated'

# Function to clean and process the dataset


def clean_data(file_path):
    validate_input_file(file_path)

    # Load the dataset
    df = pd.read_csv(file_path)

    # Handle ratings and no_of_ratings
    df = df.apply(handle_ratings, axis=1)
    df['ratings'] = df['ratings'].astype(float)
    df['no_of_ratings'] = df['no_of_ratings'].astype(int)

    # Clean and handle price columns
    df['discount_price'] = df['discount_price'].apply(clean_price_column)
    df['actual_price'] = df['actual_price'].apply(clean_price_column)
    df = df.apply(handle_prices, axis=1)
    df.dropna(subset=['discount_price', 'actual_price'], inplace=True)
    df['discount_price'] = df['discount_price'].astype(float)
    df['actual_price'] = df['actual_price'].astype(float)

    # Remove duplicates
    df = df.drop_duplicates()

    # Create new features
    df['discount_percentage'] = (
        (df['actual_price'] - df['discount_price']) / df['actual_price']) * 100
    df['price_difference'] = df['actual_price'] - df['discount_price']
    df['discount_category'] = df['discount_percentage'].apply(
        categorize_discount)

    # Clean text columns
    df['name'] = df['name'].str.lower().str.strip()
    df['main_category'] = df['main_category'].str.lower().str.strip()
    df['sub_category'] = df['sub_category'].str.lower().str.strip()

    # Classify ratings
    df['rating_category'] = df['ratings'].apply(classify_rating)

    # Save the cleaned data
    processed_data_path = "./data/processed/cleaned_amazon_products.csv"
    df.to_csv(processed_data_path, index=False)
    print(f"Cleaned data saved to {processed_data_path}")


# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_data.py <file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    try:
        clean_data(input_file_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
