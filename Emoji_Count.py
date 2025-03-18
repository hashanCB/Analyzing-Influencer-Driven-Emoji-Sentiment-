import pandas as pd
import emoji
import matplotlib.pyplot as plt
from collections import Counter

# Force the TkAgg backend (simplified for now)  2019-05-27 2019-11-23
plt.switch_backend('TkAgg')

# Function to extract all emojis from a text
def extract_emojis(text):
    text = str(text)  # Ensure text is a string
    return [e['emoji'] for e in emoji.emoji_list(text)]

# Read the filtered CSV file
try:
    filtered_df = pd.read_csv('filtered_file.csv', low_memory=False)  # Suppress DtypeWarning
except FileNotFoundError:
    print("Filtered file 'filtered_file.csv' not found.")
    exit()

# Initialize a counter for emojis
emoji_counter = Counter()

# Extract and count emojis from the 'text' column
for text in filtered_df['text']:
    emojis = extract_emojis(text)
    emoji_counter.update(emojis)

# Get the top 20 most common emojis
top_20_emojis = emoji_counter.most_common(20)

# Separate emojis and their counts for plotting
emojis, counts = zip(*top_20_emojis)

# Plot the data with numeric x-axis
plt.figure(figsize=(12, 8))
plt.bar(range(len(emojis)), counts, color='skyblue')
plt.xlabel('Emoji Index')
plt.ylabel('Count')
plt.title('Top 20 Emojis in Filtered Tweets')

# Set x-axis ticks to use numbers (1 to 20)
plt.xticks(range(len(emojis)), range(1, len(emojis) + 1))

# Avoid tight_layout to prevent rendering issues
# plt.tight_layout()  # Keep commented out for now

# Display the plot
plt.show()

# Print the mapping of indices to emojis and their counts
print("Mapping of Emoji Indices to Emojis and Counts:")
for i, (emoji_char, count) in enumerate(top_20_emojis, 1):
    print(f"Index {i}: Emoji = {emoji_char}, Count = {count}")