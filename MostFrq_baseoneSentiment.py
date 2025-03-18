import pandas as pd
import emoji
import matplotlib.pyplot as plt
from collections import Counter

# Force the TkAgg backend (simplified for now)
plt.switch_backend('TkAgg')

# Function to extract all emojis from a text
def extract_emojis(text):
    text = str(text)  # Ensure text is a string
    return [e['emoji'] for e in emoji.emoji_list(text)]

# Step 1: Read the filtered CSV file
try:
    df = pd.read_csv('filtered_file.csv', low_memory=False)  # Adjust the filename to match your dataset
except FileNotFoundError:
    print("File 'twitter_data.csv' not found.")
    exit()

# Step 2: Convert 'Date' to datetime and filter by date range
df['Date'] = pd.to_datetime(df['Date'])
filtered_df = df[(df['Date'] >= '2019-05-27') & (df['Date'] <= '2019-11-23')]

# Step 3: Extract emojis and associate them with sentiment
emoji_sentiment_dict = {'Positive': Counter(), 'Neutral': Counter(), 'Negative': Counter()}
total_emoji_counter = Counter()

for index, row in filtered_df.iterrows():
    text = row['text']
    sentiment = row['Sentiment']
    emojis = extract_emojis(text)
    
    # Update the counter for the specific sentiment
    if sentiment in emoji_sentiment_dict:
        emoji_sentiment_dict[sentiment].update(emojis)
    # Update the total counter
    total_emoji_counter.update(emojis)

# Step 4: Get the top 20 most common emojis overall
top_20_emojis = total_emoji_counter.most_common(20)

# Step 5: Categorize each top emoji based on the dominant sentiment
emoji_categories = {}
for emoji_char, _ in top_20_emojis:
    # Count occurrences of this emoji in each sentiment category
    positive_count = emoji_sentiment_dict['Positive'].get(emoji_char, 0)
    neutral_count = emoji_sentiment_dict['Neutral'].get(emoji_char, 0)
    negative_count = emoji_sentiment_dict['Negative'].get(emoji_char, 0)
    
    # Determine the dominant sentiment
    sentiment_counts = {'Positive': positive_count, 'Neutral': neutral_count, 'Negative': negative_count}
    dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    emoji_categories[emoji_char] = dominant_sentiment

# Step 6: Prepare data for plotting
emojis, counts = zip(*top_20_emojis)
colors = []
for emoji_char in emojis:
    sentiment = emoji_categories[emoji_char]
    if sentiment == 'Positive':
        colors.append('green')
    elif sentiment == 'Neutral':
        colors.append('gray')
    else:  # Negative
        colors.append('red')

# Step 7: Plot the data with numeric x-axis
plt.figure(figsize=(12, 8))
plt.bar(range(len(emojis)), counts, color=colors)
plt.xlabel('Emoji Index')
plt.ylabel('Count')
plt.title('Top 20 Emojis in Filtered Tweets (2019-05-27 to 2019-11-23) by Sentiment')

# Set x-axis ticks to use numbers (1 to 20)
plt.xticks(range(len(emojis)), range(1, len(emojis) + 1))

# Add a legend for sentiment
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='green', label='Positive'),
    Patch(facecolor='gray', label='Neutral'),
    Patch(facecolor='red', label='Negative')
]
plt.legend(handles=legend_elements, title='Sentiment')

# Display the plot
plt.show()

# Step 8: Print the mapping of indices to emojis, counts, and their sentiment category
print("Mapping of Emoji Indices to Emojis, Counts, and Sentiment:")
for i, (emoji_char, count) in enumerate(top_20_emojis, 1):
    sentiment = emoji_categories[emoji_char]
    print(f"Index {i}: Emoji = {emoji_char}, Count = {count}, Sentiment = {sentiment}")