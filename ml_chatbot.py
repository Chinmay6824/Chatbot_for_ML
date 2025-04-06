import flask
from flask import Flask, request, jsonify, render_template_string
import re
import random

app = Flask(__name__)

# Dictionary of machine learning concepts and their explanations
ml_knowledge = {
    "machine learning": "Machine learning is a field of artificial intelligence that uses statistical techniques to give computer systems the ability to 'learn' from data without being explicitly programmed.",
    "supervised learning": "Supervised learning is a type of machine learning where the algorithm learns from labeled training data, and makes predictions based on that data.",
    "unsupervised learning": "Unsupervised learning is a type of machine learning where the algorithm learns patterns from unlabeled data.",
    "reinforcement learning": "Reinforcement learning is a type of machine learning where the algorithm learns by interacting with an environment and receiving rewards or penalties.",
    "neural network": "Neural networks are computing systems inspired by the biological neural networks in animal brains. They consist of artificial neurons that can learn from and make decisions based on data.",
    "deep learning": "Deep learning is a subset of machine learning that uses neural networks with multiple layers (deep neural networks) to analyze various factors of data.",
    "cnn": "Convolutional Neural Networks (CNNs) are a class of deep neural networks most commonly applied to analyzing visual imagery. They use a mathematical operation called convolution in place of general matrix multiplication in at least one of their layers.",
    "rnn": "Recurrent Neural Networks (RNNs) are a class of neural networks where connections between nodes form a directed graph along a temporal sequence. This allows it to exhibit temporal dynamic behavior.",
    "lstm": "Long Short-Term Memory (LSTM) networks are a type of RNN that can learn order dependence in sequence prediction problems. They have feedback connections, unlike standard feedforward neural networks.",
    "gan": "Generative Adversarial Networks (GANs) are a class of machine learning frameworks where two neural networks contest with each other in a zero-sum game. They can generate new data with the same statistics as the training set.",
    "decision tree": "A decision tree is a flowchart-like structure in which each internal node represents a test on a feature, each branch represents the outcome of the test, and each leaf node represents a class label.",
    "random forest": "Random Forest is an ensemble learning method that operates by constructing multiple decision trees during training and outputting the class that is the mode of the classes of the individual trees.",
    "svm": "Support Vector Machine (SVM) is a supervised learning model that analyzes data for classification and regression. It uses a technique called the kernel trick to transform data and then finds an optimal boundary between outputs.",
    "knn": "K-Nearest Neighbors (KNN) is a simple, instance-based learning algorithm that stores all available cases and classifies new cases based on a similarity measure.",
    "clustering": "Clustering is a technique used in unsupervised learning to group similar data points together. Popular algorithms include K-means, hierarchical clustering, and DBSCAN.",
    "pca": "Principal Component Analysis (PCA) is a statistical procedure that uses an orthogonal transformation to convert a set of observations into a set of linearly uncorrelated variables called principal components.",
    "accuracy": "Accuracy is a metric for evaluating classification models. It's the ratio of correct predictions to total predictions made.",
    "precision": "Precision is a metric that quantifies the number of correct positive predictions made. It's calculated as the ratio of true positives to the sum of true and false positives.",
    "recall": "Recall (also known as sensitivity) is a metric that quantifies the number of correct positive predictions made out of all positive predictions that could have been made. It's calculated as the ratio of true positives to the sum of true positives and false negatives.",
    "f1 score": "F1 Score is the harmonic mean of precision and recall. It's a good metric when you need to balance both precision and recall.",
    "overfitting": "Overfitting occurs when a model learns the training data too well, including its noise and outliers, and performs poorly on unseen data.",
    "underfitting": "Underfitting occurs when a model is too simple to capture the underlying pattern of the data, resulting in poor performance on both training and unseen data.",
    "cross-validation": "Cross-validation is a resampling procedure used to evaluate machine learning models on a limited data sample. The most common method is k-fold cross-validation.",
    "gradient descent": "Gradient descent is an optimization algorithm used to minimize some function by iteratively moving in the direction of steepest descent as defined by the negative of the gradient.",
    "batch normalization": "Batch normalization is a technique for improving the performance and stability of neural networks by normalizing the inputs of each layer.",
    "dropout": "Dropout is a regularization technique where randomly selected neurons are ignored during training. This helps prevent overfitting.",
    "bias-variance tradeoff": "The bias-variance tradeoff is the property of a set of predictive models whereby models with lower bias have higher variance and vice versa.",
    "bagging": "Bagging (Bootstrap Aggregating) is an ensemble technique that combines the predictions of multiple models to improve accuracy and control overfitting.",
    "boosting": "Boosting is an ensemble technique that combines a set of weak learners into a strong learner to minimize training errors.",
    "xgboost": "XGBoost is an implementation of gradient boosted decision trees designed for speed and performance. It's highly efficient, flexible, and portable.",
    "regularization": "Regularization is a technique used to prevent overfitting by adding a penalty term to the loss function, discouraging complex models.",
    "hyperparameter": "Hyperparameters are parameters whose values are set before the learning process begins. They can't be learned directly from the training process.",
    "feature engineering": "Feature engineering is the process of using domain knowledge to extract features from raw data that make machine learning algorithms work better.",
    "feature selection": "Feature selection is the process of selecting a subset of relevant features for use in model construction.",
    "one-hot encoding": "One-hot encoding is a process of converting categorical variables into a form that could be provided to machine learning algorithms to improve predictions.",
    "transformer": "Transformer is a deep learning model that adopts the mechanism of self-attention, differentially weighting the significance of each part of the input data. It's primarily used in NLP and computer vision tasks.",
    "bert": "BERT (Bidirectional Encoder Representations from Transformers) is a transformer-based machine learning technique for natural language processing pre-training developed by Google.",
    "gpt": "GPT (Generative Pre-trained Transformer) is an autoregressive language model that uses deep learning to produce human-like text, developed by OpenAI."
}

