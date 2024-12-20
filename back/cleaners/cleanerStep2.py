import json

def remove_newlines(obj):
    if isinstance(obj, dict):
        return {k: remove_newlines(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [remove_newlines(item) for item in obj]
    elif isinstance(obj, str):
        return obj.replace('\n', '')
    else:
        return obj

with open('cleaned_output_first_local_after_91.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

cleaned_data = remove_newlines(data)

with open('cleaned_output_first_local_after_91_step2.json', 'w', encoding='utf-8') as outfile:
    json.dump(cleaned_data, outfile, ensure_ascii=False, indent=4)
