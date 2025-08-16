from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter
import os 
from pinecone import Pinecone
import sys
sys.path.append("c:/personal/agent_and_rag_market_comparison_service")
import config

os.environ["PINECONE_API_KEY"] = ""


file_path = 'c:/personal/agent_and_rag_market_comparison_service/data/brand_a.txt'
loader = TextLoader(file_path=file_path, encoding='utf-8')

if __name__ == '__main__':
    loader = TextLoader(file_path=file_path, encoding='utf-8')
    document = loader.load()

    print("...splitting")
    splitter = CharacterTextSplitter(chunk_size = 200, chunk_overlap = 0)
    texts = splitter.split_documents(documents=document)
    print(f"created {len(texts)} chunks")

    print("...injesting")
    embedding_model = OpenAIEmbeddings(openai_api_key = config.secrets['OPENAI_API_KEY'])
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"], environment="us-east-1-aws")
    index = config.secrets['PINECONE_INDEX_NAME']

    docsearch = PineconeVectorStore.from_documents(texts,embedding_model, index_name=index)

    print("finish")   


    
