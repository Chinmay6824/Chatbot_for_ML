import re
import random
import webbrowser
import os
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import difflib  # For better string matching

# Expanded dictionary of machine learning concepts and their explanations
ml_knowledge = {
    "machine learning": "Machine learning is a field of artificial intelligence that uses statistical techniques to give computer systems the ability to 'learn' from data without being explicitly programmed.",
    "supervised learning": "Supervised learning is a type of machine learning where the algorithm learns from labeled training data, and makes predictions based on that data. Examples include classification and regression tasks.",
    "unsupervised learning": "Unsupervised learning is a type of machine learning where the algorithm learns patterns from unlabeled data. Common examples include clustering and dimensionality reduction.",
    "reinforcement learning": "Reinforcement learning is a type of machine learning where the algorithm learns by interacting with an environment and receiving rewards or penalties. It's used in robotics, game playing, and autonomous systems.",
    "neural network": "Neural networks are computing systems inspired by the biological neural networks in animal brains. They consist of artificial neurons that can learn from and make decisions based on data.",
    "deep learning": "Deep learning is a subset of machine learning that uses neural networks with multiple layers (deep neural networks) to analyze various factors of data. It has revolutionized fields like computer vision and natural language processing.",
    "cnn": "Convolutional Neural Networks (CNNs) are a class of deep neural networks most commonly applied to analyzing visual imagery. They use a mathematical operation called convolution in place of general matrix multiplication in at least one of their layers.",
    "convolutional neural network": "Convolutional Neural Networks (CNNs) are a type of neural network designed specifically for processing grid-like data such as images. They use convolutional layers to automatically detect features and patterns in images.",
    "rnn": "Recurrent Neural Networks (RNNs) are a class of neural networks where connections between nodes form a directed graph along a temporal sequence. This allows them to exhibit temporal dynamic behavior, making them suitable for tasks involving sequential data like text or time series.",
    "recurrent neural network": "Recurrent Neural Networks (RNNs) are neural networks specialized for processing sequential data. They maintain an internal memory that helps them retain information about previous inputs, making them ideal for tasks like language modeling and speech recognition.",
    "lstm": "Long Short-Term Memory (LSTM) networks are a type of RNN that can learn long-term dependencies in sequence prediction problems. They have feedback connections and special memory cells that can maintain information over long periods, solving the vanishing gradient problem of standard RNNs.",
    "long short-term memory": "Long Short-Term Memory (LSTM) networks are advanced recurrent neural networks with a special architecture designed to remember information for long periods. They're widely used in speech recognition, language modeling, and time series prediction.",
    "gan": "Generative Adversarial Networks (GANs) consist of two neural networks—a generator and a discriminator—that compete against each other. The generator creates fake data, while the discriminator tries to distinguish real data from fake. This competition drives both networks to improve, eventually leading to the generation of highly realistic data.",
    "generative adversarial network": "Generative Adversarial Networks (GANs) are a framework where two neural networks compete: one generates candidates (Generator) and the other evaluates them (Discriminator). They're used to generate photorealistic images, enhance image resolution, and create artificial data for training.",
    "decision tree": "A decision tree is a flowchart-like structure in which each internal node represents a test on a feature, each branch represents the outcome of the test, and each leaf node represents a class label or decision. They're simple to understand but can easily overfit without proper pruning.",
    "random forest": "Random Forest is an ensemble learning method that operates by constructing multiple decision trees during training and outputting the class that is the mode of the classes of the individual trees. It reduces overfitting and improves accuracy compared to a single decision tree.",
    "svm": "Support Vector Machine (SVM) is a supervised learning model that analyzes data for classification and regression. It uses a technique called the kernel trick to transform data and then finds an optimal boundary between outputs. SVMs are effective in high-dimensional spaces and cases where the number of dimensions exceeds the number of samples.",
    "support vector machine": "Support Vector Machines (SVMs) find the hyperplane that best divides a dataset into classes. They're particularly effective when there's a clear margin of separation between classes and in high-dimensional spaces. They use kernel functions to handle nonlinear classification tasks.",
    "knn": "K-Nearest Neighbors (KNN) is a simple, instance-based learning algorithm that stores all available cases and classifies new cases based on a similarity measure. It's a non-parametric method where an object is classified by a plurality vote of its neighbors.",
    "k-nearest neighbors": "K-Nearest Neighbors (KNN) is a simple algorithm that classifies a data point based on how its neighbors are classified. The 'K' refers to the number of nearest neighbors to include in the majority voting process. It's useful for classification and regression problems but can be computationally expensive with large datasets.",
    "clustering": "Clustering is a technique used in unsupervised learning to group similar data points together. Popular algorithms include K-means, hierarchical clustering, and DBSCAN. Clustering helps identify natural groupings in data without predefined labels.",
    "pca": "Principal Component Analysis (PCA) is a statistical procedure that uses an orthogonal transformation to convert a set of observations into a set of linearly uncorrelated variables called principal components. It's primarily used for dimensionality reduction while preserving as much variance as possible.",
    "principal component analysis": "Principal Component Analysis (PCA) reduces the dimensionality of data by transforming it to a new coordinate system. The first principal component accounts for the most variance in the data, with each succeeding component accounting for less. It's useful for visualization, noise reduction, and as a preprocessing step for other algorithms.",
    "accuracy": "Accuracy is a metric for evaluating classification models. It's the ratio of correct predictions to total predictions made. While commonly used, it can be misleading for imbalanced datasets where one class significantly outnumbers others.",
    "precision": "Precision is a metric that quantifies the number of correct positive predictions made. It's calculated as the ratio of true positives to the sum of true and false positives. It answers the question: 'Of all the instances predicted as positive, how many were actually positive?'",
    "recall": "Recall (also known as sensitivity) is a metric that quantifies the number of correct positive predictions made out of all positive predictions that could have been made. It's calculated as the ratio of true positives to the sum of true positives and false negatives. It answers the question: 'Of all the actual positive instances, how many were correctly identified?'",
    "f1 score": "F1 Score is the harmonic mean of precision and recall. It's a good metric when you need to balance both precision and recall, especially with uneven class distributions. A perfect F1 score has a value of 1, indicating perfect precision and recall.",
    "overfitting": "Overfitting occurs when a model learns the training data too well, including its noise and outliers, and performs poorly on unseen data. It happens when a model is too complex relative to the amount and noisiness of the training data.",
    "underfitting": "Underfitting occurs when a model is too simple to capture the underlying pattern of the data, resulting in poor performance on both training and unseen data. It happens when important features or relationships aren't captured by the model.",
    "cross-validation": "Cross-validation is a resampling procedure used to evaluate machine learning models on a limited data sample. The most common method is k-fold cross-validation, where the data is divided into k subsets, and the model is trained and evaluated k times, each time using a different subset as the test set.",
    "gradient descent": "Gradient descent is an optimization algorithm used to minimize some function by iteratively moving in the direction of steepest descent as defined by the negative of the gradient. It's the foundation for training many machine learning models, including neural networks.",
    "batch normalization": "Batch normalization is a technique for improving the performance and stability of neural networks by normalizing the inputs of each layer, reducing internal covariate shift. It allows higher learning rates and reduces the importance of careful initialization.",
    "dropout": "Dropout is a regularization technique where randomly selected neurons are ignored during training. This helps prevent overfitting by ensuring that the network doesn't become too reliant on any particular neuron. It forces the network to be more robust and generalize better.",
    "bias-variance tradeoff": "The bias-variance tradeoff is the property of a set of predictive models whereby models with lower bias have higher variance and vice versa. Finding the right balance is crucial for building models that generalize well to new data.",
    "bagging": "Bagging (Bootstrap Aggregating) is an ensemble technique that combines the predictions of multiple models to improve accuracy and control overfitting. It involves training models on random subsets of the training data and then aggregating their predictions.",
    "boosting": "Boosting is an ensemble technique that combines a set of weak learners into a strong learner to minimize training errors. Unlike bagging, boosting trains models sequentially, with each new model trying to correct the errors of the combined ensemble so far.",
    "xgboost": "XGBoost is an implementation of gradient boosted decision trees designed for speed and performance. It's highly efficient, flexible, and portable, making it one of the most popular algorithms for structured data problems in machine learning competitions.",
    "regularization": "Regularization is a technique used to prevent overfitting by adding a penalty term to the loss function, discouraging complex models. Common types include L1 (Lasso) and L2 (Ridge) regularization, which penalize large coefficients differently.",
    "hyperparameter": "Hyperparameters are parameters whose values are set before the learning process begins. They can't be learned directly from the training process. Examples include learning rate, number of hidden layers, and number of neurons per layer in neural networks.",
    "feature engineering": "Feature engineering is the process of using domain knowledge to extract features from raw data that make machine learning algorithms work better. It's often the most important step in creating effective machine learning models.",
    "feature selection": "Feature selection is the process of selecting a subset of relevant features for use in model construction. It improves model interpretability, reduces training time, and helps avoid the curse of dimensionality.",
    "one-hot encoding": "One-hot encoding is a process of converting categorical variables into a form that could be provided to machine learning algorithms to improve predictions. It creates a binary column for each category and marks the presence of each category with a 1 and absence with a 0.",
    "transformer": "Transformer is a deep learning model that adopts the mechanism of self-attention, differentially weighting the significance of each part of the input data. It's primarily used in NLP and computer vision tasks, revolutionizing machine translation and other language tasks.",
    "bert": "BERT (Bidirectional Encoder Representations from Transformers) is a transformer-based machine learning technique for natural language processing pre-training developed by Google. It's designed to pre-train deep bidirectional representations by jointly conditioning on both left and right context in all layers.",
    "gpt": "GPT (Generative Pre-trained Transformer) is an autoregressive language model that uses deep learning to produce human-like text, developed by OpenAI. It's trained to predict the next word in a sequence, allowing it to generate coherent and contextually relevant text.",
    "nlp": "Natural Language Processing (NLP) is a field of AI that gives computers the ability to understand, interpret, and manipulate human language. It combines computational linguistics, machine learning, and deep learning to process and analyze large amounts of natural language data.",
    "natural language processing": "Natural Language Processing (NLP) enables computers to understand, interpret, and generate human language. It powers applications like machine translation, sentiment analysis, chatbots, and speech recognition systems.",
    "computer vision": "Computer Vision is a field of AI that enables computers to interpret and make decisions based on visual data from the world. It involves tasks like image classification, object detection, image segmentation, and facial recognition.",
    "reinforcement learning algorithms": "Reinforcement Learning algorithms include Q-Learning, Deep Q-Networks (DQN), Policy Gradient methods, and Actor-Critic methods. These algorithms enable agents to learn optimal behaviors through trial and error interactions with an environment.",
    "backpropagation": "Backpropagation is the central algorithm for training neural networks. It calculates the gradient of the loss function with respect to the network weights, allowing the weights to be updated in a way that minimizes the loss function using gradient descent.",
    "activation function": "Activation functions determine the output of a neural network node given a set of inputs. Common activation functions include ReLU (Rectified Linear Unit), Sigmoid, Tanh, and Softmax. They introduce non-linearity into the network, allowing it to learn complex patterns.",
    "relu": "ReLU (Rectified Linear Unit) is an activation function defined as f(x) = max(0, x). It outputs the input for positive values and zero for negative values. It's widely used in deep learning because it helps mitigate the vanishing gradient problem and allows for faster training.",
    "sigmoid": "The Sigmoid activation function maps any value to a range between 0 and 1, following an S-shaped curve. It's commonly used in the output layer of binary classification problems and in gates within LSTM units, though less common in hidden layers of deep networks due to the vanishing gradient problem.",
    "tanh": "The Tanh (hyperbolic tangent) activation function maps values to a range between -1 and 1, following an S-shaped curve similar to sigmoid but centered around zero. It's often used in hidden layers of neural networks and has stronger gradients near zero compared to sigmoid.",
    "softmax": "The Softmax activation function converts a vector of raw values into a probability distribution, ensuring all outputs sum to 1. It's typically used in the output layer of multi-class classification problems to represent the probability of each class.",
    "classification": "Classification is a supervised learning task where the model predicts discrete class labels or categories. Examples include spam detection (spam/not spam), image classification (cat/dog/etc.), and sentiment analysis (positive/negative/neutral).",
    "regression": "Regression is a supervised learning task where the model predicts continuous numerical values. Examples include predicting house prices, stock market prices, or temperature forecasts. Common algorithms include Linear Regression, Decision Trees, and Neural Networks.",
    "transfer learning": "Transfer Learning is a technique where a model developed for one task is reused as the starting point for a model on a second task. It's particularly popular in deep learning, where pre-trained models like BERT or ResNet are fine-tuned for specific applications.",
    "ensemble learning": "Ensemble Learning combines multiple machine learning models to obtain better predictive performance than could be obtained from any of the constituent models alone. Common methods include bagging (Random Forests), boosting (AdaBoost, XGBoost), and stacking.",
    "data augmentation": "Data Augmentation is a technique used to increase the diversity of training data without actually collecting new data. In image processing, it includes operations like rotation, flipping, cropping, and color adjustments to create additional training examples."
}

