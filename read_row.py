import os
import pandas as pd
import re

# Specify the directory containing your CSV files
folder_path = r'd:\RAL_AAA+AA+D\delta_action_dir'

# Initialize variables
total_rows = 0
cumulative_rows_list = []

# Create a list to store the files along with their extracted 't{i}' index
file_list = []

# Regular expression to extract the number after 't' in the filename
pattern = r'delta_action_t(\d+)_.*_robot_poses.csv'

# Loop through all the files in the directory
for filename in os.listdir(folder_path):
    # Check if the file matches the expected pattern
    match = re.match(pattern, filename)
    if match:
        # Extract the 't{i}' index from the filename
        t_index = int(match.group(1))
        file_list.append((t_index, filename))

# Sort the file list by the 't{i}' index
file_list.sort(key=lambda x: x[0])

# Now process the files in the sorted order
for t_index, filename in file_list:
    file_path = os.path.join(folder_path, filename)
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Get the number of rows in the DataFrame
    num_rows = len(df)
    
    # Update the total number of rows
    total_rows += num_rows
    
    # Append the current total to the cumulative list
    cumulative_rows_list.append(total_rows)

# Print the total number of rows
print(f"Total number of rows across all files: {total_rows}")

# Print the cumulative list
print(f"Cumulative row numbers in sorted order: {cumulative_rows_list}")
