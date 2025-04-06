from flask import Flask, request, render_template_string, redirect, url_for
import random
import sys

# Print Python information
print(f"Using Python: {sys.executable}")
print(f"Python version: {sys.version}")

app = Flask(__name__)

# Super simple HTML template with minimal JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Super Simple ML Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f7fa;
        }
        h1 {
            color: #4a6fa5;
            text-align: center;
        }
        .chat-container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 10px;
        }
        .user-message {
            background-color: #e3f2fd;
            margin-left: 20%;
            color: #0d47a1;
        }
        .bot-message {
            background-color: #f5f5f5;
            margin-right: 20%;
            color: #333;
        }
        form {
            display: flex;
            margin-top: 20px;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background-color: #4a6fa5;
            color: white;
            border: none;
            border-radius: 5px;
            margin-left: 10px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #166088;
        }
        .reset-button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #f44336;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 10px;
        }
        .reset-button:hover {
            background-color: #d32f2f;
        }
    </style>
</head>
<body>
    <h1>Super Simple ML Chatbot</h1>
    
    <div class="chat-container">
        {% for message in chat_history %}
            {% if message.type == 'user' %}
                <div class="message user-message">{{ message.content }}</div>
            {% else %}
                <div class="message bot-message">{{ message.content }}</div>
            {% endif %}
        {% endfor %}
        
        {% if not chat_history %}
            <div class="message bot-message">👋 Welcome! I'm your ML Chatbot. What would you like to know about machine learning?</div>
        {% endif %}
    </div>
    
    <form action="/send" method="post">
        <input type="text" name="message" placeholder="Type your message here..." required>
        <button type="submit">Send</button>
    </form>
    
    <a href="/reset" class="reset-button">Reset Conversation</a>
</body>
</html>
"""

# Store chat history in a global variable (for simplicity)
chat_history = []

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
    return render_template_string(HTML_TEMPLATE, chat_history=chat_history)

@app.route('/send', methods=['POST'])
def send():
    user_message = request.form.get('message', '').strip()
    
    if user_message:
        # Add user message to chat history
        chat_history.append({"type": "user", "content": user_message})
        
        # Get bot response
        bot_response = get_simple_response(user_message)
        
        # Add bot response to chat history
        chat_history.append({"type": "bot", "content": bot_response})
    
    return redirect(url_for('home'))

@app.route('/reset')
def reset():
    # Clear chat history
    chat_history.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    print("=" * 50)
    print("Starting Super Simple ML Chatbot")
    print("=" * 50)
    print("Server will be available at http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    except Exception as e:
        print(f"Error starting server: {e}") 