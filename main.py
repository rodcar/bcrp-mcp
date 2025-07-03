from fastmcp import FastMCP
from typing import Dict, List, Any
import requests
import pandas as pd

import bcrpy

mcp = FastMCP("brcp-mcp")

TIME_SERIES_GROUP = "Grupo de serie"
METADATA_URL = "https://estadisticas.bcrp.gob.pe/estadisticas/series/metadata"

@mcp.tool()
def search_time_series_groups(keywords: List[str]) -> List[str]:
    """
    Search for time series groups using one or multiple keywords.
    
    This function searches the BCRP (Banco Central de Reserva del Perú) database
    for time series groups that match the provided keywords. It returns a list
    of unique time series group names that contain or relate to the search terms.
    
    Args:
        keywords (List[str]): A list containing one or more keywords to search for.
                             Each keyword should be a single word without spaces.
    
    Returns:
        List[str]: A list of unique time series group names that match the
                  search criteria. Returns an empty list if no matches are found.
    """
    banco = bcrpy.Marco()
    results = []
    for keyword in keywords:
        results.extend(banco.wordsearch(keyword)[TIME_SERIES_GROUP].tolist())
    return list(set(results))

@mcp.tool()
def search_time_series_by_group(time_series_group: str) -> Any:
    """
    Search for time series within a specific group from the BCRP database.
    
    This function retrieves time series metadata from the BCRP (Banco Central de Reserva del Perú)
    database and filters it to find all time series that belong to a specific group. It returns
    a list of dictionaries containing the code and name of each matching time series.
    
    Args:
        time_series_group (str): The name of the time series group to search within.
                                This should match or be contained within the "Grupo de serie"
                                field in the BCRP metadata.
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries where each dictionary contains:
                             - "code": The unique identifier code for the time series
                             - "name": The descriptive name of the time series
                             If an error occurs, returns a list with a single dictionary
                             containing an "error" key with the error message.
    """
    try:
        metadata = pd.read_csv(METADATA_URL, delimiter=';', encoding='latin-1')
        result_list = metadata[metadata[TIME_SERIES_GROUP].str.contains(time_series_group, na=False)].iloc[:, [0, 3]].values.tolist()
        return [{"code": row[0], "name": row[1]} for row in result_list[:50]]
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def get_time_series_data(time_series_code: str, start: str, end: str) -> List[List[str]]:
    """
    Get the data for a specific time series within a date range.
    
    This function retrieves time series data from the BCRP (Banco Central de Reserva del Perú)
    database for a specific time series code within the specified date range. The data is
    returned as a list of lists with dates formatted as 'YYYY-MM-DD'.
    
    Args:
        time_series_code (str): The unique code identifier for the time series.
        start (str): The start date for the data retrieval. Format should be '2020-1' 
                    for monthly data or '2020-1-1' for daily data.
        end (str): The end date for the data retrieval. Format should be '2020-1' 
                  for monthly data or '2020-1-1' for daily data.
    
    Returns:
        List[List[str]]: A list of lists where each inner list contains:
                        [formatted_date, time_series_value]
                        The date is formatted as 'YYYY-MM-DD' and the value is the
                        corresponding data point for that date.
    """
    banco = bcrpy.Marco()
    banco.codes = [time_series_code]
    banco.start = start
    banco.end = end
    return banco.GET(storage='df').reset_index().assign(index=lambda x: x['index'].dt.strftime('%Y-%m-%d')).astype(str).values.tolist()

@mcp.prompt()
def search_data(keyword: str) -> str:
    return f"""Follow the following steps to find the relevant time series:
    1. Search for the time series group using the search_time_serie_group tool with the keyword: {keyword}
    2. Search for the time series using the search_time_series_by_group tool with the time series group
    3. Return the time series code and name.
    4. If no time series is found, retry with different keywords. If you have found the time series, return the time series code and name.
    """

@mcp.prompt()
def ask(question: str) -> str:
    return f"""You are a financial analyst. You are given a question and you need to answer it.
    Question: {question}
    Follow the following steps to answer the question:
    1. Extract keywords from the question, these need to be related to financial time series.
    2. Search for the time series group using the search_time_serie_group tool with the keywords.
    3. Search for the time series using the search_time_series_by_group tool with the time series group
    4. Return the time series code and name.
    5. If no time series is found, retry with different keywords.
    6. If you have found the time series, select the relevant time series for the analysis, can be more than one if the question needs it.
    7. Get the data for the time series using the get_time_series_data tool. You can get the data for multiple time series if needed.
    8. Answer the question with the data.
    """

if __name__ == "__main__":
    mcp.run(transport="stdio")