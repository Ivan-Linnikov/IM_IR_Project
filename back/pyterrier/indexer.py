import pyterrier as pt
import pandas as pd
import json
import os

# Initialize PyTerrier
if not pt.java.started():
    pt.java.init()

# File Path to JSON file
json_file_path = "datacleaned/merged_local.json"

# Load JSON Data
if not os.path.isfile(json_file_path):
    raise FileNotFoundError(f"Error: File '{json_file_path}' not found.")

with open(json_file_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Clean JSON Data
def clean_opening_times(opening_times):
    """
    Clean and normalize the 'Opening Times' field.
    """
    if not isinstance(opening_times, dict):
        return ""
    return " ".join(
        f"{k.strip().replace('*', '')}: {v.strip()}"
        for k, v in opening_times.items()
        if k.strip() and v.strip()  # Exclude empty keys or values
    )

# Process JSON data into a DataFrame
processed_df = pd.DataFrame([
    {
        "docno": str(idx),
        "Name": item.get("Name", "").strip(),
        "Address": item.get("Address", "").strip(),
        "Mobile": item.get("Mobile", "").strip(),
        "Email": item.get("Email", "").strip(),
        "Categories": " ".join(item.get("Categories", [])),
        "OpeningTimes": clean_opening_times(item.get("Opening Times", {}))
    }
    for idx, item in enumerate(json_data)
])

# Verify DataFrame structure
print("DataFrame Structure:")
print(processed_df.info())  # Check DataFrame columns
print("Data Sample:")
print(processed_df.head())  # Print first 5 rows of the DataFrame

# Ensure all fields are strings (PyTerrier requires all fields to be string-like)
processed_df = processed_df.fillna("").astype(str)

# Specify Index Path
index_path = "./hairdressers_index"

# Define indexer meta fields (note: we removed 'text')
indexer = pt.IterDictIndexer(
    index_path,
    meta={
        'docno': 24,
        'Name': 100,
        'Address': 200,
        'Mobile': 50,
        'Email': 100,
        'Categories': 200,
        'OpeningTimes': 500
    },
    overwrite=True  # Ensures we overwrite any existing index
)


# 🔥 NEW: Convert DataFrame to list of dicts
records = processed_df.to_dict(orient="records")

# 🔥 NEW: Pass list of dictionaries to the indexer
indexer.index(records)

print(f"Indexing complete! Index stored at: {index_path}")
