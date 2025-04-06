import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# ML-related keywords for simple keyword matching
ML_KEYWORDS = {
    'machine learning', 'deep learning', 'neural network', 'artificial intelligence', 'ai', 'ml',
    'supervised learning', 'unsupervised learning', 'reinforcement learning', 'classification',
    'regression', 'clustering', 'decision tree', 'random forest', 'gradient boosting',
    'support vector machine', 'svm', 'k-means', 'knn', 'naive bayes', 'logistic regression',
    'backpropagation', 'cnn', 'rnn', 'lstm', 'gan', 'transformer', 'bert', 'gpt',
    'feature extraction', 'feature selection', 'dimensionality reduction', 'pca', 'svd',
    'cross-validation', 'overfitting', 'underfitting', 'bias', 'variance', 'precision', 'recall',
    'f1 score', 'accuracy', 'roc', 'auc', 'confusion matrix', 'tensorflow', 'pytorch', 'keras',
    'scikit-learn', 'sklearn', 'data mining', 'nlp', 'natural language processing',
    'computer vision', 'image recognition', 'object detection', 'sentiment analysis',
    'recommendation system', 'anomaly detection', 'time series', 'ensemble methods',
    'hyperparameter tuning', 'grid search', 'transfer learning', 'fine-tuning',
    'one-hot encoding', 'tokenization', 'embedding', 'batch normalization', 'dropout',
    'activation function', 'relu', 'sigmoid', 'tanh', 'softmax', 'loss function',
    'gradient descent', 'adam', 'sgd', 'learning rate', 'epoch', 'batch size'
}

def preprocess_text(text):
    """Preprocess text by converting to lowercase, removing punctuation and stopwords"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return ' '.join(filtered_text)

def is_ml_related(question):
    """
    Determine if a question is related to machine learning using keyword matching.
    
    Args:
        question (str): The user's question
        
    Returns:
        bool: True if the question is ML-related, False otherwise
    """
    # Preprocess the question
    processed_question = preprocess_text(question)
    
    # Simple keyword matching
    for keyword in ML_KEYWORDS:
        if keyword in processed_question or keyword in question.lower():
            return True
            
    # If no keywords matched, it's likely not ML-related
    return False

def get_ml_response(question):
    """
    Generate a response for an ML-related question.
    
    Args:
        question (str): The user's ML-related question
        
    Returns:
        str: A response to the question
    """
    # Example responses for common ML topics
    responses = {
        'neural network': "Neural networks are computing systems inspired by the biological neural networks in animal brains. They consist of artificial neurons that can learn from data through a process called training.",
        'deep learning': "Deep learning is a subset of machine learning that uses neural networks with multiple layers (deep neural networks) to analyze various factors of data.",
        'supervised learning': "Supervised learning is a type of machine learning where the model is trained on labeled data, learning to map inputs to known outputs.",
        'unsupervised learning': "Unsupervised learning is a type of machine learning where the model works on unlabeled data, trying to find patterns or structure without explicit guidance.",
        'reinforcement learning': "Reinforcement learning is a type of machine learning where an agent learns to make decisions by taking actions in an environment to maximize some notion of cumulative reward.",
        'classification': "Classification is a supervised learning task where the model learns to categorize input data into predefined classes or categories.",
        'regression': "Regression is a supervised learning task where the model predicts continuous numerical values based on input features.",
        'clustering': "Clustering is an unsupervised learning technique that groups similar data points together based on certain features or characteristics.",
        'overfitting': "Overfitting occurs when a model learns the training data too well, including its noise and outliers, resulting in poor performance on new, unseen data.",
        'gradient descent': "Gradient descent is an optimization algorithm used to minimize the loss function in machine learning models by iteratively moving toward the steepest descent."
    }
    
    # Check if any key phrases are in the question
    for key, response in responses.items():
        if key in question.lower():
            return response
    
    # Default response if no specific match is found
    return "That's an interesting machine learning question. In a full implementation, I would provide a detailed answer using a knowledge base or a language model trained on ML concepts."

# For testing purposes
if __name__ == "__main__":
    test_questions = [
        "What is a neural network?",
        "How does deep learning work?",
        "Can you explain the weather forecast?",
        "What's the difference between supervised and unsupervised learning?",
        "How do I make a sandwich?"
    ]
    
    for q in test_questions:
        is_ml = is_ml_related(q)
        print(f"Question: {q}")
        print(f"Is ML-related: {is_ml}")
        if is_ml:
            print(f"Response: {get_ml_response(q)}")
        print("---") 