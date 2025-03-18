import pandas as pd
import emoji

# Function to check if a text contains emojis
def contains_emoji(text):
    text = str(text)  # Ensure text is a string
    return bool(emoji.emoji_list(text))  # Returns True if emojis are found

# Read the CSV file in chunks with error handling
chunk_size = 10000  # Adjust based on your system's memory
filtered_rows = []

try:
    for chunk in pd.read_csv('Bitcointweets.csv', chunksize=chunk_size, on_bad_lines='skip', engine='python'):
        # Filter rows with emojis in the 'text' column
        filtered_chunk = chunk[chunk['text'].apply(contains_emoji)]
        filtered_rows.append(filtered_chunk)
except pd.errors.ParserError as e:
    print(f"ParserError: {e}")
    print("Skipping problematic rows and continuing...")

# Combine all filtered chunks into a single DataFrame
if filtered_rows:
    filtered_df = pd.concat(filtered_rows)
    # Save the filtered data to a new CSV file
    filtered_df.to_csv('filtered_file.csv', index=False)
    print(f"Filtered data saved to 'filtered_file.csv'. Found {len(filtered_df)} rows with emojis.")
else:
    print("No rows were processed due to errors.")
















# ====================================

# import pandas as pd
# import emoji

# # Function to check if a text contains emojis
# def contains_emoji(text):
#     text = str(text)  # Ensure text is a string
#     return bool(emoji.emoji_list(text))

# # Read the CSV file in chunks with error handling
# chunk_size = 10000  # Adjust based on your system's memory
# filtered_rows = []

# try:
#     for chunk in pd.read_csv('Bitcoin_tweets.csv', chunksize=chunk_size, on_bad_lines='skip', engine='python'):
#         # Filter rows with emojis in the 'text' column
#         filtered_chunk = chunk[chunk['text'].apply(contains_emoji)]
#         filtered_rows.append(filtered_chunk)
# except pd.errors.ParserError as e:
#     print(f"ParserError: {e}")
#     print("Skipping problematic rows and continuing...")

# # Combine all filtered chunks into a single DataFrame
# if filtered_rows:
#     filtered_df = pd.concat(filtered_rows)
#     # Save the filtered data to a new CSV file
#     filtered_df.to_csv('filtered_file.csv', index=False)
#     print(f"Filtered data saved to 'filtered_file.csv'. Found {len(filtered_df)} rows with emojis.")
# else:
#     print("No rows were processed due to errors.")