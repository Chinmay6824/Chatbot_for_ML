import re
import random
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import difflib

# Comprehensive ML knowledge base
ml_knowledge = {
    "machine learning": "Machine learning is a field of artificial intelligence that uses statistical techniques to give computer systems the ability to 'learn' from data without being explicitly programmed. It focuses on developing algorithms that can access data and use it to learn for themselves.",
    
    "deep learning": "Deep learning is a subset of machine learning that uses neural networks with multiple layers (deep neural networks) to analyze various factors of data. It's particularly powerful for tasks like image and speech recognition, natural language processing, and other complex pattern recognition tasks.",
    
    "neural network": "Neural networks are computing systems inspired by the biological neural networks in animal brains. They consist of artificial neurons that can learn from and make decisions based on data. The connections between neurons can be strengthened or weakened through training, allowing the network to learn patterns in data.",
    
    "supervised learning": "Supervised learning is a type of machine learning where the algorithm learns from labeled training data, and makes predictions based on that data. The algorithm is trained on input-output pairs, where the desired output is known. Examples include classification (predicting a category) and regression (predicting a numerical value).",
    
    "unsupervised learning": "Unsupervised learning is a type of machine learning where the algorithm learns patterns from unlabeled data. The system tries to learn the patterns and structure from the data without explicit guidance. Common techniques include clustering (grouping similar data points) and dimensionality reduction (simplifying data while preserving important information).",
    
    "reinforcement learning": "Reinforcement learning is a type of machine learning where an agent learns to make decisions by taking actions in an environment to maximize a reward. The agent learns through trial and error, receiving feedback in the form of rewards or penalties. It's commonly used in robotics, game playing, and autonomous systems.",
    
    "cnn": "Convolutional Neural Networks (CNNs) are a class of deep neural networks most commonly applied to analyzing visual imagery. They use a mathematical operation called convolution in place of general matrix multiplication in at least one of their layers. CNNs are particularly effective for image classification, object detection, and facial recognition tasks.",
    
    "rnn": "Recurrent Neural Networks (RNNs) are a class of neural networks where connections between nodes form a directed graph along a temporal sequence. This allows them to exhibit temporal dynamic behavior, making them suitable for tasks involving sequential data like text or time series. However, traditional RNNs suffer from the vanishing gradient problem during training.",
    
    "lstm": "Long Short-Term Memory (LSTM) networks are a type of RNN that can learn long-term dependencies in sequence prediction problems. They have feedback connections and special memory cells that can maintain information over long periods, solving the vanishing gradient problem of standard RNNs. LSTMs are widely used in speech recognition, language modeling, and time series prediction.",
    
    "gan": "Generative Adversarial Networks (GANs) consist of two neural networks—a generator and a discriminator—that compete against each other. The generator creates fake data, while the discriminator tries to distinguish real data from fake. This competition drives both networks to improve, eventually leading to the generation of highly realistic data like images, text, or audio.",
    
    "decision tree": "A decision tree is a flowchart-like structure in which each internal node represents a test on a feature, each branch represents the outcome of the test, and each leaf node represents a class label or decision. Decision trees are simple to understand and interpret but can easily overfit the training data without proper pruning or limitations on tree depth.",
    
    "random forest": "Random Forest is an ensemble learning method that operates by constructing multiple decision trees during training and outputting the class that is the mode of the classes of the individual trees (for classification) or the average prediction (for regression). It reduces overfitting and improves accuracy compared to a single decision tree by introducing randomness in feature selection and data sampling.",
    
    "svm": "Support Vector Machine (SVM) is a supervised learning model that analyzes data for classification and regression. It uses a technique called the kernel trick to transform data and then finds an optimal boundary (hyperplane) between outputs. SVMs are effective in high-dimensional spaces and cases where the number of dimensions exceeds the number of samples, making them popular for text classification and image recognition.",
    
    "knn": "K-Nearest Neighbors (KNN) is a simple, instance-based learning algorithm that stores all available cases and classifies new cases based on a similarity measure (e.g., distance functions). It's a non-parametric method where an object is classified by a plurality vote of its neighbors, with the object being assigned to the class most common among its k nearest neighbors.",
    
    "k-means": "K-means clustering is an unsupervised learning algorithm that partitions a dataset into K distinct, non-overlapping clusters. The algorithm works by selecting K initial centroids, assigning each data point to the nearest centroid, recalculating centroids based on the current assignment, and repeating until convergence. It's widely used for customer segmentation, image compression, and anomaly detection.",
    
    "pca": "Principal Component Analysis (PCA) is a dimensionality reduction technique that transforms a dataset into a lower-dimensional space while preserving as much variance as possible. It identifies the directions (principal components) along which the data varies the most. PCA is useful for visualization, noise reduction, and as a preprocessing step for other machine learning algorithms.",
    
    "cross-validation": "Cross-validation is a resampling procedure used to evaluate machine learning models on a limited data sample. The most common method is k-fold cross-validation, where the data is divided into k subsets, and the model is trained and evaluated k times, each time using a different subset as the test set. This helps assess how well the model will generalize to independent data.",
    
    "overfitting": "Overfitting occurs when a model learns the training data too well, including its noise and outliers, and performs poorly on unseen data. It happens when a model is too complex relative to the amount and noisiness of the training data. Signs of overfitting include perfect performance on training data but poor performance on validation or test data.",
    
    "underfitting": "Underfitting occurs when a model is too simple to capture the underlying pattern of the data, resulting in poor performance on both training and unseen data. It happens when important features or relationships aren't captured by the model. Signs of underfitting include poor performance on both training and validation data.",
    
    "gradient descent": "Gradient descent is an optimization algorithm used to minimize some function by iteratively moving in the direction of steepest descent as defined by the negative of the gradient. It's the foundation for training many machine learning models, including neural networks. Variants include stochastic gradient descent (SGD), mini-batch gradient descent, and adaptive learning rate methods like Adam and RMSprop.",
    
    "backpropagation": "Backpropagation is an algorithm for training neural networks by calculating the gradient of the loss function with respect to each weight. It efficiently computes these gradients using the chain rule of calculus, propagating the error from the output layer back through the network. This allows the network weights to be updated in a way that reduces the error on the training data.",
    
    "regularization": "Regularization is a technique used to prevent overfitting by adding a penalty term to the loss function, discouraging complex models. Common types include L1 regularization (Lasso), which can lead to sparse models by pushing some weights to exactly zero, and L2 regularization (Ridge), which penalizes large weights without necessarily zeroing them out.",
    
    "bagging": "Bagging (Bootstrap Aggregating) is an ensemble technique that combines the predictions of multiple models to improve accuracy and control overfitting. It involves training models on random subsets of the training data (sampled with replacement) and then aggregating their predictions by voting (for classification) or averaging (for regression). Random Forest is a popular implementation of bagging.",
    
    "boosting": "Boosting is an ensemble technique that combines a set of weak learners into a strong learner to minimize training errors. Unlike bagging, boosting trains models sequentially, with each new model trying to correct the errors of the combined ensemble so far. Popular boosting algorithms include AdaBoost, Gradient Boosting, and XGBoost.",
    
    "hyperparameter": "Hyperparameters are parameters whose values are set before the learning process begins. They can't be learned directly from the training process and must be tuned separately. Examples include learning rate, number of hidden layers, number of neurons per layer in neural networks, and regularization strength. Hyperparameter optimization techniques include grid search, random search, and Bayesian optimization.",
    
    "feature engineering": "Feature engineering is the process of using domain knowledge to extract features from raw data that make machine learning algorithms work better. It can involve feature creation (generating new features from existing ones), feature transformation (changing the scale or distribution of features), and feature selection (choosing the most relevant features). Good feature engineering can significantly improve model performance.",
    
    "confusion matrix": "A confusion matrix is a table used to evaluate the performance of a classification model. It shows the counts of true positive, false positive, true negative, and false negative predictions. From these counts, various performance metrics can be derived, including accuracy, precision, recall, and F1 score. It's particularly useful for understanding the types of errors a model is making.",
    
    "precision": "Precision is a metric that quantifies the number of correct positive predictions made out of all positive predictions. It's calculated as (True Positives) / (True Positives + False Positives). High precision indicates low false positive rate, which is important in applications where false positives are costly, such as spam detection or medical diagnosis.",
    
    "recall": "Recall (also known as sensitivity) is a metric that quantifies the number of correct positive predictions made out of all actual positives. It's calculated as (True Positives) / (True Positives + False Negatives). High recall indicates low false negative rate, which is important in applications where missing positive cases is costly, such as disease detection or fraud detection.",
    
    "f1 score": "F1 Score is the harmonic mean of precision and recall, providing a balance between the two metrics. It's calculated as 2 * (Precision * Recall) / (Precision + Recall). F1 score is particularly useful when dealing with imbalanced datasets where one class is much more frequent than others, as it prevents the model from achieving high accuracy simply by predicting the majority class.",
    
    "accuracy": "Accuracy is a metric that measures the proportion of correct predictions among the total number of predictions. It's calculated as (True Positives + True Negatives) / (Total Predictions). While commonly used, accuracy can be misleading for imbalanced datasets where one class significantly outnumbers others, as a model can achieve high accuracy simply by predicting the majority class.",
    
    "roc curve": "Receiver Operating Characteristic (ROC) curve is a graphical plot that illustrates the diagnostic ability of a binary classifier system as its discrimination threshold is varied. It plots the true positive rate (sensitivity) against the false positive rate (1 - specificity) at various threshold settings. The area under the ROC curve (AUC-ROC) is a single number that summarizes the overall performance of the classifier.",
    
    "batch normalization": "Batch normalization is a technique used to improve the training of neural networks by normalizing the inputs of each layer to have zero mean and unit variance. This helps mitigate the internal covariate shift problem, allowing higher learning rates and less careful initialization. It also has a slight regularization effect, reducing the need for dropout in some cases.",
    
    "dropout": "Dropout is a regularization technique where randomly selected neurons are ignored during training. This helps prevent overfitting by ensuring that the network doesn't become too reliant on any particular neuron. During training, neurons are 'dropped out' with a certain probability, and during inference, all neurons are used but their outputs are scaled appropriately.",
    
    "transformer": "The Transformer is a deep learning model architecture introduced in the paper 'Attention Is All You Need' that relies entirely on self-attention mechanisms without using recurrence or convolution. It has become the foundation for many state-of-the-art natural language processing models, including BERT and GPT. Transformers are particularly effective for tasks involving sequential data due to their ability to process all elements of a sequence in parallel and capture long-range dependencies.",
    
    "bert": "BERT (Bidirectional Encoder Representations from Transformers) is a transformer-based machine learning model for natural language processing. Unlike earlier models that processed text in one direction, BERT is designed to pre-train deep bidirectional representations by jointly conditioning on both left and right context in all layers. This allows it to develop a deeper understanding of language context and flow, making it highly effective for tasks like question answering, sentiment analysis, and language inference."
}

