import json

def remove_newlines(obj):
    if isinstance(obj, dict):
        return {k: remove_newlines(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [remove_newlines(item) for item in obj]
    elif isinstance(obj, str):
        # Remove newline characters from the string
        return obj.replace('\n', '')
    else:
        return obj

# Load the original JSON data
with open('cleaned_output_first_local_after_91.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

# Recursively remove all newlines from strings
cleaned_data = remove_newlines(data)

# Write the cleaned data back out to a new file without unicode escapes
with open('cleaned_output_first_local_after_91_step2.json', 'w', encoding='utf-8') as outfile:
    json.dump(cleaned_data, outfile, ensure_ascii=False, indent=4)

print("Data cleaned and saved to cleaned_output.json.")
