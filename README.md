# Switch IT Odoo Data ETL Pipeline

## Overview
This project is a **Python-based ETL pipeline** that extracts, transforms, and loads (ETL) data from a Switch IT Odoo instance into a **MySQL cloud database**. It allows you to automate the retrieval of Customers, Orders, and Products data, clean it, and store it in a structured way for further analysis or reporting.

By using this pipeline, you can:
- Automatically sync Odoo data with your database.
- Handle your datasets without losing data consistency.
- Clean and transform data before loading it into the database.
- Keep your database up-to-date with the latest Odoo records.

---

## Features
- Connects to **Odoo API** using `requests` with JSON-RPC.
- Extracts data from:
  - `res.partner` (Customers)
  - `sale.order` (Orders)
  - `product.template` (Products)
- Cleans and processes the data:
  - Handles null values and empty strings.
  - Splits full names into first and last names.
- Loads data into **MySQL cloud database** using `pymysql`.
- Maintains **data consistency** by truncating tables before each run.
- Fully automated: run the script to refresh all tables with the latest data.

---

## Requirements
- Python 3.10+
- `pymysql`
- `requests`

You can install dependencies with:

```bash
pip install pymysql requests
```

## Environment Variables

To keep sensitive information safe, all credentials are stored in a `.env` file at the root of the project. This file should **never** be pushed to GitHub.

### Example `.env`:
- MySQL Database
  - DB_HOST=your_mysql_host
  - DB_PORT=your_mysql_port (Default=3306)
  - DB_USER=your_db_user
  - DB_PASSWORD=your_db_password
  - DB_NAME=your_db_name

- Odoo API
  - ODOO_DB=your_odoo_db
  - ODOO_LOGIN=your_odoo_email
  - ODOO_PASSWORD=your_odoo_password