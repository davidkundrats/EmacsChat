from ..Chatbot import Chatbot
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import Pinecone
from pinecone import Pinecone as Pc


class OAI_PC_Chatbot(Chatbot):
    """ Chatbot that uses OpenAI's model and Pinecone's similarity search to answer questions. """
    def __init__(self, embeddings, model, vector_store):
        super().__init__(embeddings, model, vector_store)
    def generate_prompt(self,query): 
        results = self.vector_store.similarity_search(query, k=5)
        knowledge = "/n".join(doc.page_content for doc in results)
        prompt = f""" Use only this context given to you to answer the question. If you cannot answer the query using the knowledge base, clearly state so and end your answer. 

        Knowledge: {knowledge}

        Query: {query}
        """
        return prompt
    def process_message(self, message):
        while True:
            query = message
            if query.lower() == 'exit':
                print('Chat: Goodbye!')
                break
            try:
                augmented_prompt = self.generate_prompt(query)
                response = self.model.invoke(augmented_prompt)
                return(f"Chat: {response.content}")
            except Exception as e:
                print(f"An error occurred while generating a response: {e}")
