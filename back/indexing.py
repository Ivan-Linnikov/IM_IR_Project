import pyterrier as pt
import pandas as pd
import os

# Initialize PyTerrier
pt.java.init()  # New recommended initialization

# Define the index directory
INDEX_DIR = "./index"


def indexing_documents(data: pd.DataFrame):
    if not os.path.exists(INDEX_DIR):
        os.makedirs(INDEX_DIR, exist_ok=True)

        indexer = pt.IterDictIndexer(INDEX_DIR)

        # Ensure the 'docno' field exists
        if 'docno' not in data.columns:
            data['docno'] = data.index.astype(str)

        # Rename problematic columns to lowercase and remove spaces
        data.rename(columns=lambda x: x.strip().replace(' ', '_').lower(), inplace=True)

        # Check if required columns exist
        required_columns = ['docno', 'text', 'address', 'mobile', 'opening_times', 'categories', 'email', 'name']
        for col in required_columns:
            if col not in data.columns:
                print(f"Warning: '{col}' not found in the DataFrame. Filling with 'Missing'.")
                data[col] = 'Missing'

        # Print available columns
        print(f"Available columns: {data.columns}")

        # Select the required columns and convert to list of dicts
        documents = data[required_columns].to_dict(orient='records')

        indexer.index(documents)
        print("Indexing successful.")
    else:
        print("Indexing already completed.")


# Load JSON file and convert to DataFrame
json_file_path = 'FinalData/FinalLocal.json'  # Replace with the path to your JSON file
data = pd.read_json(json_file_path)

# Check if 'docno' exists
if 'docno' not in data.columns:
    data['docno'] = data.index.astype(str)

# Call the indexing function
indexing_documents(data)


def search_documents(query: str):
    """
    Perform search using the given query and return results.
    """
    # Use the updated retrieval method
    bm25 = pt.terrier.Retriever(INDEX_DIR, wmodel="BM25")
    result = bm25.search(query)

    # Save the entire search result to a CSV file
    result.to_csv("firstTry.csv", index=False)

    # Extract the top 20 results
    top_n_results = result
    top_n_docnos = top_n_results["docno"].astype(str).tolist()

    # Ensure 'docno' exists in the data
    if 'docno' not in data.columns:
        data['docno'] = data.index.astype(str)

    # Filter the top N hairdressers from the DataFrame
    top_n_hairdressers = data[data['docno'].isin(top_n_docnos)]

    # Convert the filtered DataFrame to JSON format
    data_exact_json = top_n_hairdressers.to_json(orient='records')

    # Save the filtered data as a JSON file
    with open("data_exact.json", "w", encoding='utf-8') as file:
        file.write(data_exact_json)

    return data_exact_json



