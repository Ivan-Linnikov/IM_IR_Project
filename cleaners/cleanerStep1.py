import json

# Load the original JSON data
with open('data/final_all_salon_data_after_91.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

# Write it back out to a new file without any unicode escapes
with open('cleaned_output_first_local_after_91.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4)

print("Data cleaned and saved to cleaned_output.json.")