# Function to find the best match for a query
def find_best_match(query):
    query = query.lower()
    
    # Direct match
    for key in ml_knowledge:
        if key in query:
            return key
    
    # Check for questions about definitions or explanations
    match = re.search(r"what (is|are) (a |an )?([\w\s]+)(\?)?", query)
    if match:
        term = match.group(3).strip().lower()
        for key in ml_knowledge:
            if key == term or key in term:
                return key
    
    # If no match found
    return None

# Responses for when we don't have a specific answer
fallback_responses = [
    "I'm not sure about that. Could you ask me about a specific machine learning concept?",
    "I don't have information on that topic. I can answer questions about machine learning concepts like neural networks, supervised learning, etc.",
    "I'm specialized in machine learning topics. Try asking about algorithms, neural networks, or evaluation metrics.",
    "I don't have enough information to answer that question. Could you ask something about machine learning specifically?"
]

@app.route('/')
def home():
    # HTML template for the chatbot interface
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ML Chatbot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
                display: flex;
                flex-direction: column;
                height: 100vh;
            }
            
            .header {
                background-color: #4285f4;
                color: white;
                text-align: center;
                padding: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            .chat-container {
                flex: 1;
                max-width: 800px;
                margin: 0 auto;
                width: 100%;
                background-color: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                border-radius: 8px;
                margin-top: 20px;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .chat-box {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
            }
            
            .message {
                margin-bottom: 15px;
                padding: 10px 15px;
                border-radius: 5px;
                max-width: 80%;
                word-wrap: break-word;
            }
            
            .user-message {
                background-color: #e2f2ff;
                margin-left: auto;
                border-top-right-radius: 0;
            }
            
            .bot-message {
                background-color: #f0f0f0;
                margin-right: auto;
                border-top-left-radius: 0;
            }
            
            .input-container {
                display: flex;
                padding: 10px;
                border-top: 1px solid #ddd;
                background-color: white;
            }
            
            #user-input {
                flex: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                resize: none;
                height: 20px;
                max-height: 80px;
                overflow-y: auto;
            }
            
            #send-button {
                padding: 10px 20px;
                background-color: #4285f4;
                color: white;
                border: none;
                border-radius: 4px;
                margin-left: 10px;
                cursor: pointer;
                font-size: 14px;
            }
            
            #send-button:hover {
                background-color: #3367d6;
            }
            
            #send-button:disabled {
                background-color: #cccccc;
                cursor: not-allowed;
            }
            
            @media (max-width: 600px) {
                .chat-container {
                    margin: 10px;
                    width: auto;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Machine Learning Chatbot</h1>
            <p>Ask me questions about machine learning concepts!</p>
        </div>
        
        <div class="chat-container">
            <div class="chat-box" id="chat-box">
                <div class="message bot-message">
                    Hi there! I'm your ML assistant. Ask me about machine learning concepts like neural networks, supervised learning, or algorithms.
                </div>
            </div>
            
            <div class="input-container">
                <textarea id="user-input" placeholder="Type your question here..." rows="1"></textarea>
                <button id="send-button" onclick="sendMessage()">Send</button>
            </div>
        </div>
        
        <script>
            const chatBox = document.getElementById('chat-box');
            const userInput = document.getElementById('user-input');
            const sendButton = document.getElementById('send-button');
            
            // Auto-resize textarea as user types
            userInput.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
                
                // Enable/disable send button based on input
                if (this.value.trim() === '') {
                    sendButton.disabled = true;
                } else {
                    sendButton.disabled = false;
                }
            });
            
            // Initial state of send button
            sendButton.disabled = true;
            
            // Handle Enter key press
            userInput.addEventListener('keydown', function(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    if (!sendButton.disabled) {
                        sendMessage();
                    }
                }
            });
            
            // Send message function
            function sendMessage() {
                const message = userInput.value.trim();
                if (message === '') return;
                
                // Add user message to chat
                appendMessage(message, 'user');
                
                // Clear input and reset height
                userInput.value = '';
                userInput.style.height = 'auto';
                sendButton.disabled = true;
                
                // Show typing indicator
                const typingIndicator = document.createElement('div');
                typingIndicator.className = 'message bot-message';
                typingIndicator.id = 'typing-indicator';
                typingIndicator.textContent = 'Typing...';
                chatBox.appendChild(typingIndicator);
                chatBox.scrollTop = chatBox.scrollHeight;
                
                // Get response from server
                fetch('/get_response', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({query: message})
                })
                .then(response => response.json())
                .then(data => {
                    // Remove typing indicator
                    const indicator = document.getElementById('typing-indicator');
                    if (indicator) {
                        chatBox.removeChild(indicator);
                    }
                    
                    // Add bot response
                    appendMessage(data.response, 'bot');
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Remove typing indicator
                    const indicator = document.getElementById('typing-indicator');
                    if (indicator) {
                        chatBox.removeChild(indicator);
                    }
                    
                    // Add error message
                    appendMessage('Sorry, there was an error processing your request.', 'bot');
                });
            }
            
            // Function to append a message to the chat
            function appendMessage(text, sender) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                messageDiv.textContent = text;
                chatBox.appendChild(messageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            
            // Focus input on page load
            window.onload = function() {
                userInput.focus();
            };
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    query = data.get('query', '')
    
    # Find the best match for the query
    match = find_best_match(query)
    
    if match:
        response = ml_knowledge[match]
    else:
        response = random.choice(fallback_responses)
    
    # Add a small delay to simulate thinking (optional)
    import time
    time.sleep(0.5)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 