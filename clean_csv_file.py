import os
import pandas as pd

# Define the path to the folder containing the CSV files
folder_path = r'C:\Users\CAM\Desktop\50_action'

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Iterate through each CSV file
for csv_file in csv_files:
    # Construct the full path to the CSV file
    csv_path = os.path.join(folder_path, csv_file)
    
    # Load the CSV file, skipping the first row
    data = pd.read_csv(csv_path, skiprows=1)
    
    # Save the data back to the CSV file, overwriting it
    data.to_csv(csv_path, index=False)

    print(f"First row removed from {csv_file}.")

print("First row removed from all CSV files in the folder.")
