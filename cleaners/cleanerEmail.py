import json

def clean_email_entries(data):
    for entry in data:
        # Check if email is empty and set to 'Missing'
        if "Email" in entry and entry["Email"] == "":
            entry["Email"] = "Missing"
    return data

# Load data from a JSON file
with open('datacleaned/cleaned_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cleaned_data = clean_email_entries(data)

# Save cleaned data to a new JSON file
with open('cleaned_dataFinal.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

# Print cleaned data to verify the change
print(json.dumps(cleaned_data, indent=4))
