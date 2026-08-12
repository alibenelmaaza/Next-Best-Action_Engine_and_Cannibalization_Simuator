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