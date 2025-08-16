from langchain_community.tools import tool
from langchain_openai import ChatOpenAI
import sys
#sys.path.append("c:/personal/agent_and_rag_market_comparison_service")
import config
from tools.rag.retrieve import get_prod_details
import asyncio

llm = ChatOpenAI(temperature=0, model_name = 'gpt-3.5-turbo', openai_api_key=config.secrets['OPENAI_API_KEY'])

@tool
async def sentiment_tool(text: str) -> str:
    """Analyze the sentiment of user or competitor reviews."""
    prompt = f"What is the overall sentiment of the following text? Return Positive, Neutral, or Negative with 1-line reason.\n\n{text}"
    res = await llm.apredict(prompt)
    return res
