import pymysql
import requests
import os

connect = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

cr = connect.cursor()
cr.execute("TRUNCATE TABLE orders")
cr.execute("TRUNCATE TABLE products")
cr.execute("TRUNCATE TABLE customers")

session = requests.session()

print("Session Opened Successfully")

def isnull(value):
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    return value

#================================================================================#
#======================= Let's login with our information =======================#
#================================================================================#

base_url = "https://switch-it1.odoo.com/web" 
end_point = "/session/authenticate"

auth_url = base_url + end_point
db = os.getenv("ODOO_DB")
login = os.getenv("ODOO_LOGIN")
password = os.getenv("ODOO_PASSWORD")

headers = {
    "User-Agent": "Mozilla Fire Fox 10.0 (Windows 10; x64; 64bit)",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

auth_params = {
    "db": db,
    "login": login,
    "password": password
}

request_params = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": auth_params,
    "id": 1
}

auth_response = session.post(url=auth_url, headers=headers, json=request_params)

print("Authentication Done Successfully")

#============================================================================================#
#======================= Let's retrieve the data from table Customers =======================#
#============================================================================================#

data_url = base_url + "/dataset/call_kw"

customers_params = {
    "model": "res.partner",
    "method": "search_read",
    "args": [],
    "kwargs": {
        "fields": [],
        "limit": 1000000,
        "offset": 0,
    }
}

customers_request_params = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": customers_params,
    "id": 1,
}

call_respone = session.post(url=data_url, headers=headers, json=customers_request_params)
customers_json_dict = call_respone.json()

customers_records = []
customers = customers_json_dict["result"]
for customer in customers:
    id = isnull(customer["id"])
    full_name = isnull(customer["name"])
    if full_name:
        full_name_list = full_name.split(sep=" ")
        first_name = full_name_list[0]
        last_name = full_name_list[1] if len(full_name_list) == 2 else None
    else:
        first_name, last_name = None, None
    email = isnull(customer["email"])
    phone = isnull(customer["phone"])
    country = isnull(customer["country_id"][1]) if customer["country_id"] else None
    city = isnull(customer["city"])
    street = isnull(customer["street"])
    street2 = isnull(customer["street2"])
    zip_code = isnull(customer["zip"])
    customer_record = (id, first_name, last_name, email, phone, country, city, street, street2, zip_code)
    customers_records.append(customer_record)

cr.executemany("""
INSERT INTO customers (id, first_name, last_name, email, phone, country, city, street, street2, zip_code)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", customers_records)

connect.commit()

print("Customers sent to Database Successfully")

#=========================================================================================#
#======================= Let's retrieve the data from table Orders =======================#
#=========================================================================================#

base_url = "https://switch-it1.odoo.com/web"
data_end_point = "/dataset/call_kw"
data_url = base_url + data_end_point

orders_params = {
    "model": "sale.order",
    "method": "search_read",
    "args": [],
    "kwargs": {
        "fields": [],
        "limit": 100000,
        "offset": 0,
    } 
}

orders_request_params = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": orders_params,
    "id": 2,
}

order_response = session.post(url=data_url, headers=headers, json=orders_request_params)
orders_json_dict = order_response.json()

orders_records = []
orders = orders_json_dict["result"]
for order in orders:
    id = isnull(order["id"])
    customer_id = isnull(order["partner_id"][0]) if order["partner_id"] else None
    order_date = isnull(order["date_order"])
    order_status = isnull(order["state"])
    sales = isnull(order["amount_total"])
    delivery_company_id = isnull(order["carrier_id"])
    delivery_status = isnull(order["delivery_status"])
    delivery_sales = isnull(order["amount_delivery"])
    order_record = (id, customer_id, order_date, order_status, sales,
                    delivery_company_id, delivery_status, delivery_sales)
    orders_records.append(order_record)
    
insert_records_into_orders = """
INSERT INTO orders (id, customer_id, order_date, order_status, sales,
                    delivery_company_id, delivery_status, delivery_sales)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

cr.executemany(insert_records_into_orders, orders_records)

connect.commit()

print("Orders sent to Database Successfully")

#===========================================================================================#
#======================= Let's retrieve the data from table Products =======================#
#===========================================================================================#

products_params = {
    "model": "product.template",
    "method": "search_read",
    "args": [],
    "kwargs": {
        "fields": [],
        "limit": 100000,
        "offset": 0,
    }
}

products_request_params = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": products_params,
    "id": 2,
}

products_response = session.post(url=data_url, headers=headers, json=products_request_params)
products_json_dict = products_response.json()

products_records = []
products = products_json_dict["result"]
for product in products:
    id = product["id"]
    name = product["display_name"]
    product_record = (id, name)
    products_records.append(product_record)

cr.executemany("""INSERT INTO products (id, name) VALUES (%s, %s)""", products_records)

connect.commit()

print("Products sent to Database Successfully")

#===========================================================================================#
#===========================================================================================#
#===========================================================================================#

connect.close()

session.close()

print("Session Closed Successfully")