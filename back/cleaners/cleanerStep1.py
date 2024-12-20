import json

with open('data/final_all_salon_data_after_91.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

with open('cleaned_output_first_local_after_91.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4)


