from fastmcp import FastMCP
from typing import Optional
import requests
import urllib.parse

# Shared MCP server instance
mcp = FastMCP("Norwegian Historical Archives Search Server")
mcp.description = """
Norwegian Historical Archives Search Server provides access to centuries of 
Norwegian historical documents (16th to 20th centuries).

Use this server to whenever the user asks questions regarding Norwegian archival materials or history.

Search queries should be provided in Norwegian only!

Languages: Norwegian
Geographic scope: Norway and related historical territories
"""

def validate_date(date_str: str) -> bool:
    """Validate YYYY-MM-DD date format"""
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def query_api(search_url: str)  -> list[dict]:
    """
    Function for sending http queries and filtering the results.
    """
    try:
        output = requests.get(search_url)
        data = output.json()
        if 'data' not in data:
            return []
            
        filtered_result = [
            {   
                'id': d.get('id'),
                'text': d.get('text', ''),
                'archiveUnitName': d.get('archiveUnitName', ''),
                'sourceTitleNb': d.get('sourceTitleNb'),
                'sourceStartYear': d.get('sourceStartYear'),
                'sourceEndYear': d.get('sourceEndYear'),
                'thumbnailUrl': d.get('thumbnailUrl', '')
            } 
            for d in data['data']
        ]
        return filtered_result
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except (KeyError, ValueError) as e:
        raise Exception(f"Failed to parse API response: {str(e)}")

@mcp.tool()
def search_index(query_term: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> list[dict]:
    """
    Query term search to an api of the Norwegian National Archives.
    Search queries should be provided in Norwegian only!

    Args:
        query_term: search term in Norwegian.
        start_date: search documents from this date onwards. The form is: YYYY-MM-DD
        end_date: search documents up to this date. The form is: YYYY-MM-DD

    Returns:
    A list of dictionaries containing the search results. 
    The data fields are:
    - 'id': Reference id of the document
    - 'text': Contains the transcribed text content (or part of it) of the document
    - 'sourceStartYear': Start year of the source collection
    - 'sourceEndYear': End year of the source collection
    - 'archiveUnitName': Name of the archive unit that the document belongs to.
    - 'sourceTitleNb': Name of the archive, archive reference, protocol number etc. relating to the document
    - 'thumbnailUrl': Url to the digitized document
    """   
    base_url = "https://nye.digitalarkivet.no/api/media-file/search/transcription?s="
    search_url = base_url + urllib.parse.quote(query_term)

    if start_date and not validate_date(start_date):
        raise ValueError("start_date must be in YYYY-MM-DD format")
    if end_date and not validate_date(end_date):
        raise ValueError("end_date must be in YYYY-MM-DD format")

    if start_date:
        search_url = search_url + '&date_from=' + start_date
    if end_date:
        search_url = search_url + '&date_to=' + end_date

    result = query_api(search_url)

    return result

@mcp.tool()
def reindeer_search_index(query_term: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> list[dict]:
    """
    Query term search to a dataset containing the transcribed diaries and logs of reindeer administrators in the north 
    of Norway. The archive also contains material from the regional board, the earmarking committee, and the reindeer husbandry funds in Nordland. 
    The data covers the years from 1898 to 2003.

    Search queries should be provided in Norwegian only!

    Args:
        query_term: search term in Norwegian.
        start_date: search documents from this date onwards. The form is: YYYY-MM-DD
        end_date: search documents up to this date. The form is: YYYY-MM-DD

    Returns:
    A list of dictionaries containing the search results. 
    The data fields are:
    - 'text': Contains the transcribed text content (or part of it) of the document
    - 'sourceStartYear': Start year of the source collection
    - 'sourceEndYear': End year of the source collection
    - 'archiveName': Name of the archive that the document belongs to.
    - 'thumbnailUrl': Url to the digitized document
    """   
    base_url = "https://nye.digitalarkivet.no/api/media-file/search/transcription?archives[]=no-a1450-08000000280505&s="
    search_url = base_url + urllib.parse.quote(query_term)

    # Then in your functions:
    if start_date and not validate_date(start_date):
        raise ValueError("start_date must be in YYYY-MM-DD format")
    if end_date and not validate_date(end_date):
        raise ValueError("end_date must be in YYYY-MM-DD format")

    if start_date:
        search_url = search_url + '&date_from=' + start_date
    if end_date:
        search_url = search_url + '&date_to=' + end_date

    result = query_api(search_url)   
    return result

# Entry point to run the server
if __name__ == "__main__":
    mcp.run()
