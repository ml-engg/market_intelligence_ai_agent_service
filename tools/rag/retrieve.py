from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter
import os 
from pinecone import Pinecone
#import sys
#sys.path.append("c:/personal/agent_and_rag_market_comparison_service")
import config

os.environ["PINECONE_API_KEY"] = ""

QUERY_TEMPLATE = """
You are retrieving brand_a shampoo product knowledge for competitive analysis.
Focus only on facts, not opinions.
Include: formulation details, ingredients, certifications, packaging, sustainability practices, and review highlights.
Query: {user_query}
"""

    
def get_prod_details(query : str) -> str:
    embedding_model = OpenAIEmbeddings(openai_api_key = config.secrets['OPENAI_API_KEY'])
    vector_store = PineconeVectorStore(index_name=config.secrets['PINECONE_INDEX_NAME'], embedding=embedding_model)
    final_query = QUERY_TEMPLATE.format(user_query=query)
    results = vector_store.similarity_search(final_query,k = 3)

    return "\n".join([doc.page_content for doc in results])

