from flask import Flask, request, jsonify, render_template_string
import logging
import random
import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simple_server.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

# Simple HTML template for the chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Simple ML Chatbot</title>
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
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }
        
        .container {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            padding: 10px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 1rem;
            text-align: center;
            border-radius: 8px 8px 0 0;
            margin-bottom: 0;
            position: relative;
        }
        
        header h1 {
            font-size: 1.8rem;
            margin-bottom: 0.3rem;
        }
        
        header p {
            font-size: 1rem;
            opacity: 0.9;
        }
        
        .refresh-button {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .refresh-button svg {
            margin-right: 4px;
        }
        
        .refresh-button:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .chat-container {
            background: white;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 15px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        #messages {
            flex-grow: 1;
            overflow-y: auto;
            padding: 10px;
            margin-bottom: 15px;
            min-height: 300px;
            max-height: calc(100vh - 220px);
        }
        
        .message {
            margin-bottom: 15px;
            padding: 12px;
            border-radius: 18px;
            max-width: 85%;
            word-wrap: break-word;
            animation: fadeIn 0.3s ease-out;
            position: relative;
            line-height: 1.5;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-message {
            background-color: #e3f2fd;
            margin-left: auto;
            border-bottom-right-radius: 5px;
            color: #0d47a1;
        }
        
        .bot-message {
            background-color: #f5f5f5;
            margin-right: auto;
            border-bottom-left-radius: 5px;
            color: #333;
        }
        
        .error-message {
            background-color: #ffebee;
            border-left: 4px solid #f44336;
            color: #b71c1c;
        }
        
        .typing-indicator {
            display: none;
            margin-bottom: 15px;
            padding: 12px;
            border-radius: 18px;
            border-bottom-left-radius: 5px;
            background-color: #f5f5f5;
            max-width: 85%;
            margin-right: auto;
        }
        
        .typing-indicator span {
            height: 10px;
            width: 10px;
            float: left;
            margin: 0 1px;
            background-color: #9E9EA1;
            display: block;
            border-radius: 50%;
            opacity: 0.4;
        }
        
        .typing-indicator span:nth-of-type(1) {
            animation: 1s blink infinite 0.3333s;
        }
        
        .typing-indicator span:nth-of-type(2) {
            animation: 1s blink infinite 0.6666s;
        }
        
        .typing-indicator span:nth-of-type(3) {
            animation: 1s blink infinite 0.9999s;
        }
        
        @keyframes blink {
            50% { opacity: 1; }
        }
        
        .input-form {
            display: flex;
            gap: 10px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            margin-top: auto;
            position: sticky;
            bottom: 0;
            z-index: 10;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        }
        
        #user-input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 20px;
            font-size: 16px;
            transition: all 0.3s ease;
            background-color: white;
            color: var(--text-color);
            min-height: 24px;
            max-height: 120px;
            resize: none;
            overflow-y: auto;
        }
        
        #user-input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(74, 111, 165, 0.2);
        }
        
        #send-button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        
        #send-button:hover {
            background-color: var(--secondary-color);
        }
        
        #send-button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
            opacity: 0.7;
        }
        
        /* Mobile optimizations */
        @media (max-width: 768px) {
            .container {
                padding: 5px;
            }
            
            header {
                padding: 0.8rem;
            }
            
            header h1 {
                font-size: 1.5rem;
            }
            
            .chat-container {
                padding: 10px;
            }
            
            #messages {
                padding: 5px;
                min-height: 250px;
            }
            
            .message {
                padding: 10px;
                margin-bottom: 10px;
                max-width: 90%;
            }
            
            .input-form {
                padding: 8px;
            }
            
            #user-input {
                padding: 10px;
            }
            
            #send-button {
                width: 42px;
                height: 42px;
                padding: 10px;
            }
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            body {
                background-color: #121212;
                color: #e0e0e0;
            }
            
            .chat-container {
                background: #1e1e1e;
            }
            
            .bot-message {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            
            .user-message {
                background-color: #0d47a1;
                color: white;
            }
            
            .error-message {
                background-color: #3e2723;
                border-left: 4px solid #f44336;
                color: #ffcdd2;
            }
            
            .input-form {
                background: #2d2d2d;
            }
            
            #user-input {
                background: #1e1e1e;
                color: #e0e0e0;
                border-color: #424242;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Simple ML Chatbot</h1>
            <p>Your AI Assistant for Machine Learning Concepts</p>
            <button class="refresh-button" onclick="resetConversation()">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4C7.58 4 4.01 7.58 4.01 12C4.01 16.42 7.58 20 12 20C15.73 20 18.84 17.45 19.73 14H17.65C16.83 16.33 14.61 18 12 18C8.69 18 6 15.31 6 12C6 8.69 8.69 6 12 6C13.66 6 15.14 6.69 16.22 7.78L13 11H20V4L17.65 6.35Z" fill="white"/>
                </svg>
                Reset Chat
            </button>
        </header>
        
        <div class="chat-container">
            <div id="messages">
                <div class="message bot-message">
                    👋 Welcome! I'm your Simple ML Chatbot, specialized in answering questions about machine learning concepts and related topics. What would you like to know about machine learning today?
                </div>
            </div>
            
            <div class="typing-indicator" id="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
            
            <form class="input-form" id="chat-form">
                <textarea id="user-input" placeholder="Ask a machine learning question..." rows="1" autocomplete="off"></textarea>
                <button type="submit" id="send-button">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" fill="white"/>
                    </svg>
                </button>
            </form>
        </div>
    </div>

    <script>
        // Initialize variables
        const messagesDiv = document.getElementById('messages');
        const chatForm = document.getElementById('chat-form');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        const typingIndicator = document.getElementById('typing-indicator');
        let chatHistory = [];
        
        // Focus the input field when the page loads
        window.addEventListener('load', () => {
            userInput.focus();
        });
        
        // Auto-resize textarea as user types
        userInput.addEventListener('input', () => {
            // Reset height to auto to get the correct scrollHeight
            userInput.style.height = 'auto';
            // Set the height to match content (with a max height)
            userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
            
            // Enable/disable send button based on content
            sendButton.disabled = userInput.value.trim() === '';
        });
        
        // Handle Enter key (send message) and Shift+Enter (new line)
        userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (userInput.value.trim() !== '') {
                    chatForm.dispatchEvent(new Event('submit'));
                }
            }
        });

        function scrollToBottom() {
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function addMessage(content, type) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}-message`;
            messageDiv.textContent = content;
            messagesDiv.appendChild(messageDiv);
            scrollToBottom();
            
            // Add to chat history
            chatHistory.push({
                content: content,
                type: type
            });
            
            // Save chat history to local storage
            localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        }

        function showTypingIndicator() {
            typingIndicator.style.display = 'block';
            scrollToBottom();
        }

        function hideTypingIndicator() {
            typingIndicator.style.display = 'none';
        }
        
        function resetConversation() {
            // Clear chat history
            chatHistory = [];
            localStorage.removeItem('chatHistory');
            
            // Clear messages
            messagesDiv.innerHTML = '';
            
            // Add welcome message
            const welcomeMessage = document.createElement('div');
            welcomeMessage.className = 'message bot-message';
            welcomeMessage.textContent = '👋 Welcome! I\'m your Simple ML Chatbot, specialized in answering questions about machine learning concepts and related topics. What would you like to know about machine learning today?';
            messagesDiv.appendChild(welcomeMessage);
            
            // Reset conversation on server
            fetch('/api/reset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            // Focus on input
            userInput.focus();
        }

        // Load chat history from local storage
        function loadChatHistory() {
            const savedHistory = localStorage.getItem('chatHistory');
            if (savedHistory) {
                try {
                    chatHistory = JSON.parse(savedHistory);
                    
                    // Clear the welcome message
                    messagesDiv.innerHTML = '';
                    
                    // Restore messages
                    chatHistory.forEach(msg => {
                        const messageDiv = document.createElement('div');
                        messageDiv.className = `message ${msg.type}-message`;
                        messageDiv.textContent = msg.content;
                        messagesDiv.appendChild(messageDiv);
                    });
                    
                    scrollToBottom();
                } catch (e) {
                    console.error('Error loading chat history:', e);
                    // Reset if there's an error
                    chatHistory = [];
                }
            }
        }

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = userInput.value.trim();
            if (!message) return;

            // Add user message
            addMessage(message, 'user');
            
            // Clear and reset input
            userInput.value = '';
            userInput.style.height = 'auto';
            sendButton.disabled = true;
            
            // Show typing indicator
            showTypingIndicator();
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        message: message
                    }),
                });

                if (!response.ok) {
                    throw new Error(`Server responded with status: ${response.status}`);
                }

                const data = await response.json();
                
                // Hide typing indicator
                hideTypingIndicator();
                
                // Add bot response
                addMessage(data.response, 'bot');
                
            } catch (error) {
                console.error('Error:', error);
                hideTypingIndicator();
                addMessage('Sorry, something went wrong. Please try again.', 'error');
            }
            
            // Focus back on the input field
            userInput.focus();
        });

        // Initial load
        document.addEventListener('DOMContentLoaded', () => {
            loadChatHistory();
            scrollToBottom();
        });
    </script>
</body>
</html>
"""

# Simple ML responses
ML_RESPONSES = {
    "default": [
        "Machine learning is a field of artificial intelligence that uses statistical techniques to give computer systems the ability to 'learn' from data.",
        "In machine learning, we train models on data to make predictions or decisions without being explicitly programmed to perform the task.",
        "I'd be happy to explain more about specific machine learning concepts. Could you provide more details about what you'd like to know?",
        "That's an interesting question about machine learning. Let me provide some information that might help.",
        "Machine learning algorithms can be categorized into supervised learning, unsupervised learning, and reinforcement learning."
    ],
    "neural_networks": [
        "Neural networks are computing systems inspired by the biological neural networks in animal brains. They consist of artificial neurons that can learn from and make decisions based on data.",
        "Deep learning is a subset of machine learning that uses neural networks with many layers (deep neural networks) to analyze various factors of data.",
        "Convolutional Neural Networks (CNNs) are particularly effective for image processing tasks, while Recurrent Neural Networks (RNNs) work well with sequential data like text or time series."
    ],
    "algorithms": [
        "Common machine learning algorithms include linear regression, logistic regression, decision trees, random forests, and support vector machines.",
        "K-means clustering is an unsupervised learning algorithm used to identify clusters of data based on similarity.",
        "Gradient boosting algorithms like XGBoost and LightGBM are very popular in competitions and real-world applications due to their performance."
    ],
    "evaluation": [
        "Common metrics for evaluating machine learning models include accuracy, precision, recall, F1 score, and area under the ROC curve (AUC).",
        "Cross-validation is a technique used to assess how the results of a statistical analysis will generalize to an independent data set.",
        "The confusion matrix provides a detailed breakdown of correct and incorrect classifications for each class in classification problems."
    ]
}

def get_simple_response(message):
    """Generate a simple response based on the user's message."""
    message = message.lower()
    
    # Check for keywords to determine category
    if any(word in message for word in ["neural", "network", "deep", "cnn", "rnn", "lstm"]):
        responses = ML_RESPONSES["neural_networks"]
    elif any(word in message for word in ["algorithm", "regression", "tree", "forest", "svm", "cluster"]):
        responses = ML_RESPONSES["algorithms"]
    elif any(word in message for word in ["accuracy", "precision", "recall", "f1", "auc", "evaluate", "metric"]):
        responses = ML_RESPONSES["evaluation"]
    else:
        responses = ML_RESPONSES["default"]
    
    # Return a random response from the selected category
    return random.choice(responses)

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
    
    try:
        # Simulate processing time
        import time
        time.sleep(1)
        
        # Get a simple response
        response = get_simple_response(user_message)
        
        # Log the interaction
        logging.info(f"User: {user_message}")
        logging.info(f"Bot: {response[:100]}...")
        
        return jsonify({
            'response': response
        })
        
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'An error occurred while processing your message',
            'details': str(e)
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset():
    return jsonify({
        'response': 'Conversation has been reset.'
    })

if __name__ == "__main__":
    print("Starting Simple ML Chatbot server on http://localhost:5000")
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    except Exception as e:
        print(f"Error starting server: {e}") 