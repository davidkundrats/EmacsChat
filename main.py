import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import Pinecone
from pinecone import Pinecone as Pc


load_dotenv()

try: 
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key =os.environ.get('OPEN_AI_KEY'))
    model = ChatOpenAI(
        temperature= 0,
        openai_api_key=os.environ.get('OPEN_AI_KEY')
    )
    pc = Pc(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index("knowledge-base")
    vector_store = Pinecone(index, embeddings, text_key = "text")
except Exception as e: 
    print(f'An error occurred while initializing embeddings model and chat model: {e}')

#prompt
def generate_prompt(query): 
    results = vector_store.similarity_search(query, k=5)
    knowledge = "/n".join(doc.page_content for doc in results)
    prompt = f""" Use only this context given to you to answer the question. If you cannot answer the query using the knowledge base, clearly state so and end your answer. 

    Knowledge: {knowledge}

    Query: {query}
    """
    return prompt
#process message from app
def process_message(message):
    while True:
        query = message
        if query.lower() == 'exit':
            print('Chat: Goodbye!')
            break
        try:
            augmented_prompt = generate_prompt(query)
            response = model.invoke(augmented_prompt)
            return(f"Chat: {response.content}")
        except Exception as e:
            print(f"An error occurred while generating a response: {e}")
