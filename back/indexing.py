import pyterrier as pt
import pandas as pd
import os


pt.java.init()  

INDEX_DIR = "./index"


def indexing_documents(data: pd.DataFrame):
    if not os.path.exists(INDEX_DIR):
        os.makedirs(INDEX_DIR, exist_ok=True)

        indexer = pt.IterDictIndexer(INDEX_DIR)

        if 'docno' not in data.columns:
            data['docno'] = data.index.astype(str)

        data.rename(columns=lambda x: x.strip().replace(' ', '_').lower(), inplace=True)

        required_columns = ['docno', 'text', 'address', 'mobile', 'opening_times', 'categories', 'email', 'name']
        for col in required_columns:
            if col not in data.columns:
                print(f"Warning: '{col}' not found in the DataFrame. Filling with 'Missing'.")
                data[col] = 'Missing'

        print(f"Available columns: {data.columns}")

        documents = data[required_columns].to_dict(orient='records')

        indexer.index(documents)
        print("Indexing successful.")
    else:
        print("Indexing already completed.")



json_file_path = 'FinalData/FinalLocal.json'  
data = pd.read_json(json_file_path)

if 'docno' not in data.columns:
    data['docno'] = data.index.astype(str)

indexing_documents(data)


def search_documents(query: str):
    """
    Perform search using the given query and return results.
    """
    bm25 = pt.terrier.Retriever(INDEX_DIR, wmodel="BM25")
    result = bm25.search(query)

    result.to_csv("firstTry.csv", index=False)

    top_n_results = result
    top_n_docnos = top_n_results["docno"].astype(str).tolist()

    if 'docno' not in data.columns:
        data['docno'] = data.index.astype(str)

    top_n_hairdressers = data[data['docno'].isin(top_n_docnos)]
    data_exact_json = top_n_hairdressers.to_json(orient='records')

    with open("data_exact.json", "w", encoding='utf-8') as file:
        file.write(data_exact_json)

    return data_exact_json



