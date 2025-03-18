import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the datasets
try:
    twitter_df = pd.read_csv('filtered_file.csv')
except FileNotFoundError:
    print("File 'twitter_data.csv' not found.")
    exit()

try:
    btc_df = pd.read_csv('./BTC/BTC-2019min.csv')
except FileNotFoundError:
    print("File 'btc_data.csv' not found.")
    exit()

# Step 2: Convert date columns to datetime and filter by date range
# Twitter data
twitter_df['Date'] = pd.to_datetime(twitter_df['Date'])
twitter_df = twitter_df[(twitter_df['Date'] >= '2019-05-27') & (twitter_df['Date'] <= '2019-11-23')]

# BTC data
btc_df['date'] = pd.to_datetime(btc_df['date'])
btc_df = btc_df[(btc_df['date'] >= '2019-05-27') & (btc_df['date'] <= '2019-11-23')]

# Step 3: Aggregate BTC data to daily level (average close price per day)
btc_daily = btc_df.groupby(btc_df['date'].dt.date)['close'].mean().reset_index()
btc_daily['date'] = pd.to_datetime(btc_daily['date'])

# Step 4: Summarize Twitter sentiment per day
# Count the number of Positive, Negative, etc. sentiments per day
sentiment_counts = twitter_df.groupby(['Date', 'Sentiment']).size().unstack(fill_value=0).reset_index()
sentiment_counts['Date'] = pd.to_datetime(sentiment_counts['Date'])

# Step 5: Merge the BTC and Twitter data on date
merged_df = pd.merge(btc_daily, sentiment_counts, left_on='date', right_on='Date', how='inner')

# Step 6: Prepare data for plotting
# Let's assume Sentiment has 'Positive' and 'Negative' values (adjust based on your data)
# We'll calculate a simple sentiment score: (Positive - Negative) / Total
if 'Positive' in merged_df.columns and 'Negative' in merged_df.columns:
    merged_df['Total_Tweets'] = merged_df['Positive'] + merged_df['Negative']
    # Avoid division by zero
    merged_df['Sentiment_Score'] = (merged_df['Positive'] - merged_df['Negative']) / merged_df['Total_Tweets'].replace(0, 1)
else:
    # If you have different sentiment labels, adjust accordingly
    print("Sentiment labels not as expected. Found columns:", merged_df.columns)
    # For simplicity, let's use Positive tweet count as the "sentiment" if Negative isn't present
    merged_df['Sentiment_Score'] = merged_df.get('Positive', 0)

# Step 7: Plot the data
plt.figure(figsize=(12, 6))
plt.scatter(merged_df['Sentiment_Score'], merged_df['close'], color='blue', alpha=0.5)
plt.title('Bitcoin Price vs Twitter Sentiment (2019-05-27 to 2019-11-23)', fontsize=16)
plt.xlabel('Sentiment Score (Positive - Negative / Total Tweets)', fontsize=12)
plt.ylabel('BTC Close Price (USD)', fontsize=12)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Optional: Print the merged data for inspection
print(merged_df[['date', 'close', 'Sentiment_Score']])