# Common acronyms and their expanded forms
acronyms = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "nn": "neural network",
    "cnn": "convolutional neural network",
    "rnn": "recurrent neural network",
    "lstm": "long short-term memory",
    "gan": "generative adversarial network",
    "svm": "support vector machine",
    "knn": "k-nearest neighbors",
    "pca": "principal component analysis",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "rl": "reinforcement learning"
}

# Common ML topic word lists for better matching
ml_topics = {
    "neural networks": ["neural network", "nn", "deep learning", "dl", "cnn", "rnn", "lstm", "gan", "transformer", "bert", "gpt"],
    "algorithms": ["algorithm", "decision tree", "random forest", "svm", "knn", "clustering", "pca", "gradient descent", "xgboost"],
    "evaluation": ["accuracy", "precision", "recall", "f1 score", "overfitting", "underfitting", "cross-validation"],
    "techniques": ["regularization", "hyperparameter", "feature engineering", "feature selection", "one-hot encoding", "transfer learning", "data augmentation"]
}

# Function to find the best match for a query with improved matching
def find_best_match(query):
    query = query.lower().strip()
    
    # Check if the query is a single-word or short acronym and expand it
    if len(query.split()) <= 2:
        query_words = query.split()
        for i, word in enumerate(query_words):
            if word in acronyms:
                query_words[i] = acronyms[word]
        query = " ".join(query_words)
    
    # If the query starts with "what is" or similar patterns, extract the main term
    match = re.search(r"what (is|are) (a |an |the )?([\w\s\-]+)(\?)?", query)
    if match:
        term = match.group(3).strip().lower()
        
        # Direct match in knowledge base
        if term in ml_knowledge:
            return term
        
        # Check if term is an acronym
        if term in acronyms:
            expanded_term = acronyms[term]
            if expanded_term in ml_knowledge:
                return expanded_term
        
        # Try to find a close match using difflib
        close_matches = difflib.get_close_matches(term, ml_knowledge.keys(), n=1, cutoff=0.8)
        if close_matches:
            return close_matches[0]
            
        # Try to match parts of the term
        for key in ml_knowledge.keys():
            if key in term or term in key:
                return key
    
    # Multi-part query handling - check each word individually for better matching
    words = query.split()
    if len(words) > 1:
        # Try to find direct matches for each word
        for word in words:
            if word in ml_knowledge:
                return word
            if word in acronyms and acronyms[word] in ml_knowledge:
                return acronyms[word]
                
    # Direct match in knowledge base for any part of the query
    for key in ml_knowledge:
        if key == query:
            return key
    
    # Check for key phrases in the query
    for key in ml_knowledge:
        if key in query:
            return key
    
    # Check for topic areas - if the query contains multiple terms from a topic area
    topic_matches = {}
    for topic, terms in ml_topics.items():
        matches = sum(1 for term in terms if term in query)
        if matches > 0:
            topic_matches[topic] = matches
    
    # If we found topic matches, return the most relevant term from that topic
    if topic_matches:
        best_topic = max(topic_matches.items(), key=lambda x: x[1])[0]
        for term in ml_topics[best_topic]:
            if term in ml_knowledge and term in query:
                return term
        # If no specific term found, find the closest match from that topic
        for term in ml_topics[best_topic]:
            if term in ml_knowledge:
                return term
    
    # As a last resort, try to find any close matches to the full query
    all_keys = list(ml_knowledge.keys())
    close_matches = difflib.get_close_matches(query, all_keys, n=1, cutoff=0.6)
    if close_matches:
        return close_matches[0]
    
    # Handle complex queries by looking for any ml term
    for key in ml_knowledge:
        for word in query.split():
            if word == key or (len(word) > 3 and key.startswith(word)):
                return key
    
    # If no match found
    return None

