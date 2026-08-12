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