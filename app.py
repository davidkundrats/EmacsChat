from flask import Flask, request, jsonify
from create_chatbot import create_chatbot

app = Flask(__name__)
chatbot = create_chatbot()
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    bot_response = chatbot.process_message(user_message)
    return jsonify({'response': bot_response})
if __name__ == '__main__':
    app.run(debug = True)
    
