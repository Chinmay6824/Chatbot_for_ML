from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import sys

# Add the parent directory to sys.path to import ml_filter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ml_filter.classifier import is_ml_related, get_ml_response
except ImportError as e:
    print(f"Error importing ml_filter: {e}")
    # Fallback functions if ml_filter is not available
    def is_ml_related(question):
        ml_keywords = ['machine learning', 'neural network', 'ai', 'ml', 'deep learning']
        return any(keyword in question.lower() for keyword in ml_keywords)
    
    def get_ml_response(question):
        return "This is a simplified response as the full ML filter module couldn't be loaded. In a complete implementation, I would provide detailed information about machine learning concepts."

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# HTML template for the chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ML Chatbot</title>
    <style>
        :root {
            --primary-color: #4a6fa5;
            --secondary-color: #166088;
            --background-color: #f5f7fa;
            --text-color: #333;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Segoe UI', sans-serif;
            line-height: 1.6;
            background-color: var(--background-color);
            color: var(--text-color);
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 1rem;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }
        
        .chat-container {
            background: white;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        
        #messages {
            height: 400px;
            overflow-y: auto;
            padding: 10px;
            margin-bottom: 20px;
        }
        
        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 8px;
            max-width: 80%;
        }
        
        .user-message {
            background-color: #e3f2fd;
            margin-left: auto;
        }
        
        .bot-message {
            background-color: #f5f5f5;
        }
        
        .not-ml-message {
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
        }
        
        .input-form {
            display: flex;
            gap: 10px;
        }
        
        #user-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        
        button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        
        button:hover {
            background-color: var(--secondary-color);
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 10px 0;
        }
        
        .loading.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ML Chatbot</h1>
            <p>Ask me anything about Machine Learning!</p>
        </header>
        
        <div class="chat-container">
            <div id="messages">
                <div class="message bot-message">
                    👋 Welcome! I'm specialized in answering questions about machine learning concepts and related topics. What would you like to know about machine learning today?
                </div>
            </div>
            
            <div class="loading" id="loading">
                Thinking...
            </div>
            
            <form class="input-form" id="chat-form">
                <input type="text" id="user-input" placeholder="Ask a machine learning question..." required>
                <button type="submit">Send</button>
            </form>
        </div>
    </div>

    <script>
        const messagesDiv = document.getElementById('messages');
        const chatForm = document.getElementById('chat-form');
        const userInput = document.getElementById('user-input');
        const loading = document.getElementById('loading');

        function scrollToBottom() {
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function addMessage(content, type) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}-message`;
            messageDiv.textContent = content;
            messagesDiv.appendChild(messageDiv);
            scrollToBottom();
        }

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = userInput.value.trim();
            if (!message) return;

            // Add user message
            addMessage(message, 'user');
            userInput.value = '';
            loading.classList.add('active');

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                });

                const data = await response.json();
                
                // Add bot response
                addMessage(
                    data.response,
                    data.is_ml_related ? 'bot' : 'not-ml'
                );
            } catch (error) {
                console.error('Error:', error);
                addMessage('Sorry, something went wrong. Please try again.', 'bot');
            } finally {
                loading.classList.remove('active');
            }
        });

        // Initial scroll to bottom
        scrollToBottom();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({
            'error': 'No message provided'
        }), 400
    
    # Check if the question is ML-related
    if is_ml_related(user_message):
        # Generate response for ML-related question
        response = get_ml_response(user_message)
        return jsonify({
            'is_ml_related': True,
            'response': response
        })
    else:
        # Return a polite message for non-ML questions
        return jsonify({
            'is_ml_related': False,
            'response': "I'm sorry, I can only answer questions related to machine learning. Please ask me something about ML concepts, algorithms, or applications."
        })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 