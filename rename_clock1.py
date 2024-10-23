import os
import glob
import re

def rename_files(directory):
    # Ensure the directory exists
    if not os.path.isdir(directory):
        print(f'The directory "{directory}" does not exist.')
        return

    # Define the file pattern to include the .csv extension
    file_pattern = os.path.join(directory, 'state_columns_t*_robot_poses.csv')
    all_files = glob.glob(file_pattern)

    # Compile a regular expression to match files like 'state_columns_t{i}_robot_poses.csv'
    regex_pattern = re.compile(r'^state_columns_t\d+_robot_poses\.csv$')

    # Filter the files to only include those that match the regex pattern
    files_to_rename = [f for f in all_files if regex_pattern.match(os.path.basename(f))]

    # Print the file pattern and files found for debugging
    print(f'Looking for files matching: {file_pattern}')
    print(f'Files to rename: {files_to_rename}')

    if not files_to_rename:
        print(f'No files found matching the specified pattern in "{directory}".')
        return

    for old_name in files_to_rename:
        # Construct the new file name by replacing '_robot_poses.csv' with '_clock1_robot_poses.csv'
        new_name = old_name.replace('_robot_poses.csv', '_clock1_robot_poses.csv')

        # Rename the file
        os.rename(old_name, new_name)
        print(f'Renamed "{old_name}" to "{new_name}"')

if __name__ == '__main__':
    # Specify the directory containing the files
    directory = r'D:\RAL_AAA+AA+D\state_files'
    rename_files(directory)
