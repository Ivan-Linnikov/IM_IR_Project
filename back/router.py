import json
import os
from http.client import HTTPException

import pandas as pd
import pyterrier as pt
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from indexing import search_documents
from filter import filter_json_by_location_day_and_time  


router = APIRouter()

class QueryModel(BaseModel):
    query: str

@router.post("/")
def search(query_data: QueryModel):
    """
    This endpoint accepts a query and returns relevant documents.
    """
    query = query_data.query
    results = search_documents(query)
    return results

class FilterModel(BaseModel):
    city: Optional[str] = ''  
    day: Optional[str] = '' 
    time: Optional[str] = ''  

@router.post("/result")
def filter_results(filter_data: FilterModel):
    """
    This endpoint accepts city, day, and time as input and returns filtered JSON data.
    """
    city = filter_data.city  
    day = filter_data.day  
    time = filter_data.time  


    filter_json_by_location_day_and_time(city, day, time)

    with open('filtered_data_exact.json', 'r', encoding='utf-8') as file:
        filtered_results = file.read()
    return json.loads(filtered_results) 