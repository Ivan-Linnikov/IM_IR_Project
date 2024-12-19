import pyterrier as pt
import pandas as pd
import os
import indexing as indexing

bm25 = pt.BatchRetrieve(INDEX_DIR, wmodel="BM25")


def search():

 query =  "my text here"

result = bm25.search(query)

result.to_csv("firstTry", index = False)

top_n_results = result.head(10)
top_n_docnos = top_n_results["docno"].astype(str).tolist()
top_n_hairdressers = data[data["docno"].isin(top_n_docnos)]
save_to_csv(top_n_hairdressers, output_file="data_exact.csv")
