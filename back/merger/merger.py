import json
import os

input_file1 = 'datacleaned/cleaned_local.json'
input_file2 = 'datacleaned/cleaned_local_91.json'
output_file = 'datacleaned/merged_local.json'

def merge_json_files(file1, file2, output):
    if not os.path.isfile(file1):
        print(f"Error: The file '{file1}' does not exist.")
        return
    
    if not os.path.isfile(file2):
        print(f"Error: The file '{file2}' does not exist.")
        return

    try:
        with open(file1, 'r', encoding='utf-8') as f1:
            data1 = json.load(f1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{file1}': {e}")
        return

    try:
        with open(file2, 'r', encoding='utf-8') as f2:
            data2 = json.load(f2)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{file2}': {e}")
        return

    if not isinstance(data1, list):
        print(f"Error: The first JSON file '{file1}' does not contain a list.")
        return
    if not isinstance(data2, list):
        print(f"Error: The second JSON file '{file2}' does not contain a list.")
        return

    merged_data = data1 + data2

    try:
        with open(output, 'w', encoding='utf-8') as outfile:
            json.dump(merged_data, outfile, ensure_ascii=False, indent=4)
        print(f"Successfully merged '{file1}' and '{file2}' into '{output}'.")
    except IOError as e:
        print(f"Error writing to file '{output}': {e}")

if __name__ == "__main__":
    merge_json_files(input_file1, input_file2, output_file)
