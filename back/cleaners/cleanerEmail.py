import json

def clean_email_entries(data):
    for entry in data:
        if "Email" in entry and entry["Email"] == "":
            entry["Email"] = "Missing"
    return data

with open('datacleaned/cleaned_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cleaned_data = clean_email_entries(data)

with open('cleaned_dataFinal.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

print(json.dumps(cleaned_data, indent=4))
