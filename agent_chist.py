import asyncio
import time
import sys
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import initialize_agent, AgentType
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory 

from langchain_community.chat_message_histories import ChatMessageHistory 
from langchain.schema import HumanMessage, AIMessage

import config

# Assuming these are your async tools defined in their respective files
from tools.tavily_search_tool import crawl_web
from tools.rag.retrieve import get_prod_details 
from tools.sentiment_tool import sentiment_tool
from tools.compare_tool import compare_tool


# --- In-Memory Chat History Store ---
# This dictionary will hold ChatMessageHistory objects, keyed by session_id
chat_history_store = {}

def get_in_memory_chat_history(session_id: str) -> ChatMessageHistory:
    # """
    # Returns an InMemoryChatMessageHistory instance for the given session_id.
    # Creates a new one if the session_id is not found.
    # """
    # if session_id not in chat_history_store:
    #     chat_history_store[session_id] = ChatMessageHistory()
    # return chat_history_store[session_id]
    if session_id not in chat_history_store:
        print(f"Creating new history for session_id: {session_id}")
        chat_history_store[session_id] = ChatMessageHistory()
    else:
        print(f"Retrieving existing history for session_id: {session_id}")

    # You can inspect the history here:
    current_history = chat_history_store[session_id]
    print(f"History for {session_id}: {current_history.messages}") 

    return current_history

embedding_model = OpenAIEmbeddings(openai_api_key = config.secrets['OPENAI_API_KEY']) # Still needed for embedding if using RAG

llm = ChatOpenAI(temperature=0, model_name = 'gpt-3.5-turbo', openai_api_key=config.secrets['OPENAI_API_KEY'])

tools = [crawl_web, sentiment_tool, compare_tool] 

# --- Agent and Chain Setup --- 
base_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

chain_with_history = RunnableWithMessageHistory(
    base_agent,
    # Use the in-memory history function
    get_in_memory_chat_history, 
    input_messages_key="input",  
    history_messages_key="chat_history"  
)

async def run_agent_task(prompt: str, session_id: str) -> str:
    """
    Run the agent query asynchronously with in-memory chat history.
    Uses the provided session_id to manage distinct user histories.
    """
    try:
        config = {"configurable": {"session_id": session_id}} # Pass session_id in config
        res = await chain_with_history.ainvoke({"input": prompt}, config=config)
        return res['output']
    except Exception as e:
        print(f"Error running agent task: {e}")
        return f"An error occurred: {e}"

