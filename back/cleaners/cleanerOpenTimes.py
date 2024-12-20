import json

def clean_opening_times(data):
    for entry in data:
        opening_times = entry.get("Opening Times", {})
        if "" in opening_times and opening_times[""] == "":
            del opening_times[""]
    return data

with open('datacleaned/merged_local.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cleaned_data = clean_opening_times(data)

with open('cleaned_data.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
