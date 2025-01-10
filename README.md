# **Amazon E-Commerce Product Analytics & Dashboard**

## **Overview**

This project aims to build an end-to-end data analytics pipeline for analyzing Amazon e-commerce product data. The project involves collecting data from various categories, storing it in AWS S3, cleaning and transforming it, and analyzing it with AWS Redshift. Finally, Tableau will create interactive dashboards to visualize insights like product distribution, discount patterns, ratings, and top-rated products.

### **Goals of the Project**
- Identify product categories with the highest/lowest discounts.
- Analyze how ratings and discounts vary across categories.
- Determine the top-rated and best-selling products.
- Build a production-ready data pipeline using cloud tools and best practices.

---

## **Tools & Technologies**
- **Python**: For data cleaning, transformation, and analysis.
- **AWS S3**: Cloud storage for raw and processed data.
- **AWS Redshift**: Data warehousing for efficient querying.
- **boto3**: Python library to interact with AWS services.
- **psycopg2**: PostgreSQL library for Redshift connection.
- **Tableau**: For building interactive dashboards.
- **GitHub**: For version control and project management.
- **VS Code**: Primary IDE for coding and debugging.

---

## **Table of Contents**

- [**Amazon E-Commerce Product Analytics \& Dashboard**](#amazon-e-commerce-product-analytics--dashboard)
  - [**Overview**](#overview)
    - [**Goals of the Project**](#goals-of-the-project)
  - [**Tools \& Technologies**](#tools--technologies)
  - [**Table of Contents**](#table-of-contents)
  - [**Results \& Visualizations**](#results--visualizations)
  - [**Project Directory Structure**](#project-directory-structure)
  - [**Setup Instructions**](#setup-instructions)
    - [**Prerequisites**](#prerequisites)
    - [**Installing Dependencies**](#installing-dependencies)
    - [**Setting Up AWS S3**](#setting-up-aws-s3)
    - [**Connecting to AWS Redshift**](#connecting-to-aws-redshift)
    - [**Sample .env File**](#sample-env-file)
  - [**Usage**](#usage)
    - [**Run the Data Pipeline**](#run-the-data-pipeline)
    - [**Build Dashboards in Tableau**](#build-dashboards-in-tableau)
  - [**Contributing**](#contributing)
  - [**License**](#license)

---

## **Results & Visualizations**

> Placeholder for results, screenshots, and insights derived from the analysis.

- **Key Insights:** (e.g., “Electronics has the highest discounts.”)  
- **Tableau Dashboards:** (Add screenshots or links to Tableau Public dashboards.)  
- **Correlations & Trends:** (Summarize key findings.)  

---

## **Project Directory Structure**

```plaintext
amazon-product-analytics-dashboard/
│
├── data/                  # Store raw and processed data
│   ├── raw/               # Raw CSVs uploaded to S3
│   └── processed/         # Cleaned and transformed data
│
├── scripts/               # Python scripts for data processing and analysis
│   ├── s3_upload.py       # Script to upload files to S3
│   └── redshift_connection.py  # Script to connect and query Redshift
│
├── notebooks/             # Jupyter Notebooks for EDA and visualization
│
├── dashboards/            # Tableau dashboards or exported files
│
├── README.md              # Project documentation
│
└── requirements.txt       # Python dependencies
```

---

## **Setup Instructions**

### **Prerequisites**

Ensure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [Tableau Desktop](https://www.tableau.com/products/desktop)
- [Git](https://git-scm.com/)
- AWS account with access to S3 and Redshift.

---

### **Installing Dependencies**

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/amazon-product-analytics-dashboard.git
   cd amazon-product-analytics-dashboard
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

### **Setting Up AWS S3**

1. Create an S3 bucket (if not already created):
   ```bash
   aws s3 mb s3://amazon-product-analytics
   ```

2. Configure the bucket permissions using the [AWS Management Console](https://aws.amazon.com/console/).

3. Upload raw data:
   ```bash
   python scripts/s3_upload.py data/raw/example.csv amazon-product-analytics
   ```

---

### **Connecting to AWS Redshift**

1. Ensure the Redshift cluster is created and available.
2. Use the following connection details in `redshift_connection.py`:
   - **Host**: `analytics-cluster.cblhjtrhob5d.us-east-1.redshift.amazonaws.com`
   - **Port**: `5439`
   - **Database**: `dev`
   - **Username** and **Password**: Configure in environment variables or `.env` file.
3. Test the connection by running:
   ```bash
   python scripts/redshift_connection.py
   ```

---

### **Sample .env File**

Create a `.env` file in the project root to securely store sensitive information. Below is a sample structure:

```plaintext
# AWS credentials
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key

# AWS Redshift credentials
REDSHIFT_HOST=your_redshift_host
REDSHIFT_PORT=5439
REDSHIFT_DBNAME=dev
REDSHIFT_USER=your_redshift_username
REDSHIFT_PASSWORD=your_redshift_password
```

**Note:** Never upload the `.env` file to GitHub. Add it to your `.gitignore` file.

---

## **Usage**

### **Run the Data Pipeline**

1. Upload data to S3:
   ```bash
   python scripts/s3_upload.py data/raw/example.csv amazon-product-analytics
   ```

2. Run SQL queries on Redshift:
   ```python
   from scripts.redshift_connection import run_query

   query = "SELECT * FROM products;"
   result = run_query(query)
   print(result)
   ```

### **Build Dashboards in Tableau**

- Connect Tableau to the Redshift cluster.
- Load processed data and create visualizations.

---

## **Contributing**

Contributions are welcome!  
To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of changes.

---

## **License**

This project is licensed under the [MIT License](LICENSE).