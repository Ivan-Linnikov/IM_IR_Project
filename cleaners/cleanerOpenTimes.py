import json

def clean_opening_times(data):
    for entry in data:
        opening_times = entry.get("Opening Times", {})
        if "" in opening_times and opening_times[""] == "":
            del opening_times[""]
    return data

# Load data from a JSON file
with open('datacleaned/merged_local.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cleaned_data = clean_opening_times(data)

# Save cleaned data to a new JSON file
with open('cleaned_data.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

# Print cleaned data to verify the change
print(json.dumps(cleaned_data, indent=4))