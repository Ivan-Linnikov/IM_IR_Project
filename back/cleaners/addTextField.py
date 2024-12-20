import json

def generate_text_field(data):
    for entry in data:
        text_content = []
        for key in ["Name", "Address", "Categories"]:
            if key in entry:
                value = entry[key]
                if isinstance(value, list):
                    text_content.append(f"{key}: {', '.join(value)}")
                elif value != "Missing":
                    text_content.append(f"{key}: {value}")
        entry["text"] = ' | '.join(text_content)
    return data

with open('FinalData/cleaned_dataFinal.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cleaned_data = generate_text_field(data)

with open('FinalLocal.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

print(json.dumps(cleaned_data, indent=4))
