from chatbot import OAI_PC_Chatbot
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import Pinecone
from pinecone import Pinecone as Pc
from flask import jsonify

def create_chatbot(): 
    try: 
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key =os.environ.get('OPEN_AI_KEY'))
        model = ChatOpenAI(
            temperature= 0,
            openai_api_key=os.environ.get('OPEN_AI_KEY')
        )
        pc = Pc(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index("knowledge-base")
        vector_store = Pinecone(index, embeddings, text_key = "text")
        chatbot = OAI_PC_Chatbot(embeddings, model, vector_store)
        return chatbot
    except Exception as e: 
        print(f'An error occurred while initializing embeddings model and chat model: {e}')

