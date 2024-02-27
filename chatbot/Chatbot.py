from abc import ABC, abstractmethod

class Chatbot():
    """ The abstract class providing the template for the chatbot:all instances of a chatbot must implement this class """
    def __init__(self, embeddings, model, vector_store):
        self.embeddings = embeddings
        self.model = model
        self.vector_store = vector_store
    @abstractmethod
    def generate_prompt(self, query):
        #Abstract class to generate prompt. Should be implemented by subclass
        pass
    @abstractmethod
    def process_message(self, message):
        #Abstract class to generate prompt. Should be implemented by subclass
        pass
