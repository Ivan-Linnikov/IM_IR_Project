from fastapi import APIRouter
from pydantic import BaseModel
from indexing import search_documents

# Create a router instance
router = APIRouter()

# Pydantic model for query input
class QueryModel(BaseModel):
    query: str

@router.post("/")
def search(query_data: QueryModel):
    """
    This endpoint accepts a query and returns relevant documents.
    """
    query = query_data.query  # Extract the query from the request
    print(query)
    results = search_documents(query)
    print(results)# Call the search logic from retrieval.py
    return results
