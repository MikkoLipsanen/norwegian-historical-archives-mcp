# MCP Server for the Norwegian Historical Archives Search API

This repository contains the code for a prototype MCP server for the Norwegian Historical Archives Search API (```https://nye.digitalarkivet.no/api/media-file/```).
developed during the 2025 Nordic Archives Hackathon in Oslo. 

## What the MCP server can be used for

The server contains two tools:
- ```search_index```: takes as input a query term and optional start and end dates, and performs a search to all the collections available via the api
- ```reindeer_search_index```: takes as input a query term and optional start and end dates, and performs a search specifically to the Reindriftsforvaltningen Nordland-collection

The server can be used to provide data for LLM, which performs the queries based on user questions. The server can be run locally using for instance Claude Desktop.

## Using the server with Claude Desktop

- Create Python virtual environment using for example Conda or UV
- Activate the virtual environment and install libraries listed in the ```requirements.txt``` file
- Add the server specification to Claude Desktop's configuration file. The specification should follow the general formula below: 

```
{
  "mcpServers": {
    "Norwegian Historical Archives Search Server": {
      "command": "/path/to/virtual/environment",
      "transport": "stdio",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "/path/to/norwegian_search_api_mcp.py"
      ]
    }
  }
}
```
- More detailed instructions can be found [here](https://modelcontextprotocol.io/docs/develop/connect-local-servers)
