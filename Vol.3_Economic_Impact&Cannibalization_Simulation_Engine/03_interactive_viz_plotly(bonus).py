# ==============================================================================
# 4. EXECUTIVE DASHBOARD: INTERACTIVE VISUALIZATION WITH PLOTLY
# ==============================================================================
import plotly.graph_objects as go

print("\n--- [INITIATING] Interactive Plotly Dashboard Module ---")

# Preparing the dataframe
viz_df = share_pivot.reset_index()

# Initializing the Plotly Figure object
fig = go.Figure()

# 1. Adding the Pre-Campaign Bar Trace (Dark Blue)
fig.add_trace(go.Bar(
    x=viz_df['product_name'],
    y=viz_df['1_Pre_Campaign'],
    name='Pre-Campaign',
    marker_color='#2c3e50',
    # Automatically placing the percentage text on the bars
    text=viz_df['1_Pre_Campaign'].apply(lambda x: f"{x}%"),
    textposition='auto',
    hovertemplate="Product: %{x}<br>Share: %{y}%<extra></extra>"
))

# 2. Adding the Post-Campaign Bar Trace (Bright Blue)
fig.add_trace(go.Bar(
    x=viz_df['product_name'],
    y=viz_df['2_Post_Campaign'],
    name='Post-Campaign',
    marker_color='#3498db',
    text=viz_df['2_Post_Campaign'].apply(lambda x: f"{x}%"),
    textposition='auto',
    hovertemplate="Product: %{x}<br>Share: %{y}%<extra></extra>"
))

# 3. Customizing the layout for a premium corporate look
fig.update_layout(
    title={
        'text': '<b>Strategic Cannibalization: Market Share Shift</b>',
        'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top',
        'font': dict(size=22)
    },
    xaxis_title='<b>Product Category</b>',
    yaxis_title='<b>Market Share (%)</b>',
    barmode='group', # This places the bars side-by-side
    template='plotly_white', # Clean white background
    legend_title_text='<b>Timeline</b>',
    hovermode='x unified',
    margin=dict(t=80, b=40, l=40, r=40)
)

# Rendering the interactive chart
fig.show()

print("[SUCCESS] Interactive Plotly chart rendered successfully. Hover over the bars to test it!")
# ==============================================================================