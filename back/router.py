from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from indexing import search_documents
from filter import filter_json_by_location_day_and_time  


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

# Pydantic model for query input
class FilterModel(BaseModel):
    city: Optional[str] = ''  # Optional, defaults to empty string
    day: Optional[str] = ''  # Optional, defaults to empty string
    time: Optional[str] = ''  # Optional, defaults to empty string

@router.post("/filter")
def filter_results(filter_data: FilterModel):
    """
    This endpoint accepts city, day, and time as input and returns filtered JSON data.
    """
    city = filter_data.city  # Extract city from request (used as location in the filter function)
    day = filter_data.day  # Extract day from request
    time = filter_data.time  # Extract time from request

    print(f"City: {city}, Day: {day}, Time: {time}")  # Debugging information

    # Call the filter logic from the filter function
    filter_json_by_location_day_and_time(city, day, time)
    
    # Read the filtered data from the output file
    with open('filtered_data_ex.json', 'r', encoding='utf-8') as file:
        filtered_results = file.read()
    
    return filtered_results  # Return the filtered results as a JSON response