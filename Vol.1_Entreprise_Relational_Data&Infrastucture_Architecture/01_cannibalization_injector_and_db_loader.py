# ==============================================================================
# 8. Strategic EDA: Identifying High-Volume Products for Cannibalization Simulation :
# ==============================================================================
print("\n --- Identifying Top Revenue Drivers ---")

# Merging transactions records with product dimensions to extract readable insights
# I'm mapping the product name to the +32M rows in order products using a Left Join
top_products_df = pd.merge(order_products, products[['product_id', 'product_name']], on='product_id', how='left')

# Aggregating total sales volume per product to isolate the top 10 market leaders
top_10_products = top_products_df['product_name'].value_counts().head(10)

print("\n 🔥 Top 10 High-Volume Products:")
print(top_10_products)

# Memory Management Step: Deleting the massive temporary DataFrame
del top_products_df
print("\n RAM optimized by deleting temporary DataFrame successfully☑️.")

# ==============================================================================
# 9. Marketing Scenario Injection: Simulating Product Cannibalization
# ==============================================================================
print("\n--- [INITIATING] Cannibalization Scenario Simulation ---")

# Defining the business parameters for the marketing simulation 
cannibalized_product_name = "Banana" # Incumbent Product
promoted_product_name = "Bag of Organic Bananas" # Challenger Product

# Extracting unique products identifiers (Primary Keys) from dimensions table
cannibalized_product_id = products[products['product_name'] == cannibalized_product_name]['product_id'].values[0]
promoted_product_id = products[products['product_name'] == promoted_product_name]['product_id'].values[0]

print(f" [*] Incumbent Product: {cannibalized_product_name} (ID: {cannibalized_product_id} )")
print(f" [*] Challenger Product: {promoted_product_name} (ID: {promoted_product_id} )")

# Enforcing reproducibility for entreprise auditing and model validation
np.random.seed(42)

# Defining the temporal bounds of the marketing campain (Orders > 2,000,000)
# Isolating the baseline demand for the incumbent product within this window
campaign_mask = (order_products['product_id'] == cannibalized_product_id) & (order_products['order_id'] > 2000000 )

# Simulating the cross-elasticity effect: 30% of the incumbent's target audience
# Originaly transitions to the promoted product
cannibalize_mask = campaign_mask & (np.random.rand(len(order_products)) < 0.30 )

# Executing the demand shift (Data Mutation)
order_products.loc[cannibalize_mask, 'product_id'] = promoted_product_id

# Quantifying the absolute business impact
cannibalized_amount = cannibalize_mask.sum()
print("\n[SUCCESS] Marketing Scenario Data Mutation Completed.")
print(f"[METRIC]  Total Cannibalized Volume: {cannibalized_amount:,} units shifted from '{cannibalized_product_name}' to '{promoted_product_name}'.")

# ==============================================================================
# 10. ENTERPRISE DATA MIGRATION: LOADING TO POSTGRESQL (ETL - LOAD PHASE)
# ==============================================================================
print("\n--- [INITIATING] Enterprise Database Migration ---")

# Connection Setup 
db_user = 'postgres'
db_password = '8169' 
db_host = 'localhost'
db_port = '5432'
db_name = 'instacart_db'

# Creating connection link using psycopg2 and sqlalchemy
connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = sqlalchemy.create_engine(connection_string)

print("[*] Database engine configured successfully. Connection established.")

# Building a smart loading function
def load_to_db(df, table_name, engine):
    print(f"[*] Migrating table: '{table_name}' to PostgreSQL ...")
    start_time = time.time()
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False, chunksize=100000)
    
    print(f"[SUCCESS] '{table_name}' migrated seamlessly in {round(time.time() - start_time, 2)} seconds.")

# Star Schema Naming Convention
load_to_db(products, 'dim_products', engine)
load_to_db(orders, 'fact_orders', engine)

print("\n[WARNING] Commencing heavy data migration (32M+ rows). This will take a few minutes...")
# Cannibalized injected file covention
load_to_db(order_products, 'fact_order_products', engine)

print("\n[COMPLETED] Volume 1 : Infrastructure successfully deployed to PostgreSQL! 🚀")
# ==============================================================================