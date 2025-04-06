from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import re
import random

app = Flask(__name__)
CORS(app)

# ML-related keywords for simple keyword matching
ML_KEYWORDS = {
    'machine learning', 'deep learning', 'neural network', 'artificial intelligence', 'ai', 'ml',
    'supervised learning', 'unsupervised learning', 'reinforcement learning', 'classification',
    'regression', 'clustering', 'decision tree', 'random forest', 'gradient boosting',
    'support vector machine', 'svm', 'k-means', 'knn', 'naive bayes', 'logistic regression',
    'backpropagation', 'cnn', 'rnn', 'lstm', 'gan', 'transformer', 'bert', 'gpt'
}

# Predefined responses for ML topics
RESPONSES = {
    'machine learning': "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
    'deep learning': "Deep learning is a subset of machine learning that uses neural networks with multiple layers to analyze various factors of data.",
    'neural network': "Neural networks are computing systems inspired by biological neural networks, consisting of interconnected nodes (neurons) that process and transmit information.",
    'supervised learning': "Supervised learning is where the model learns from labeled training data to make predictions or classifications on new, unseen data.",
    'unsupervised learning': "Unsupervised learning involves finding patterns and structures in unlabeled data without explicit guidance.",
    'reinforcement learning': "Reinforcement learning is where an agent learns to make decisions by interacting with an environment and receiving rewards or penalties.",
    'classification': "Classification is a supervised learning task where the model learns to categorize input data into predefined classes.",
    'regression': "Regression is a supervised learning task where the model predicts continuous numerical values based on input features.",
    'clustering': "Clustering is an unsupervised learning technique that groups similar data points together based on their characteristics.",
    'decision tree': "A decision tree is a tree-like model that makes decisions based on asking a series of questions about the input features.",
    'random forest': "Random forest is an ensemble learning method that combines multiple decision trees to make more accurate predictions.",
    'gradient boosting': "Gradient boosting is a machine learning technique that creates a strong predictor by combining multiple weak predictors sequentially.",
    'artificial intelligence': "Artificial Intelligence (AI) is the simulation of human intelligence by machines, encompassing machine learning and other approaches.",
    'overfitting': "Overfitting occurs when a model learns the training data too well, including noise, leading to poor performance on new data.",
    'underfitting': "Underfitting happens when a model is too simple to capture the underlying patterns in the data.",
    'cross validation': "Cross validation is a technique to assess how well a model will generalize to new, unseen data by testing it on multiple data subsets.",
    'feature extraction': "Feature extraction is the process of selecting or creating relevant features from raw data to improve model performance.",
    'hyperparameter': "Hyperparameters are configuration settings used to control the learning process, such as learning rate or number of hidden layers.",
    'bias variance': "The bias-variance tradeoff is a fundamental concept in machine learning that deals with model complexity and generalization.",
    'tensorflow': "TensorFlow is a popular open-source machine learning framework developed by Google.",
    'pytorch': "PyTorch is a machine learning framework known for its dynamic computational graphs and ease of use.",
    'keras': "Keras is a high-level neural network library that runs on top of TensorFlow, known for its user-friendliness.",
    'scikit learn': "Scikit-learn is a popular machine learning library in Python that provides simple and efficient tools for data analysis and modeling."
}

# Add these new dictionaries after ML_KEYWORDS
GREETINGS = {
    'hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'howdy'
}

GREETING_RESPONSES = [
    "👋 Hi there! I'm your ML Chatbot. What would you like to know about machine learning?",
    "Hello! I'm excited to help you learn about machine learning. What's on your mind?",
    "Hey! Ready to explore some machine learning concepts together?",
    "Hi! I'm here to help with all your machine learning questions. What would you like to know?"
]

FAREWELLS = {
    'bye', 'goodbye', 'see you', 'farewell', 'good night', 'thanks', 'thank you'
}

FAREWELL_RESPONSES = [
    "Goodbye! Feel free to come back if you have more questions about machine learning!",
    "Thanks for chatting! Don't hesitate to return when you want to learn more about ML!",
    "See you later! Remember, I'm always here to help with machine learning concepts!",
    "Bye! Looking forward to our next discussion about machine learning!"
]

