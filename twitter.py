import pandas as pd

# Initialize an empty list to store filtered chunks
filtered_chunks = []

# Read the CSV file in chunks
for chunk in pd.read_csv("twitter_data.csv", chunksize=100000):  # Adjust chunksize as needed
    # Filter the chunk
    filtered_chunk = chunk[['date', 'msg']]  # Adjust column names as needed
    # Append the filtered chunk to the list
    filtered_chunks.append(filtered_chunk)

# Combine all filtered chunks into a single DataFrame
filtered_df = pd.concat(filtered_chunks, ignore_index=True)

# Save the filtered data to a new CSV file
filtered_df.to_csv("filtered_twitter_data.csv", index=False)

print("Filtered data saved to 'filtered_twitter_data.csv'.")