# Improved responses for when we don't have a specific answer
fallback_responses = [
    "I'm not sure about that specific topic. Could you ask me about a particular machine learning concept like neural networks, CNNs, SVMs, or gradient descent?",
    "I don't have enough information to answer that question precisely. Try asking about specific machine learning algorithms, techniques, or evaluation metrics.",
    "I'm specialized in machine learning topics. Could you rephrase your question to focus on a specific ML concept?",
    "That's a bit outside my knowledge area. I can answer questions about neural networks, supervised/unsupervised learning, common ML algorithms, and evaluation metrics."
]

# Function to create a more informative response when we don't have a direct match
def create_general_response(query):
    # Check if asking about accuracy
    if "accuracy" in query.lower() or "accurate" in query.lower() or "precision" in query.lower():
        return "Accuracy in machine learning refers to the proportion of correct predictions among the total number of predictions. It's calculated as (True Positives + True Negatives) / Total Predictions. However, for imbalanced datasets, metrics like precision, recall, and F1 score are often more informative."
    
    # Check if asking about neural networks or related terms
    if any(term in query.lower() for term in ["neural", "network", "deep", "learning", "cnn", "rnn", "lstm"]):
        return "Neural networks are computational models inspired by the human brain. They consist of layers of interconnected nodes (neurons) that process and transform data. Deep learning uses neural networks with many layers. Popular types include CNNs for image processing, RNNs for sequence data, and LSTMs for learning long-term dependencies."
    
    # Check if asking about supervised vs unsupervised learning
    if any(term in query.lower() for term in ["supervised", "unsupervised", "reinforcement"]):
        return "In supervised learning, models learn from labeled data to make predictions. Unsupervised learning finds patterns in unlabeled data. Reinforcement learning involves an agent learning to make decisions by receiving rewards or penalties based on its actions in an environment."
    
    # Check if asking about algorithms
    if "algorithm" in query.lower() or any(algo in query.lower() for algo in ["decision tree", "random forest", "svm", "knn"]):
        return "Machine learning algorithms include Decision Trees (flowchart-like models), Random Forests (ensembles of decision trees), Support Vector Machines (finding optimal boundaries between classes), and K-Nearest Neighbors (classification based on nearby examples)."
    
    # Check if the query is asking about a particular topic area
    for topic, terms in ml_topics.items():
        for term in terms:
            if term in query.lower():
                if topic == "neural networks":
                    return "Neural networks are a fundamental concept in machine learning. They include various types like Convolutional Neural Networks (CNNs) for image processing, Recurrent Neural Networks (RNNs) for sequence data, and transformers for NLP tasks. Could you ask about a specific type of neural network?"
                elif topic == "algorithms":
                    return "Machine learning algorithms include supervised learning methods like Decision Trees, Random Forests, and SVMs, as well as unsupervised approaches like clustering and PCA. Could you specify which algorithm you're interested in?"
                elif topic == "evaluation":
                    return "Evaluation metrics in machine learning include accuracy, precision, recall, F1 score, and techniques like cross-validation to ensure model reliability. Different metrics are important for different problems, especially with imbalanced datasets."
                elif topic == "techniques":
                    return "Machine learning employs various techniques to improve model performance, including regularization to prevent overfitting, feature engineering to create better input data, and transfer learning to leverage pre-trained models."
    
    # Default general response
    return random.choice(fallback_responses)

