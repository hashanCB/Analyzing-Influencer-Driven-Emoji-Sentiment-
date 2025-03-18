import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

# Step 1: Load the datasets
try:
    vcrix_df = pd.read_csv('./BTCVCRIX/2024-01-27 vcrix.csv')
    btc_df = pd.read_csv('./BTC/BTC-2019min.csv')
    print("Columns in vcrix_df:", vcrix_df.columns.tolist())
    print("Columns in btc_df:", btc_df.columns.tolist())
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure 'vcrix.csv' and 'btc.csv' are in the correct directory.")
    exit()

# Step 2: Convert date columns to datetime and filter by date range
# Handle vcrix_df
if 'date' in vcrix_df.columns:
    vcrix_df['date'] = pd.to_datetime(vcrix_df['date'])
    vcrix_df = vcrix_df[(vcrix_df['date'] >= '2019-05-27') & (vcrix_df['date'] <= '2019-11-23')]
    if vcrix_df.empty:
        print("Warning: No data in vcrix_df within the range 2019-05-27 to 2019-11-23.")
else:
    print("Warning: 'date' column not found in vcrix_df. Using index-based date conversion.")
    vcrix_df['date'] = pd.to_datetime(vcrix_df.index + 1, origin=pd.Timestamp('2018-01-04'))  # Adjust origin based on your data
    vcrix_df = vcrix_df[(vcrix_df['date'] >= '2019-05-27') & (vcrix_df['date'] <= '2019-11-23')]
    if vcrix_df.empty:
        print("Warning: No data in vcrix_df within the range 2019-05-27 to 2019-11-23 after index conversion.")

# Handle btc_df
if 'date' in btc_df.columns:
    btc_df['date'] = pd.to_datetime(btc_df['date'])
    btc_df = btc_df[(btc_df['date'] >= '2019-05-27') & (btc_df['date'] <= '2019-11-23')]
    if btc_df.empty:
        print("Warning: No data in btc_df within the range 2019-05-27 to 2019-11-23.")
elif 'unix' in btc_df.columns:
    print("Converting 'unix' timestamp to datetime.")
    btc_df['date'] = pd.to_datetime(btc_df['unix'], unit='s')  # Convert UNIX timestamp to datetime
    btc_df = btc_df[(btc_df['date'] >= '2019-05-27') & (btc_df['date'] <= '2019-11-23')]
    if btc_df.empty:
        print("Warning: No data in btc_df within the range 2019-05-27 to 2019-11-23.")
else:
    print("Error: Neither 'date' nor 'unix' column found in btc_df. Please check your CSV structure.")
    exit()

# Step 3: Aggregate BTC data to daily level (average close price per day)
btc_daily = btc_df.groupby(btc_df['date'].dt.date)['close'].mean().reset_index()
btc_daily['date'] = pd.to_datetime(btc_daily['date'])

# Step 4: Merge VCRIX and BTC data
merged_df = pd.merge(vcrix_df[['date', 'vcrix']], btc_daily[['date', 'close']], on='date', how='inner')
if merged_df.empty:
    print("Warning: No overlapping data between vcrix_df and btc_df within the range 2019-05-27 to 2019-11-23.")

# Step 5: Simulate On-Chain Metrics
# Note: Real on-chain data requires API access (e.g., Glassnode, CryptoQuant). Here, we simulate for demonstration.

# Simulate Whale Transaction Volume
btc_df['Volume_USD'] = btc_df['Volume BTC'] * btc_df['close']  # Approximate USD volume
btc_df = btc_df.sort_values('Volume_USD', ascending=False)
whale_threshold = int(len(btc_df) * 0.05)  # Top 5% as whales
whale_volume = btc_df.head(whale_threshold).groupby(btc_df['date'].dt.date)['Volume_USD'].sum().reset_index()
whale_volume['date'] = pd.to_datetime(whale_volume['date'])
merged_df = pd.merge(merged_df, whale_volume, on='date', how='left').fillna(0)

# Simulate Exchange Inflow/Outflow
np.random.seed(42)  # For reproducibility
merged_df['Exchange_Inflow'] = np.random.uniform(0, merged_df['close'].max() * 0.1, len(merged_df))
merged_df['Exchange_Outflow'] = np.random.uniform(0, merged_df['close'].max() * 0.1, len(merged_df))
merged_df['Netflow'] = merged_df['Exchange_Outflow'] - merged_df['Exchange_Inflow']

# Simulate Realized Cap
market_cap = merged_df['close'] * 10000000  # Simplified, assuming 10M BTC in circulation
realized_cap = market_cap * np.random.uniform(0.8, 1.2, len(merged_df))  # Simulated variation
merged_df['Realized_Cap'] = realized_cap

# Calculate MVRV Ratio
merged_df['MVRV_Ratio'] = market_cap / merged_df['Realized_Cap']

# Step 6: Create a multi-axis plot
if not merged_df.empty:
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot VCRIX on the left y-axis
    ax1.plot(merged_df['date'], merged_df['vcrix'], label='VCRIX', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('VCRIX (Volatility Index)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Second y-axis for BTC Close Price
    ax2 = ax1.twinx()
    ax2.plot(merged_df['date'], merged_df['close'], label='BTC Close Price', color='green')
    ax2.set_ylabel('BTC Close Price (USD)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Third y-axis for Whale Volume
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))  # Offset the third axis
    ax3.plot(merged_df['date'], merged_df['Volume_USD'], label='Whale Volume (USD)', color='red', alpha=0.5)
    ax3.set_ylabel('Whale Transaction Volume (USD)', color='red')
    ax3.tick_params(axis='y', labelcolor='red')

    # Format the x-axis
    plt.title('BTC Price, VCRIX, and On-Chain Metrics (2019-05-27 to 2019-11-23)')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)

    # Add grid and legend
    ax1.grid(True, linestyle='--', linewidth=0.5)
    fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
    fig.tight_layout()
    plt.show()

# Step 7: Print summary statistics
print("Summary of On-Chain Metrics:")
print(merged_df[['date', 'close', 'vcrix', 'Volume_USD', 'Netflow', 'MVRV_Ratio']].head())