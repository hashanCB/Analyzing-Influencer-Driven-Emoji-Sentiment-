import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the Twitter dataset
try:
    df = pd.read_csv('filtered_file.csv', low_memory=False)
except FileNotFoundError:
    print("File 'twitter_data.csv' not found.")
    exit()

# Step 2: Convert 'Date' to datetime and filter by date range (2019-05-27 to 2019-11-23)
df['Date'] = pd.to_datetime(df['Date'])
df = df[(df['Date'] >= '2019-05-27') & (df['Date'] <= '2019-11-23')]

# Step 3: Convert sentiment to numerical scores
sentiment_map = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
df['SentimentScore'] = df['Sentiment'].map(sentiment_map).fillna(0)  # Default to 0 for unknown sentiments

# Step 4: Create a column to identify weekdays (0-4) and weekends (5-6)
df["DayOfWeek"] = df["Date"].dt.dayofweek
df["Weekend"] = df["DayOfWeek"].apply(lambda x: "Weekend" if x >= 5 else "Weekday")

# Step 5: Compute average sentiment score for weekdays and weekends
sentiment_weekend = df.groupby("Weekend")["SentimentScore"].mean()

# Step 6: Bar Chart
plt.figure(figsize=(6, 4))
sentiment_weekend.plot(kind="bar", color=["blue", "orange"])
plt.xlabel("Day Type")
plt.ylabel("Average Sentiment Score")
plt.title("Weekend vs. Weekday Sentiment Score (2019-05-27 to 2019-11-23)")
plt.xticks(rotation=0)  # Ensure labels are horizontal for clarity
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Step 7: Optional - Print the results for inspection
print("Average Sentiment Score by Day Type:")
print(sentiment_weekend)