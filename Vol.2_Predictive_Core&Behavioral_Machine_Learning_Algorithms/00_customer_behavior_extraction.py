# ==============================================================================
# 1. DATABASE CONNECTION & CUSTOMER BEHAVIOR EXTRACTION (FEATURE ENGINEERING)
# ==============================================================================
import pandas as pd
import sqlalchemy

print("\n--- [INITIATING] Database Connection for Feature Engineering ---")

# 1. Database connection parameters
db_user = 'postgres'
db_password = '8169'
db_host = 'localhost'
db_port = '5432'
db_name = 'instacart_db'

# Creating the database engine
connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = sqlalchemy.create_engine(connection_string)

print("[SUCCESS] Connected to PostgreSQL 'instacart_db' successfully.")

# 2. Writing the SQL Query to build the "Customer Profile"
# We are aggregating raw transactions into behavioral features for Machine Learning
sql_query = """
SELECT 
    user_id,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(days_since_prior_order)::numeric, 2) AS avg_days_between_orders,
    MODE() WITHIN GROUP (ORDER BY order_dow) AS favorite_shopping_day,
    MODE() WITHIN GROUP (ORDER BY order_hour_of_day) AS favorite_shopping_hour
FROM 
    fact_orders
GROUP BY 
    user_id
LIMIT 10;
"""

print("[*] Executing SQL Query to extract customer behavioral features...")

# 3. Executing the query and loading results into a Pandas DataFrame
customer_features_df = pd.read_sql(sql_query, engine)

print("[SUCCESS] Customer features extracted successfully!\n")
print("--- Customer Profiles Preview ---")
display(customer_features_df)
# ==============================================================================