import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Step 1: Load the datasets
try:
    vcrix_df = pd.read_csv('./BTCVCRIX/2024-01-27 vcrix.csv')
    btc_df = pd.read_csv('./BTC/BTC-2019min.csv')
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure 'vcrix.csv' and 'btc.csv' are in the correct directory.")
    exit()

# Step 2: Convert date columns to datetime and filter by date range
# vcrix data
vcrix_df['date'] = pd.to_datetime(vcrix_df['date'])
vcrix_df = vcrix_df[(vcrix_df['date'] >= '2019-05-27') & (vcrix_df['date'] <= '2019-11-23')]

# btc data
btc_df['date'] = pd.to_datetime(btc_df['date'])
btc_df = btc_df[(btc_df['date'] >= '2019-05-27') & (btc_df['date'] <= '2019-11-23')]

# Step 3: Aggregate BTC data to daily level (average close price per day)
btc_daily = btc_df.groupby(btc_df['date'].dt.date)['close'].mean().reset_index()
btc_daily['date'] = pd.to_datetime(btc_daily['date'])

# Step 4: Merge the datasets on date
merged_df = pd.merge(vcrix_df[['date', 'vcrix']], btc_daily[['date', 'close']], on='date', how='inner')

# Step 5: Create a dual-axis plot
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot vcrix on the left y-axis
ax1.plot(merged_df['date'], merged_df['vcrix'], label='VCRIX', color='blue')
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('VCRIX (Volatility Index)', color='blue', fontsize=12)
ax1.tick_params(axis='y', labelcolor='blue')

# Create a second y-axis for BTC close price
ax2 = ax1.twinx()
ax2.plot(merged_df['date'], merged_df['close'], label='BTC Close Price', color='red')
ax2.set_ylabel('BTC Close Price (USD)', color='red', fontsize=12)
ax2.tick_params(axis='y', labelcolor='red')

# Format the x-axis to show dates nicely
plt.title('VCRIX vs BTC Close Price (2019-05-27 to 2019-11-23)', fontsize=16)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(rotation=45)

# Add grid and legend
ax1.grid(True, linestyle='--', linewidth=0.5)
fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))

# Display the plot
plt.show()

# Optional: Print the merged data for inspection
print(merged_df)