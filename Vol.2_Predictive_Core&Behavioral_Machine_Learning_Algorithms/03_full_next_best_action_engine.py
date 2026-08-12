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

# ==============================================================================
# 2. MARKET BASKET ANALYSIS: PRODUCT CO-OCCURRENCE (CROSS-SELLING)
# ==============================================================================
print("\n--- [INITIATING] Market Basket Analysis (Product Pairs) ---")

# Writing an advanced SQL Query using CTEs (Common Table Expressions) and Self-Joins
# We sample 50,000 orders to optimize performance and prevent memory overload
mba_query = """
WITH sample_orders AS (
    SELECT order_id FROM fact_orders LIMIT 50000
),
basket AS (
    SELECT op.order_id, p.product_name
    FROM fact_order_products op
    JOIN dim_products p ON op.product_id = p.product_id
    WHERE op.order_id IN (SELECT order_id FROM sample_orders)
)
SELECT 
    b1.product_name AS product_a, 
    b2.product_name AS product_b, 
    COUNT(*) AS times_bought_together
FROM basket b1
JOIN basket b2 
    ON b1.order_id = b2.order_id 
    AND b1.product_name < b2.product_name
GROUP BY b1.product_name, b2.product_name
ORDER BY times_bought_together DESC
LIMIT 10;
"""

print("[*] Executing Advanced SQL for Pattern Discovery...")
product_pairs_df = pd.read_sql(mba_query, engine)

print("[SUCCESS] Cross-Selling pairs extracted successfully!\n")
print("--- Top 10 Products Bought Together ---")
display(product_pairs_df)
# ==============================================================================

# ==============================================================================
# 3. THE NEXT-BEST-ACTION (NBA) ENGINE: PERSONALIZED RECOMMENDATION FUNCTION
# ==============================================================================

def generate_next_best_action(user_id, db_engine):
    print(f"\n--- [INITIATING] AI Recommendation Engine for User ID: {user_id} ---")
    
    # Writing a highly optimized SQL query to extract personalization metrics
    # We combine user purchasing cycles (when) with product loyalty (what)
    nba_query = f"""
    WITH UserStats AS (
        SELECT 
            ROUND(AVG(days_since_prior_order)::numeric, 0) AS days_to_next_purchase,
            MODE() WITHIN GROUP (ORDER BY order_hour_of_day) AS optimal_contact_hour
        FROM fact_orders
        WHERE user_id = {user_id}
    ),
    TopProduct AS (
        SELECT p.product_name AS anchor_product, COUNT(*) as loyalty_score
        FROM fact_order_products op
        JOIN fact_orders o ON op.order_id = o.order_id
        JOIN dim_products p ON op.product_id = p.product_id
        WHERE o.user_id = {user_id}
        GROUP BY p.product_name
        ORDER BY loyalty_score DESC
        LIMIT 1
    )
    SELECT 
        u.days_to_next_purchase,
        u.optimal_contact_hour,
        t.anchor_product
    FROM UserStats u CROSS JOIN TopProduct t;
    """
    
    print("[*] Analyzing historical transaction data...")
    # Executing the query against PostgreSQL
    result_df = pd.read_sql(nba_query, db_engine)
    
    if result_df.empty:
        print("[ERROR] User not found or insufficient transaction history.")
        return
        
    # Extracting the business intelligence variables
    days_to_next = int(result_df['days_to_next_purchase'][0])
    best_hour = int(result_df['optimal_contact_hour'][0])
    recommended_product = result_df['anchor_product'][0]
    
    # Displaying the output in a clean, enterprise-grade format
    print("\n[SUCCESS] Profile analyzed. Next-Best-Action generated!")
    print("==========================================================")
    print(f"🎯 MARKETING ACTION PLAN FOR USER {user_id}:")
    print(f"   ► Target Product:      '{recommended_product}'")
    print(f"   ► Optimal Timing:      Trigger campaign {days_to_next} days after last order.")
    print(f"   ► Best Contact Hour:   Send Push Notification at {best_hour}:00.")
    print("==========================================================")


# Testing the Engine on User ID 1
generate_next_best_action(user_id=1, db_engine=engine)
# ==============================================================================