# Function to generate a response for ML questions
def generate_ml_response(query):
    query = query.lower().strip()
    
    # Handle greetings
    greetings = ["hi", "hello", "hey", "greetings"]
    if query in greetings or any(greeting in query.split() for greeting in greetings):
        return "Hello! I'm an ML assistant designed to answer questions about machine learning concepts. What would you like to know about machine learning today?"
    
    # Handle direct questions about what the system can do
    if "what can you do" in query or "what are you" in query or "who are you" in query:
        return "I'm a specialized chatbot focused on machine learning topics. I can explain concepts like neural networks, supervised learning, deep learning algorithms, evaluation metrics, and more. Just ask me any question about machine learning!"
    
    # Check for direct matches in our knowledge base
    for term, explanation in ml_knowledge.items():
        if query == term or query == f"what is {term}" or query == f"explain {term}":
            return explanation
    
    # Extract key term from "what is X" pattern
    match = re.search(r"what (is|are) (a |an |the )?([\w\s\-]+)(\?)?", query)
    if match:
        term = match.group(3).strip().lower()
        
        # Check direct match with the extracted term
        if term in ml_knowledge:
            return ml_knowledge[term]
        
        # Try to find close matches
        close_matches = difflib.get_close_matches(term, ml_knowledge.keys(), n=1, cutoff=0.8)
        if close_matches:
            return f"I think you're asking about {close_matches[0]}. {ml_knowledge[close_matches[0]]}"
    
    # Check for terms from our knowledge base contained in the query
    matched_terms = [term for term in ml_knowledge.keys() if term in query]
    if matched_terms:
        # Return the longest matched term to avoid partial matches
        best_match = max(matched_terms, key=len)
        return ml_knowledge[best_match]
    
    # Check for difference/comparison questions
    difference_patterns = [
        r"(difference|compare|vs|versus) (between )?([\w\s]+) (and|vs|versus) ([\w\s]+)",
        r"(how|what)('s| is| are) ([\w\s]+) (different from|compared to) ([\w\s]+)",
        r"([\w\s]+) (vs|versus|or|compared to) ([\w\s]+)"
    ]
    
    for pattern in difference_patterns:
        match = re.search(pattern, query)
        if match:
            # Extract the two terms being compared
            groups = match.groups()
            term1 = None
            term2 = None
            
            # Handle different patterns
            if len(groups) == 5:  # First pattern
                term1 = groups[2].strip().lower()
                term2 = groups[4].strip().lower()
            elif len(groups) == 5:  # Second pattern
                term1 = groups[2].strip().lower()
                term2 = groups[4].strip().lower()
            elif len(groups) == 3:  # Third pattern
                term1 = groups[0].strip().lower()
                term2 = groups[2].strip().lower()
            
            if term1 and term2:
                # Find closest matches in our knowledge base
                term1_match = find_best_match(term1)
                term2_match = find_best_match(term2)
                
                if term1_match and term2_match:
                    return f"Comparing {term1_match} and {term2_match}:\n\n{term1_match.capitalize()}: {ml_knowledge[term1_match]}\n\n{term2_match.capitalize()}: {ml_knowledge[term2_match]}"
    
    # If the query is about machine learning but we don't have a specific match
    ml_related_terms = ["machine learning", "neural", "algorithm", "model", "training", "data", "prediction", "classification", "regression", "clustering", "supervised", "unsupervised", "reinforcement"]
    if any(term in query for term in ml_related_terms):
        return "I understand you're asking about a machine learning topic, but I don't have specific information on that particular aspect. Could you rephrase your question or ask about a more general machine learning concept like neural networks, supervised/unsupervised learning, or specific algorithms?"
    
    # Default response for non-ML questions
    return "I'm specialized in answering questions about machine learning. If you have a question about neural networks, algorithms, training methods, or other ML concepts, I'd be happy to help!"

