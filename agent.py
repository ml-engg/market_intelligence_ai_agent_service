from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
import config
from tools.tavily_search_tool import crawl_web
from tools.rag.retrieve import get_prod_details
from tools.sentiment_tool import sentiment_tool
from tools.compare_tool import compare_tool
from tools.tavily_search_tool import crawl_web
import asyncio

llm = ChatOpenAI(temperature=0, model_name = 'gpt-3.5-turbo', openai_api_key=config.secrets['OPENAI_API_KEY'])

tools = [crawl_web, sentiment_tool, compare_tool]

# Use ReAct agent in sync mode
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

async def run_agent_task(task: str):
    """Run the agent query synchronously."""
    return await agent.arun(task)


