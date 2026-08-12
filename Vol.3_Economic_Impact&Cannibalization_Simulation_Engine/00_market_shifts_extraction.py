# ==============================================================================
# 1. CANNIBALIZATION SIMULATOR: EXTRACTING MARKET SHIFTS
# ==============================================================================
import pandas as pd
import sqlalchemy

print("\n--- [INITIATING] Cannibalization Simulator: Market Shift Detection ---")

# 1. Database connection parameters
db_user = 'postgres'
db_password = '8169'
db_host = 'localhost'
db_port = '5432'
db_name = 'instacart_db'

# Creating the database engine
connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = sqlalchemy.create_engine(connection_string)
print("[SUCCESS] Connected to PostgreSQL successfully.")

# 2. Writing the SQL Query to isolate the Campaign Impact
# We use CASE WHEN to split history into 'Pre-Campaign' and 'Post-Campaign'
impact_query = """
WITH CampaignData AS (
    SELECT 
        p.product_name,
        CASE 
            WHEN op.order_id <= 2000000 THEN '1_Pre_Campaign'
            ELSE '2_Post_Campaign'
        END AS campaign_period,
        COUNT(*) AS total_sales
    FROM fact_order_products op
    JOIN dim_products p ON op.product_id = p.product_id
    WHERE p.product_name IN ('Banana', 'Bag of Organic Bananas')
    GROUP BY p.product_name, campaign_period
)
SELECT * FROM CampaignData
ORDER BY product_name, campaign_period;
"""

print("[*] Executing SQL Query to scan 32M+ rows for volume shifts...")
sales_shift_df = pd.read_sql(impact_query, engine)

# 3. Pivoting the data to create a professional Business Report format
pivot_df = sales_shift_df.pivot(index='product_name', columns='campaign_period', values='total_sales')

# 4. Calculating the absolute Volume Shift
pivot_df['Volume_Shift'] = pivot_df['2_Post_Campaign'] - pivot_df['1_Pre_Campaign']

print("[SUCCESS] Market shifts detected successfully!\n")
print("--- Cannibalization Impact Analysis ---")
display(pivot_df)
# ==============================================================================