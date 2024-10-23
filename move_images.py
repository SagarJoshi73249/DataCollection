import os
import shutil
import re

# Define the path to the main folder and the destination folder
main_folder = r'd:\RAL_AAA+AA+D\imgs_b'
destination_folder = r'd:\RAL_AAA+AA+D\img_b'

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Initialize a list to hold the cumulative count of images
cumulative_list = []
cumulative_count = 0

# Function to extract the numeric part of the folder name
def numeric_key(subfolder_name):
    match = re.search(r'\d+', subfolder_name)
    return int(match.group()) if match else float('inf')

# Iterate over each subfolder in the main folder sorted by numeric order
for subfolder in sorted(os.listdir(main_folder), key=numeric_key):
    subfolder_path = os.path.join(main_folder, subfolder)

    # Check if it's a directory
    if os.path.isdir(subfolder_path):
        # Initialize a count for the current subfolder
        count = 0
        
        # Sort the files in the subfolder by name
        for filename in sorted(os.listdir(subfolder_path)):
            file_path = os.path.join(subfolder_path, filename)
            
            # Check if it's a file (not a directory)
            if os.path.isfile(file_path):
                # Create the new filename with the prefix
                new_filename = f"{subfolder}_{filename}"
                new_file_path = os.path.join(destination_folder, new_filename)
                
                # Move the file to the destination folder
                shutil.copy2(file_path, new_file_path)
                
                # Increment the count for the current subfolder
                count += 1

        # Update the cumulative count and add it to the list
        cumulative_count += count
        cumulative_list.append(cumulative_count)

print("All images have been moved and renamed successfully.")
print("Cumulative list of image counts:", cumulative_list)
