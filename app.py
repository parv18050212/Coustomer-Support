from flask import Flask, request, jsonify, render_template
from chatbot import ChatBot

# Initialize the chatbot
chatbot = ChatBot()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index_new.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    data = request.form.get('message')
    
    if data and data.strip():
        response = chatbot.get_response(data)
        return jsonify({"response": response})
    else:
        return jsonify({"error": "Please provide a message."}), 400

if __name__ == '__main__':
    app.run(debug=True)