# HTML Template for the chatbot
HTML_TEMPLATE = """
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
                Hi there! I'm your ML assistant. Ask me about machine learning concepts like neural networks, supervised learning, algorithms, or specific terms like CNN, LSTM, or SVM.
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Type your question here..." autocomplete="off">
            <button id="send-button">Send</button>
        </div>
    </div>
    
    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        
        // Enable/disable send button based on input
        userInput.addEventListener('input', function() {
            if (this.value.trim() === '') {
                sendButton.disabled = true;
            } else {
                sendButton.disabled = false;
            }
        });
        
        // Initial state of send button
        sendButton.disabled = userInput.value.trim() === '';
        
        // Handle Enter key press
        userInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
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
            
            // Clear input
            userInput.value = '';
            sendButton.disabled = true;
            
            // Show typing indicator
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'message bot-message';
            typingIndicator.id = 'typing-indicator';
            typingIndicator.textContent = 'Typing...';
            chatBox.appendChild(typingIndicator);
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
            
            # Get the response using the improved function
            response = get_response(query)
            
            # Add a small delay to simulate thinking
            time.sleep(0.5)
            
            # Send the response
            self.wfile.write(json.dumps({'response': response}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ChatbotHandler)
    print(f"Starting ML Chatbot on port {port}...")
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