from langchain_community.tools import tool
from tools.rag.retrieve import get_prod_details
from langchain_openai import ChatOpenAI
import sys
#sys.path.append("c:/personal/agent_and_rag_market_comparison_service")
import config
import asyncio

llm = ChatOpenAI(temperature=0, model_name = 'gpt-3.5-turbo', openai_api_key=config.secrets['OPENAI_API_KEY'])


@tool
async def compare_tool(comp_info : str) -> str:
    """
    Compare competitor shampoo info with our brand a brand using data from RAG.
    This tool:
    - Retrieves brand_a details from Pinecone via RAG
    - Compares ingredients, target segment, pricing, and eco-friendliness
    - Outputs a side-by-side comparison table and summary
    """

    brand_a_data = get_prod_details("brand_a shampoo full product details for competitive analysis")
    
    comparison_prompt = f"""
    You are a market research analyst. Compare these two shampoo brands across the following points:
    1. Ingredients & formulation
    2. Target customer segment
    3. Pricing & value positioning
    4. Eco-friendliness & sustainability claims
    5. Review sentiment

    Our Brand - brand_a:
    {brand_a_data}

    Competitor:
    {comp_info}

    Provide a concise but insightful side-by-side comparison table, followed by a summary paragraph.
    """

    res = await llm.apredict(comparison_prompt)
    return res
