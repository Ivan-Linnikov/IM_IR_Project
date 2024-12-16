import json
import os

# Define the file paths
input_file1 = 'datacleaned/cleaned_local.json'
input_file2 = 'datacleaned/cleaned_local_91.json'
output_file = 'datacleaned/merged_local.json'

def merge_json_files(file1, file2, output):
    # Check if the first input file exists
    if not os.path.isfile(file1):
        print(f"Error: The file '{file1}' does not exist.")
        return

    # Check if the second input file exists
    if not os.path.isfile(file2):
        print(f"Error: The file '{file2}' does not exist.")
        return

    try:
        # Load data from the first JSON file
        with open(file1, 'r', encoding='utf-8') as f1:
            data1 = json.load(f1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{file1}': {e}")
        return

    try:
        # Load data from the second JSON file
        with open(file2, 'r', encoding='utf-8') as f2:
            data2 = json.load(f2)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{file2}': {e}")
        return

    # Ensure both JSON files contain lists
    if not isinstance(data1, list):
        print(f"Error: The first JSON file '{file1}' does not contain a list.")
        return
    if not isinstance(data2, list):
        print(f"Error: The second JSON file '{file2}' does not contain a list.")
        return

    # Merge the two lists
    merged_data = data1 + data2

    try:
        # Write the merged data to the output file
        with open(output, 'w', encoding='utf-8') as outfile:
            json.dump(merged_data, outfile, ensure_ascii=False, indent=4)
        print(f"Successfully merged '{file1}' and '{file2}' into '{output}'.")
    except IOError as e:
        print(f"Error writing to file '{output}': {e}")

if __name__ == "__main__":
    merge_json_files(input_file1, input_file2, output_file)