ENCOURAGEMENTS = [
    "That's a great question about machine learning!",
    "I'm glad you're interested in learning about ML!",
    "Excellent question! Let me help you understand this ML concept.",
    "I'd be happy to explain this machine learning topic!"
]

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
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 1.5rem;
            text-align: center;
            border-radius: 8px 8px 0 0;
            margin-bottom: 0;
        }
        
        .chat-container {
            background: white;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        #messages {
            flex-grow: 1;
            overflow-y: auto;
            padding: 10px;
            margin-bottom: 20px;
            min-height: 400px;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 12px;
            border-radius: 8px;
            max-width: 85%;
            animation: fadeIn 0.3s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-message {
            background-color: #e3f2fd;
            margin-left: auto;
            border-bottom-right-radius: 2px;
        }
        
        .bot-message {
            background-color: #f5f5f5;
            margin-right: auto;
            border-bottom-left-radius: 2px;
        }
        
        .not-ml-message {
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
        }
        
        .input-form {
            display: flex;
            gap: 10px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            margin-top: auto;
        }
        
        #user-input {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        #user-input:focus {
            outline: none;
            border-color: var(--primary-color);
        }
        
        button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        button:hover {
            background-color: var(--secondary-color);
        }
        
        button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        
        .suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }
        
        .suggestion-chip {
            background-color: #e3f2fd;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .suggestion-chip:hover {
            background-color: #bbdefb;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ML Chatbot</h1>
            <p>Your AI Assistant for Machine Learning Concepts</p>
        </header>
        
        <div class="chat-container">
            <div id="messages">
                <div class="message bot-message">
                    👋 Welcome! I'm your ML Chatbot, specialized in answering questions about machine learning concepts and related topics. What would you like to know about machine learning today?
                </div>
            </div>
            
            <div class="suggestions">
                <div class="suggestion-chip" onclick="askQuestion('What is machine learning?')">What is machine learning?</div>
                <div class="suggestion-chip" onclick="askQuestion('Explain neural networks')">Neural Networks</div>
                <div class="suggestion-chip" onclick="askQuestion('What is deep learning?')">Deep Learning</div>
                <div class="suggestion-chip" onclick="askQuestion('Supervised vs Unsupervised learning')">Supervised vs Unsupervised</div>
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

        function askQuestion(question) {
            userInput.value = question;
            chatForm.dispatchEvent(new Event('submit'));
        }

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = userInput.value.trim();
            if (!message) return;

            // Add user message
            addMessage(message, 'user');
            userInput.value = '';

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
            }
        });

        // Initial scroll to bottom
        scrollToBottom();
    </script>
</body>
</html>
"""

def is_ml_related(question):
    """Check if the question is related to machine learning"""
    question = question.lower()
    # Check for exact matches in responses first
    for key in RESPONSES:
        if key in question:
            return True
    # Then check for keyword matches
    return any(keyword in question for keyword in ML_KEYWORDS)

def get_ml_response(question):
    """Generate a response for an ML-related question"""
    question = question.lower()
    
    # Check for exact matches in responses
    for key, response in RESPONSES.items():
        if key in question:
            return response
    
    # If no exact match, provide a general response
    return ("I understand you're asking about machine learning. While I don't have a specific "
            "answer for this question, I can help with many ML concepts like neural networks, "
            "supervised learning, deep learning, and more. Feel free to ask about these topics!")

def is_greeting(message):
    """Check if the message is a greeting"""
    return any(greeting in message.lower() for greeting in GREETINGS)

def is_farewell(message):
    """Check if the message is a farewell"""
    return any(farewell in message.lower() for farewell in FAREWELLS)

def get_greeting_response():
    """Get a random greeting response"""
    return random.choice(GREETING_RESPONSES)

def get_farewell_response():
    """Get a random farewell response"""
    return random.choice(FAREWELL_RESPONSES)

def get_encouragement():
    """Get a random encouragement response"""
    return random.choice(ENCOURAGEMENTS)

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
    
    # Check for greetings
    if is_greeting(user_message):
        return jsonify({
            'is_ml_related': True,
            'response': get_greeting_response()
        })
    
    # Check for farewells
    if is_farewell(user_message):
        return jsonify({
            'is_ml_related': True,
            'response': get_farewell_response()
        })
    
    # Check if the question is ML-related
    if is_ml_related(user_message):
        # Generate response for ML-related question
        response = get_ml_response(user_message)
        # Add an encouragement before the response
        if len(user_message.split()) > 3:  # Only add encouragement for longer questions
            response = f"{get_encouragement()} {response}"
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

if __name__ == '__main__':
    app.run(debug=True) 