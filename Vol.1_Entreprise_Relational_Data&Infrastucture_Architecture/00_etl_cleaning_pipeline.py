# ==============================================================================
# 0. Importing Libraries needed:
# ==============================================================================
import pandas as pd
import numpy as np
import psycopg2
import sqlalchemy
import time

# ==============================================================================
# 1. Preparing data pipelines:
# ==============================================================================
path = "./instacartdata/" 

print("Loading data...🚀")
start_time = time.time()

# ==============================================================================
# 2. Reading the main files :
# Using dtype for Memory Optimization:
# ==============================================================================
products = pd.read_csv(path + "products.csv", dtype={'product_id': np.int32, 'aisle_id': np.int32, 'department_id': np.int32})
orders = pd.read_csv(path + "orders.csv", dtype={'order_id': np.int32, 'user_id': np.int32, 'order_number': np.int16, 'order_dow': np.int8, 'order_hour_of_day': np.int8})
order_products = pd.read_csv(path + "order_products__prior.csv", dtype={'order_id': np.int32, 'product_id': np.int32, 'add_to_cart_order': np.int16, 'reordered': np.int8})

print(f"Successfuly Downloaded ✅ {round(time.time() - start_time, 2)} ")

# ==============================================================================
# 3. Discovering the real data size:
# ==============================================================================
print("\n--- Data size ---")
print(f"Number of available products: {len(products):,}")
print(f"Number of orders: {len(orders):,}")
print(f"Number of selled products: {len(order_products):,}")

# ==============================================================================
# 4. Quick checking :
# ==============================================================================
print("\n--- Portion of row (orders) ---")
display(orders.head())

# ==============================================================================
# 5. Checking missing values:
# ==============================================================================
print(" --- Checking NULLs")
print("In Orders table:\n", orders.isnull().sum())
print("In Products table:\n", products.isnull().sum())

# ==============================================================================
# 6. Handling the missing values:
# ==============================================================================
orders['days_since_prior_order'] = orders['days_since_prior_order'].fillna(0).astype(np.float32)
print("\nThe row days_since_prior_order has cleaned successfully☑️.")

# ==============================================================================
# 7. Checking Duplicates:
# ==============================================================================
print("\n --- Checking Duplicates :")
print(f" The duplicated values value in Products: {products.duplicated().sum()} ")
print(f" The duplicated values value in Orders: {orders.duplicated().sum()} ")