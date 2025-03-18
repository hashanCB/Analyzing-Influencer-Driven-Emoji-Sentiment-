import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Load the Twitter dataset
try:
    df = pd.read_csv('filtered_file.csv', low_memory=False)
except FileNotFoundError:
    print("File 'twitter_data.csv' not found.")
    exit()

# Step 2: Convert 'Date' to datetime and filter by date range
df['Date'] = pd.to_datetime(df['Date'])
df = df[(df['Date'] >= '2019-05-27') & (df['Date'] <= '2019-11-23')]

# Step 3: Convert sentiment to numerical scores
sentiment_map = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
df['Sentiment_Score'] = df['Sentiment'].map(sentiment_map).fillna(0)  # Default to 0 for unknown sentiments

# Step 4: Aggregate sentiment score by date (e.g., average sentiment per day)
daily_sentiment = df.groupby(df['Date'].dt.date)['Sentiment_Score'].mean().reset_index()
daily_sentiment['Date'] = pd.to_datetime(daily_sentiment['Date'])

# Step 5: Compute Exponential Moving Average (EMA) of sentiment
# Using a 7-day window (adjust as needed)
window_size = 7
daily_sentiment['Sentiment_EMA'] = daily_sentiment['Sentiment_Score'].ewm(span=window_size, adjust=False).mean()

# Step 6: Compute Sentiment Momentum (difference between current and lagged EMA)
daily_sentiment['SentimentMomentum'] = daily_sentiment['Sentiment_EMA'].diff()

# Step 7: Plot Sentiment Momentum
plt.figure(figsize=(12, 5))
plt.plot(daily_sentiment['Date'], daily_sentiment['SentimentMomentum'], label="Sentiment Momentum", color="purple")
plt.axhline(y=0, color="black", linestyle="--", label="Zero Line")
plt.xlabel("Date")
plt.ylabel("Momentum")
plt.title("Sentiment Momentum Indicator (2019-05-27 to 2019-11-23)")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Step 8: Optional - Print the data for inspection
print(daily_sentiment[['Date', 'Sentiment_EMA', 'SentimentMomentum']])