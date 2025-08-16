from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import tool
import sys
sys.path.append("c:/personal/agent_and_rag_market_comparison_service")
import config
import asyncio

search = TavilySearchResults(max_results=5, tavily_api_key = config.secrets['TAVILY_API_KEY'])

@tool
async def crawl_web(query:str) -> str:
    # search latest competitor info based on query using Tavily
    """
    Search and scrape the latest competitor information from the web using Tavily.
    Takes a search query string and returns combined text content from the top search results.
    """
    results = await search.arun(query)
    #print(results)
    query_result = '\n\n'.join([x['content'] for x in results])
    return query_result

