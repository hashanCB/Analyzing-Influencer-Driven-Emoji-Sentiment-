import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Step 1: Load the dataset
# Assuming your dataset is in a CSV file named 'btc_data.csv'
try:
    df = pd.read_csv('./BTC/BTC-2019min.csv')
except FileNotFoundError:
    print("File 'btc_data.csv' not found. Please ensure the file exists in the correct directory.")
    exit()

# Step 2: Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Step 3: Plot the data
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['close'], label='Close Price', color='blue')

# Step 4: Format the plot
plt.title('BTC/USD Close Price Over Time', fontsize=16)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Price (USD)', fontsize=12)

# Format the x-axis to show dates nicely
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())  # Automatically adjust the date ticks
plt.xticks(rotation=45)

# Add a grid for better readability
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Add a legend
plt.legend()

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the plot
plt.show()