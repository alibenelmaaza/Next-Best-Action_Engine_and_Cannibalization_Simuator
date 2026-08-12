# ==============================================================================
# 2. CANNIBALIZATION SIMULATOR: MARKET SHARE DYNAMICS
# ==============================================================================
print("\n--- [INITIATING] Market Share & Cannibalization Analysis ---")

# 1. Calculating Total Category Volume per period
# We need the total 'pie' size for each period to calculate the slices (shares) accurately
category_totals = sales_shift_df.groupby('campaign_period')['total_sales'].transform('sum')

# 2. Calculating the Market Share (Percentage) for each product
sales_shift_df['market_share_%'] = (sales_shift_df['total_sales'] / category_totals) * 100
sales_shift_df['market_share_%'] = sales_shift_df['market_share_%'].round(2)

# 3. Pivoting the data for executive presentation
share_pivot = sales_shift_df.pivot(index='product_name', columns='campaign_period', values='market_share_%')

# 4. Calculating the true Market Share Shift (in Percentage Points)
share_pivot['Share_Shift_(pp)'] = share_pivot['2_Post_Campaign'] - share_pivot['1_Pre_Campaign']

print("[SUCCESS] Market Share dynamics calculated successfully!\n")
print("--- True Cannibalization Impact (Market Share) ---")
display(share_pivot)
# ==============================================================================