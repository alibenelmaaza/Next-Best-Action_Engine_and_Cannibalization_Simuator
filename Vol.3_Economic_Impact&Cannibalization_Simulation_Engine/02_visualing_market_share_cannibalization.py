# ==============================================================================
# 3. EXECUTIVE DASHBOARD: VISUALIZING MARKET SHARE CANNIBALIZATION
# ==============================================================================
import matplotlib.pyplot as plt
import numpy as np

print("\n--- [INITIATING] Executive Visualization Module ---")

# Preparing the data from the previous step
viz_df = share_pivot.reset_index()

# Setting up the canvas size and style for a corporate presentation
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

# Setting the positions and width for the bars
x = np.arange(len(viz_df['product_name']))
width = 0.35  

# Plotting the bars (Pre-campaign in Dark Blue, Post-campaign in Bright Blue)
bars1 = ax.bar(x - width/2, viz_df['1_Pre_Campaign'], width, label='Pre-Campaign', color='#2c3e50')
bars2 = ax.bar(x + width/2, viz_df['2_Post_Campaign'], width, label='Post-Campaign', color='#3498db')

# Formatting the axes and title
ax.set_ylabel('Market Share (%)', fontsize=12, fontweight='bold')
ax.set_title('Strategic Cannibalization: Market Share Shift', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(viz_df['product_name'], fontsize=12, fontweight='bold')
ax.legend(title='Timeline', fontsize=11)

# Adding data labels directly on top of the bars for instant readability
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', fontsize=11)

add_labels(bars1)
add_labels(bars2)

# Rendering the chart cleanly
plt.tight_layout()
plt.show()

print("[SUCCESS] Executive Chart rendered successfully.")
# ==============================================================================