# Find the best match for a term in our knowledge base
def find_best_match(term):
    if term in ml_knowledge:
        return term
    
    # Try to find close matches
    close_matches = difflib.get_close_matches(term, ml_knowledge.keys(), n=1, cutoff=0.7)
    if close_matches:
        return close_matches[0]
    
    return None

# HTML Template for the chatbot
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ML GPT</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f7f7f8;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        
        .header {
            background-color: #10a37f;
            color: white;
            text-align: center;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: normal;
        }
        
        .chat-container {
            flex: 1;
            max-width: 900px;
            margin: 0 auto;
            width: 100%;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            margin-top: 20px;
            margin-bottom: 20px;
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
            margin-bottom: 20px;
            padding: 12px 16px;
            border-radius: 8px;
            max-width: 88%;
            line-height: 1.5;
        }
        
        .user-message {
            background-color: #f0f4f9;
            margin-left: auto;
            color: #343541;
        }
        
        .bot-message {
            background-color: #f7f7f8;
            margin-right: auto;
            color: #343541;
            border: 1px solid #e5e5e5;
        }
        
        .input-container {
            display: flex;
            padding: 15px;
            border-top: 1px solid #e5e5e5;
            background-color: white;
        }
        
        #user-input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 16px;
            font-family: inherit;
            resize: none;
            height: 24px;
            max-height: 120px;
            overflow-y: auto;
        }
        
        #send-button {
            padding: 0 20px;
            background-color: #10a37f;
            color: white;
            border: none;
            border-radius: 6px;
            margin-left: 10px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.2s;
        }
        
        #send-button:hover {
            background-color: #0c8b6c;
        }
        
        #send-button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        
        .typing-indicator {
            display: inline-block;
            width: 50px;
            height: 20px;
        }
        
        .typing-indicator span {
            display: inline-block;
            width: 8px;
            height: 8px;
            margin-right: 3px;
            background-color: #10a37f;
            border-radius: 50%;
            opacity: 0.4;
            animation: typing 1.4s infinite both;
        }
        
        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typing {
            0% {
                opacity: 0.4;
                transform: translateY(0);
            }
            50% {
                opacity: 1;
                transform: translateY(-5px);
            }
            100% {
                opacity: 0.4;
                transform: translateY(0);
            }
        }
        
        @media (max-width: 768px) {
            .chat-container {
                margin: 10px;
                border-radius: 0;
            }
            
            .message {
                max-width: 85%;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>ML GPT - Machine Learning Assistant</h1>
    </div>
    
    <div class="chat-container">
        <div class="chat-box" id="chat-box">
            <div class="message bot-message">
                Hello! I'm ML GPT, a specialized AI assistant focused on machine learning topics. Ask me any questions about neural networks, algorithms, training methods, or other ML concepts!
            </div>
        </div>
        
        <div class="input-container">
            <textarea id="user-input" placeholder="Ask a question about machine learning..." rows="1"></textarea>
            <button id="send-button">Send</button>
        </div>
    </div>
    
    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        
        // Auto-resize textarea as user types
        userInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (Math.min(this.scrollHeight, 120)) + 'px';
            
            // Enable/disable send button based on input
            if (this.value.trim() === '') {
                sendButton.disabled = true;
            } else {
                sendButton.disabled = false;
            }
        });
        
        // Initial state of send button
        sendButton.disabled = userInput.value.trim() === '';
        
        // Handle Enter key press (send on Enter, new line on Shift+Enter)
        userInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                if (!sendButton.disabled) {
                    sendMessage();
                }
            }
        });
        
        // Send button click event
        sendButton.addEventListener('click', function() {
            if (!sendButton.disabled) {
                sendMessage();
            }
        });
        
        // Function to send message and get response
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
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message bot-message';
            typingDiv.id = 'typing-indicator';
            
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'typing-indicator';
            
            for (let i = 0; i < 3; i++) {
                const dot = document.createElement('span');
                typingIndicator.appendChild(dot);
            }
            
            typingDiv.appendChild(typingIndicator);
            chatBox.appendChild(typingDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            
            // Get response from server
            fetch('/get_response?query=' + encodeURIComponent(message))
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
            
            // Replace newlines with <br> for proper display
            text = text.replace(/\\n/g, '<br>').replace(/\n/g, '<br>');
            messageDiv.innerHTML = text;
            
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
"""

class ChatbotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        elif self.path.startswith('/get_response'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Parse the query
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            query = query_params.get('query', [''])[0]
            
            # Get the ML-specific response
            response = generate_ml_response(query)
            
            # Add a delay to simulate thinking (optional)
            time.sleep(1)
            
            # Send the response
            self.wfile.write(json.dumps({'response': response}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ChatbotHandler)
    print(f"Starting ML GPT on port {port}...")
    print(f"Open your browser and go to: http://localhost:{port}")
    
    # Open browser automatically
    webbrowser.open(f'http://localhost:{port}')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down the server...')
        httpd.server_close()

if __name__ == '__main__':
    port = 8000
    run_server(port) 