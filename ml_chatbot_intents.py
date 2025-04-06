from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import random
import re
import os
import difflib
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure logging with error handling
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('chatbot.log'),
            logging.StreamHandler()
        ]
    )
except Exception as e:
    print(f"Warning: Could not set up file logging: {e}")
    # Fallback to just console logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Define technical ML terms at module level
technical_ml_terms = {
    'epoch': 'hyperparameter_tuning',
    'epochs': 'hyperparameter_tuning',
    'accuracy': 'model_evaluation',
    'learning rate': 'hyperparameter_tuning',
    'batch size': 'hyperparameter_tuning',
    'overfitting': 'overfitting',
    'underfitting': 'underfitting',
    'regularization': 'regularization',
    'dropout': 'regularization',
    'optimizer': 'optimization',
    'sgd': 'optimization',
    'adam': 'optimization'
}

# Load intents with better error handling
def load_intents():
    possible_paths = [
        r"C:\Users\Asus\Downloads\intents1 (1).json",
        'intents1.json',
        os.path.join(os.path.dirname(__file__), 'intents1.json'),
        'intents.json'
    ]
    
    for path in possible_paths:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(f"Successfully loaded intents from {path}")
                print(f"Found {len(data['intents'])} intents")
                
                # Validate the intents structure
                valid_intents = []
                for intent in data['intents']:
                    if 'tag' in intent and 'patterns' in intent and 'responses' in intent:
                        if len(intent['patterns']) > 0 and len(intent['responses']) > 0:
                            valid_intents.append(intent)
                        else:
                            print(f"Warning: Intent {intent.get('tag')} has empty patterns or responses")
                    else:
                        print(f"Warning: Intent missing required fields: {intent}")
                
                if len(valid_intents) < len(data['intents']):
                    print(f"Warning: {len(data['intents']) - len(valid_intents)} intents were invalid")
                    data['intents'] = valid_intents
                
                return data
        except Exception as e:
            print(f"Could not load intents from {path}: {e}")
            continue
    
    # If no file could be loaded, return minimal fallback
    print("Warning: Using minimal fallback intents structure")
    return {
        "intents": [
            {
                "tag": "fallback",
                "patterns": [""],
                "responses": ["Sorry, I'm having trouble accessing my knowledge base. Please try again later."]
            }
        ]
    }

intents_data = load_intents()

# HTML template for the chat interface - mobile-friendly
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
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
        
        .refresh-button:hover, .share-button:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .share-button {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
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
        
        .not-ml-message {
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
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
        
        .suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
            overflow-x: auto;
            padding-bottom: 5px;
            -webkit-overflow-scrolling: touch;
        }
        
        .suggestion-chip {
            background-color: #e3f2fd;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 14px;
            white-space: nowrap;
            cursor: pointer;
            transition: background-color 0.3s ease;
            border: 1px solid #bbdefb;
        }
        
        .suggestion-chip:hover {
            background-color: #bbdefb;
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
            
            button {
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
            
            .not-ml-message {
                background-color: #3e2723;
                border-left: 4px solid #ff9800;
                color: #e0e0e0;
            }
            
            .input-form {
                background: #2d2d2d;
            }
            
            #user-input {
                background: #1e1e1e;
                color: #e0e0e0;
                border-color: #424242;
            }
            
            .suggestion-chip {
                background-color: #0d47a1;
                color: white;
                border-color: #1565c0;
            }
            
            .suggestion-chip:hover {
                background-color: #1565c0;
            }
        
        .upload-container {
            display: flex;
            justify-content: center;
            margin: 10px 0;
            padding: 10px;
            background: rgba(74, 111, 165, 0.1);
            border-radius: 8px;
        }
        
        .upload-button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            display: flex;
            align-items: center;
        }
        
        .upload-button svg {
            margin-right: 8px;
        }
        
        .upload-button:hover {
            background-color: var(--secondary-color);
        }
        
        #file-upload {
            display: none;
        }
        
        .file-info {
            margin-left: 10px;
            font-size: 14px;
            color: var(--text-color);
            display: flex;
            align-items: center;
        }
        
        .process-file-button {
            background-color: var(--secondary-color);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            margin-left: 10px;
            display: none;
        }
        
        .process-file-button:hover {
            background-color: #0d47a1;
        }
        
        @media (prefers-color-scheme: dark) {
            .upload-container {
                background: rgba(74, 111, 165, 0.2);
            }
            
            .file-info {
                color: #e0e0e0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ML Chatbot</h1>
            <p>Your AI Assistant for Machine Learning Concepts</p>
            <button class="refresh-button" onclick="refreshChat()">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4C7.58 4 4.01 7.58 4.01 12C4.01 16.42 7.58 20 12 20C15.73 20 18.84 17.45 19.73 14H17.65C16.83 16.33 14.61 18 12 18C8.69 18 6 15.31 6 12C6 8.69 8.69 6 12 6C13.66 6 15.14 6.69 16.22 7.78L13 11H20V4L17.65 6.35Z" fill="white"/>
                </svg>
                Refresh
            </button>
            <button class="share-button" onclick="shareChat()">Share</button>
        </header>
        
        <div class="chat-container">
            <div id="messages">
                <div class="message bot-message">
                    👋 Welcome! I'm your ML Chatbot, specialized in answering questions about machine learning concepts and related topics. What would you like to know about machine learning today?
                </div>
            </div>
            
            <div class="typing-indicator" id="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
            
            <div class="suggestions">
                <div class="suggestion-chip" onclick="askQuestion('What is machine learning?')">What is machine learning?</div>
                <div class="suggestion-chip" onclick="askQuestion('Explain neural networks')">Neural Networks</div>
                <div class="suggestion-chip" onclick="askQuestion('What is deep learning?')">Deep Learning</div>
                <div class="suggestion-chip" onclick="askQuestion('Supervised vs Unsupervised learning')">Supervised vs Unsupervised</div>
                <div class="suggestion-chip" onclick="askQuestion('What is reinforcement learning?')">Reinforcement Learning</div>
            </div>
            
            <div class="upload-container">
                <input type="file" id="file-upload" accept=".txt,.csv,.json">
                <button class="upload-button" onclick="document.getElementById('file-upload').click()">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M19.35 10.04C18.67 6.59 15.64 4 12 4C9.11 4 6.6 5.64 5.35 8.04C2.34 8.36 0 10.91 0 14C0 17.31 2.69 20 6 20H19C21.76 20 24 17.76 24 15C24 12.36 21.95 10.22 19.35 10.04ZM19 18H6C3.79 18 2 16.21 2 14C2 11.95 3.53 10.24 5.56 10.03L6.63 9.92L7.13 8.97C8.08 7.14 9.94 6 12 6C14.62 6 16.88 7.86 17.39 10.43L17.69 11.93L19.22 12.04C20.78 12.14 22 13.45 22 15C22 16.65 20.65 18 19 18ZM8 13H10.55V16H13.45V13H16L12 9L8 13Z" fill="white"/>
                    </svg>
                    Upload Questions
                </button>
                <div class="file-info" id="file-info"></div>
                <button class="process-file-button" id="process-file-button" onclick="processUploadedFile()">Process File</button>
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
        const messagesDiv = document.getElementById('messages');
        const chatForm = document.getElementById('chat-form');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        const typingIndicator = document.getElementById('typing-indicator');
        let chatHistory = [];

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
            localStorage.setItem('mlChatHistory', JSON.stringify(chatHistory));
        }

        function showTypingIndicator() {
            typingIndicator.style.display = 'block';
            scrollToBottom();
        }

        function hideTypingIndicator() {
            typingIndicator.style.display = 'none';
        }

        function askQuestion(question) {
            userInput.value = question;
            chatForm.dispatchEvent(new Event('submit'));
        }
        
        function shareChat() {
            // Create a shareable URL or text
            const shareText = "Check out this ML Chatbot: " + window.location.href;
            
            // Use Web Share API if available
            if (navigator.share) {
                navigator.share({
                    title: 'ML Chatbot',
                    text: 'Check out this Machine Learning Chatbot!',
                    url: window.location.href,
                })
                .catch(error => console.log('Error sharing:', error));
            } else {
                // Fallback to copying to clipboard
                navigator.clipboard.writeText(shareText)
                    .then(() => alert('Link copied to clipboard! Share it with your friends.'))
                    .catch(err => console.error('Failed to copy: ', err));
            }
        }
        
        function refreshChat() {
            // Clear chat history
            chatHistory = [];
            localStorage.removeItem('mlChatHistory');
            
            // Clear messages
            messagesDiv.innerHTML = '';
            
            // Add welcome message
            const welcomeMessage = document.createElement('div');
            welcomeMessage.className = 'message bot-message';
            welcomeMessage.textContent = '👋 Welcome! I\'m your ML Chatbot, specialized in answering questions about machine learning concepts and related topics. What would you like to know about machine learning today?';
            messagesDiv.appendChild(welcomeMessage);
            
            // Focus on input
            userInput.focus();
        }

        // File upload handling
        const fileUpload = document.getElementById('file-upload');
        const fileInfo = document.getElementById('file-info');
        const processFileButton = document.getElementById('process-file-button');
        let uploadedFile = null;
        
        fileUpload.addEventListener('change', (e) => {
            uploadedFile = e.target.files[0];
            if (uploadedFile) {
                fileInfo.textContent = `Selected: ${uploadedFile.name}`;
                processFileButton.style.display = 'block';
            } else {
                fileInfo.textContent = '';
                processFileButton.style.display = 'none';
            }
        });
        
        async function processUploadedFile() {
            if (!uploadedFile) return;
            
            // Show typing indicator
            showTypingIndicator();
            
            // Create a message indicating file processing
            addMessage(`Processing file: ${uploadedFile.name}`, 'user');
            
            try {
                const formData = new FormData();
                formData.append('file', uploadedFile);
                
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                // Hide typing indicator
                hideTypingIndicator();
                
                if (data.error) {
                    addMessage(`Error processing file: ${data.error}`, 'not-ml');
                } else {
                    // Add bot response
                    addMessage(data.response, 'bot');
                    
                    // If there are multiple responses, add them
                    if (data.additional_responses && data.additional_responses.length > 0) {
                        data.additional_responses.forEach(resp => {
                            addMessage(resp, 'bot');
                        });
                    }
                }
                
                // Reset file upload
                fileUpload.value = '';
                fileInfo.textContent = '';
                processFileButton.style.display = 'none';
                uploadedFile = null;
                
            } catch (error) {
                console.error('Error:', error);
                hideTypingIndicator();
                addMessage('Sorry, there was an error processing your file. Please try again.', 'not-ml');
            }
        }

        // Load chat history from local storage
        function loadChatHistory() {
            const savedHistory = localStorage.getItem('mlChatHistory');
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
                    body: JSON.stringify({ message }),
                });

                if (!response.ok) {
                    throw new Error(`Server responded with status: ${response.status}`);
                }

                const data = await response.json();
                
                // Hide typing indicator
                hideTypingIndicator();
                
                // Add bot response
                addMessage(
                    data.response,
                    data.is_ml_related ? 'bot' : 'not-ml'
                );
                
                // Update suggestions based on context
                updateSuggestions(message, data.response);
                
            } catch (error) {
                console.error('Error:', error);
                hideTypingIndicator();
                addMessage('Sorry, something went wrong. Please try again.', 'not-ml');
            }
            
            // Focus back on the input field
            userInput.focus();
        });
        
        function updateSuggestions(userMessage, botResponse) {
            // This function could dynamically update the suggestion chips based on the conversation context
            // For simplicity, we'll keep the original suggestions for now
        }

        // Initial load
        document.addEventListener('DOMContentLoaded', () => {
            loadChatHistory();
            scrollToBottom();
            
            // Focus input on mobile after a short delay (helps with mobile keyboards)
            setTimeout(() => {
                if (window.innerWidth <= 768) {
                    userInput.focus();
                }
            }, 500);
        });
        
        // Handle service worker for PWA support
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(registration => {
                        console.log('ServiceWorker registration successful');
                    })
                    .catch(error => {
                        console.log('ServiceWorker registration failed:', error);
                    });
            });
        }

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
    </script>
</body>
</html>
"""

def analyze_question_complexity(message):
    """Analyze the complexity of the question to determine if it's compound"""
    # Keywords that might indicate a compound question
    relation_keywords = ['and', 'versus', 'vs', 'compared to', 'relationship between', 'difference between', 'how does', 'impact of']
    question_marks = message.count('?')
    
    # Count relation keywords
    relation_count = sum(1 for keyword in relation_keywords if keyword in message.lower())
    
    # Determine if it's a compound question
    is_compound = question_marks > 1 or relation_count > 0
    
    # Extract main topics
    topics = []
    for term in technical_ml_terms.keys():
        if term in message.lower():
            topics.append(term)
    
    return {
        'is_compound': is_compound,
        'topics': topics,
        'relation_keywords': [kw for kw in relation_keywords if kw in message.lower()]
    }

def generate_compound_response(topics, relations):
    """Generate a comprehensive response for compound questions"""
    # Map topics to their explanations
    topic_explanations = {
        'epoch': "An epoch is one complete pass through the training dataset",
        'accuracy': "Accuracy measures the percentage of correct predictions",
        'learning rate': "Learning rate controls how much to adjust the model in response to errors",
        'batch size': "Batch size is the number of training examples used in one iteration",
        'overfitting': "Overfitting occurs when a model learns the training data too well",
        'underfitting': "Underfitting happens when a model is too simple to learn the patterns",
        'regularization': "Regularization helps prevent overfitting by adding constraints",
        'dropout': "Dropout randomly deactivates neurons during training to prevent overfitting",
        'optimizer': "An optimizer adjusts the model's parameters to minimize error"
    }
    
    # Generate response based on topics and their relationships
    if len(topics) >= 2:
        response_parts = []
        # Add individual explanations
        for topic in topics:
            if topic in topic_explanations:
                response_parts.append(topic_explanations[topic])
        
        # Add relationship explanation if relevant
        if 'versus' in relations or 'vs' in relations or 'compared to' in relations:
            response_parts.append(f"\n\nRegarding the relationship between {' and '.join(topics)}:")
            # Add specific relationship explanations for common comparisons
            if 'overfitting' in topics and 'underfitting' in topics:
                response_parts.append("Overfitting and underfitting are opposite problems in machine learning. Overfitting occurs when a model learns the training data too well and performs poorly on new data, while underfitting happens when the model is too simple and can't capture the underlying patterns in the data.")
            elif 'epoch' in topics and 'batch size' in topics:
                response_parts.append("While epochs and batch size are both training hyperparameters, they serve different purposes. An epoch represents a complete pass through the dataset, while batch size determines how many samples the model processes before updating its weights. They work together to control the training process and affect both training speed and model performance.")
        
        return ' '.join(response_parts)
    
    return None

def correct_ml_typos(text):
    """Correct common typos in ML terminology"""
    ml_terms = {
        'epoch': ['epco', 'epcho', 'epock', 'epoc', 'epoach'],
        'epochs': ['epcos', 'epchos', 'epocks', 'epocs', 'epoaches'],
        'accuracy': ['accurcy', 'accuraccy', 'acuracy', 'accurasy', 'acurracy'],
        'neural': ['nural', 'nueral', 'neurral', 'nurel'],
        'network': ['netwrk', 'netwerk', 'netwrok', 'nework'],
        'learning': ['learing', 'lerning', 'learnin', 'lernin'],
        'algorithm': ['algoritm', 'algorythm', 'algorthm', 'algorithem'],
        'regression': ['regresion', 'regressin', 'regresion', 'regresn'],
        'classification': ['clasification', 'clasiffication', 'classifcation'],
        'supervised': ['supervized', 'superviced', 'supervissed'],
        'unsupervised': ['unsupervized', 'unsuperviced', 'unsupervissed'],
        'reinforcement': ['reinforcment', 'reinforsment', 'reinforcemnt'],
        'gradient': ['gradiant', 'gradent', 'graident'],
        'descent': ['decent', 'desent', 'descant'],
        'backpropagation': ['backprop', 'backpropogation', 'backpropergation'],
        'overfitting': ['overfiting', 'overfitng', 'overffiting'],
        'underfitting': ['underfiting', 'underfitng', 'underffiting'],
        'hyperparameter': ['hyperparamter', 'hyper parameter', 'hyper-parameter'],
        'validation': ['validaton', 'validasion', 'validashun'],
        'training': ['trainning', 'trainin', 'traning'],
        'cnn': ['convnet', 'convolution network', 'convolutional network'],
        'rnn': ['recurrent network', 'recurent network'],
        'lstm': ['long short term memory', 'long short-term'],
        'gan': ['generative adversarial', 'generative network'],
        'transformer': ['transformers', 'transform model', 'attention model']
    }
    
    # Add acronym expansions
    acronyms = {
        'cnn': 'convolutional neural network',
        'rnn': 'recurrent neural network',
        'lstm': 'long short-term memory',
        'gan': 'generative adversarial network',
        'svm': 'support vector machine',
        'knn': 'k nearest neighbors',
        'pca': 'principal component analysis',
        'sgd': 'stochastic gradient descent',
        'mlp': 'multilayer perceptron',
        'dnn': 'deep neural network',
        'ai': 'artificial intelligence',
        'ml': 'machine learning',
        'dl': 'deep learning'
    }
    
    words = text.split()
    corrected_words = []
    
    for word in words:
        word_lower = word.lower()
        
        # Check if this is an acronym that needs expansion
        if word_lower in acronyms and len(words) <= 5:  # Only expand in short queries
            print(f"Expanding acronym: {word} -> {acronyms[word_lower]}")
            corrected_words.extend(acronyms[word_lower].split())
            continue
            
        # Check if this word is a known typo
        for correct_term, typos in ml_terms.items():
            if word_lower in typos:
                print(f"Corrected typo: {word} -> {correct_term}")
                corrected_words.append(correct_term)
                break
        else:
            # If not a known typo, check if it's close to any ML term
            close_matches = []
            for correct_term in ml_terms.keys():
                # Use difflib to find close matches
                similarity = difflib.SequenceMatcher(None, word_lower, correct_term).ratio()
                if similarity > 0.8:  # 80% similarity threshold
                    close_matches.append((correct_term, similarity))
            
            if close_matches:
                # Use the closest match
                best_match = max(close_matches, key=lambda x: x[1])
                print(f"Fuzzy correction: {word} -> {best_match[0]} (similarity: {best_match[1]:.2f})")
                corrected_words.append(best_match[0])
            else:
                # Keep the original word
                corrected_words.append(word)
    
    return ' '.join(corrected_words)

def find_intent(user_message):
    """Find the matching intent for the user message using a more robust algorithm"""
    user_message = user_message.lower().strip()
    
    # Print debug information
    print(f"\n=== Processing message: '{user_message}' ===")
    
    # Special handling for acronyms
    acronyms = {
        'cnn': 'convolutional neural network',
        'rnn': 'recurrent neural network',
        'lstm': 'long short-term memory',
        'gan': 'generative adversarial network',
        'bert': 'bidirectional encoder representations from transformers',
        'gpt': 'generative pre-trained transformer'
    }
    
    # Check if the query is just an acronym
    if user_message in acronyms or user_message.startswith('what is ' + user_message.split()[-1]) and user_message.split()[-1] in acronyms:
        acronym = user_message.split()[-1] if user_message.startswith('what is ') else user_message
        if acronym in acronyms:
            # Look for a matching intent tag
            for intent in intents_data['intents']:
                if intent['tag'].lower() == acronym.lower():
                    print(f"Direct acronym match: {acronym} -> {intent['tag']}")
                    return intent
    
    # 1. Direct handling for accuracy-related questions
    if 'accuracy' in user_message and ('low' in user_message or 'wrong' in user_message or 'improve' in user_message):
        print("Detected accuracy improvement question")
        return {
            "tag": "accuracy_improvement",
            "responses": [
                "To improve model accuracy: 1) Ensure you have enough quality training data, 2) Try different algorithms, 3) Perform feature engineering, 4) Tune hyperparameters, 5) Use ensemble methods, 6) Address class imbalance if present, 7) Consider regularization to prevent overfitting, and 8) Normalize your data if needed."
            ]
        }
    
    # 2. Analyze question complexity
    analysis = analyze_question_complexity(user_message)
    print(f"Question analysis: {analysis}")
    
    # 3. Handle compound questions
    if analysis['is_compound'] and len(analysis['topics']) >= 2:
        compound_response = generate_compound_response(analysis['topics'], analysis['relation_keywords'])
        if compound_response:
            print(f"Generated compound response for topics: {analysis['topics']}")
            return {
                'tag': 'compound_question',
                'responses': [compound_response]
            }
    
    # 4. Check for technical terms with expanded mapping
    technical_ml_terms = {
        'epoch': 'hyperparameter_tuning',
        'epochs': 'hyperparameter_tuning',
        'accuracy': 'model_evaluation',
        'learning rate': 'hyperparameter_tuning',
        'batch size': 'hyperparameter_tuning',
        'overfitting': 'overfitting',
        'underfitting': 'underfitting',
        'regularization': 'regularization',
        'dropout': 'regularization',
        'optimizer': 'optimization',
        'sgd': 'optimization',
        'adam': 'optimization',
        'cnn': 'cnn',
        'convolutional': 'cnn',
        'convolution': 'cnn',
        'rnn': 'rnn',
        'recurrent': 'rnn',
        'lstm': 'lstm',
        'gan': 'gan',
        'generative': 'gan',
        'transformer': 'transformer',
        'attention': 'transformer'
    }
    
    for term, intent_tag in technical_ml_terms.items():
        if term in user_message:
            # Find the corresponding intent
            for intent in intents_data['intents']:
                if intent.get('tag') == intent_tag:
                    print(f"Technical term match found: {term} -> {intent_tag}")
                    return intent
    
    # 5. Try exact pattern matches
    exact_matches = []
    for intent in intents_data['intents']:
        for pattern in intent['patterns']:
            pattern_lower = pattern.lower().strip()
            # Calculate exact match score
            if pattern_lower == user_message:
                print(f"Exact match found: {pattern_lower}")
                exact_matches.append((intent, 1.0))  # Perfect score
            elif pattern_lower in user_message or user_message in pattern_lower:
                # Calculate containment score
                containment_score = len(pattern_lower) / max(len(user_message), len(pattern_lower))
                exact_matches.append((intent, containment_score))
                print(f"Containment match found: {pattern_lower} (score: {containment_score:.2f})")
    
    if exact_matches:
        best_exact_match = max(exact_matches, key=lambda x: x[1])
        print(f"Best exact/containment match: {best_exact_match[0]['tag']} (score: {best_exact_match[1]:.2f})")
        return best_exact_match[0]
    
    # 6. Try word-level matching with improved scoring
    user_words = set(user_message.split())
    word_matches = []
    
    for intent in intents_data['intents']:
        best_pattern_score = 0
        best_pattern = None
        
        for pattern in intent['patterns']:
            pattern_lower = pattern.lower()
            pattern_words = set(pattern_lower.split())
            
            # Calculate word overlap
            common_words = user_words.intersection(pattern_words)
            
            if not common_words:
                continue
                
            # Calculate Jaccard similarity (intersection over union)
            if len(user_words.union(pattern_words)) > 0:
                similarity = len(common_words) / len(user_words.union(pattern_words))
                
                # Weight by the number of matching words and their importance
                score = similarity * (1 + len(common_words))
                
                # Boost score for important ML terms
                important_terms = ['machine', 'learning', 'neural', 'network', 'deep', 'supervised', 
                                  'unsupervised', 'reinforcement', 'classification', 'regression']
                for term in important_terms:
                    if term in common_words:
                        score *= 1.2  # 20% boost per important term
                
                # Boost score for longer common phrases (bigrams, trigrams)
                user_message_words = user_message.split()
                pattern_words_list = pattern_lower.split()
                
                for n in range(2, 4):  # Check for bigrams and trigrams
                    if len(user_message_words) >= n and len(pattern_words_list) >= n:
                        user_ngrams = [' '.join(user_message_words[i:i+n]) for i in range(len(user_message_words)-n+1)]
                        pattern_ngrams = [' '.join(pattern_words_list[i:i+n]) for i in range(len(pattern_words_list)-n+1)]
                        
                        common_ngrams = set(user_ngrams).intersection(set(pattern_ngrams))
                        if common_ngrams:
                            score *= (1 + 0.5 * len(common_ngrams))  # Boost for each common n-gram
                
                if score > best_pattern_score:
                    best_pattern_score = score
                    best_pattern = pattern
        
        if best_pattern_score > 0:
            word_matches.append((intent, best_pattern_score, best_pattern))
    
    # Sort word matches by score
    word_matches.sort(key=lambda x: x[1], reverse=True)
    
    # Print top matches for debugging
    print("\nTop word matches:")
    for i, (intent, score, pattern) in enumerate(word_matches[:3]):
        if i < len(word_matches):
            print(f"  {i+1}. {intent['tag']} (score: {score:.2f}, pattern: '{pattern}')")
    
    # Return the best match if it exceeds a minimum threshold
    if word_matches and word_matches[0][1] > 0.1:
        best_match = word_matches[0]
        print(f"Best word match: {best_match[0]['tag']} (score: {best_match[1]:.2f})")
        return best_match[0]
    
    # 7. Try fuzzy matching as a last resort
    fuzzy_matches = []
    
    for intent in intents_data['intents']:
        best_fuzzy_score = 0
        best_fuzzy_pattern = None
        
        for pattern in intent['patterns']:
            pattern_lower = pattern.lower()
            ratio = difflib.SequenceMatcher(None, user_message, pattern_lower).ratio()
            
            if ratio > best_fuzzy_score:
                best_fuzzy_score = ratio
                best_fuzzy_pattern = pattern
        
        if best_fuzzy_score > 0:
            fuzzy_matches.append((intent, best_fuzzy_score, best_fuzzy_pattern))
    
    # Sort fuzzy matches by score
    fuzzy_matches.sort(key=lambda x: x[1], reverse=True)
    
    # Print top fuzzy matches for debugging
    print("\nTop fuzzy matches:")
    for i, (intent, score, pattern) in enumerate(fuzzy_matches[:3]):
        if i < len(fuzzy_matches):
            print(f"  {i+1}. {intent['tag']} (score: {score:.2f}, pattern: '{pattern}')")
    
    # Return the best fuzzy match if it exceeds a minimum threshold
    if fuzzy_matches and fuzzy_matches[0][1] > 0.6:
        best_match = fuzzy_matches[0]
        print(f"Best fuzzy match: {best_match[0]['tag']} (score: {best_match[1]:.2f})")
        return best_match[0]
    
    # 8. Check for general ML-related keywords as fallback
    ml_keywords = ['machine learning', 'neural', 'ai', 'ml', 'deep learning', 'algorithm', 
                  'model', 'train', 'data', 'supervised', 'unsupervised', 'classification']
    
    if any(keyword in user_message for keyword in ml_keywords):
        # Find the most general ML intent as fallback
        for intent in intents_data['intents']:
            if intent['tag'] == 'machine_learning_basics':
                print(f"Falling back to ML basics")
                return intent
    
    # 9. No good match found - use fallback intent
    print("No match found, using fallback response")
    return {
        "tag": "fallback",
        "responses": [
            "I'm not sure I understand that question about machine learning. Could you rephrase it or ask about a specific ML concept like neural networks, deep learning, or supervised learning?",
            "I don't have enough information to answer that question accurately. Could you provide more details or ask about a specific machine learning topic?",
            "I'm still learning and don't have a good answer for that question yet. I can help with topics like neural networks, supervised learning, or model evaluation if you're interested."
        ]
    }

def get_response(intent, user_message=None):
    """Get a response from the intent with enhanced conversational elements"""
    if not intent or 'responses' not in intent:
        return "I'm not sure I understand that question. Could you ask me something about machine learning concepts like neural networks, deep learning, or supervised learning?"
    
    # Get a random response from the intent
    response = random.choice(intent['responses'])
    
    # Add conversational elements based on intent type
    if intent['tag'] == 'greeting':
        # For greetings, add a follow-up question
        follow_ups = [
            " What would you like to know about machine learning today?",
            " Is there a specific ML concept you're curious about?",
            " I can help with topics like neural networks, deep learning, or supervised learning. What interests you?"
        ]
        response += random.choice(follow_ups)
    
    elif intent['tag'] == 'thanks':
        # For thanks, add an offer to help more
        follow_ups = [
            " Is there anything else you'd like to know?",
            " Feel free to ask if you have more questions!",
            " I'm happy to explain other ML concepts if you're interested."
        ]
        response += random.choice(follow_ups)
    
    elif user_message and len(user_message.split()) > 3:
        # For longer, more complex questions, add an encouragement or acknowledgment
        acknowledgments = [
            "That's a great question! ",
            "I'm glad you asked about this. ",
            "Excellent question! ",
            "This is an important concept in ML. "
        ]
        
        # Only add acknowledgment sometimes to keep it natural (50% chance)
        if random.random() > 0.5:
            response = random.choice(acknowledgments) + response
    
    return response

def log_interaction(user_message, corrected_message, intent_tag, response, is_compound=False):
    """Log each interaction with the chatbot"""
    interaction_data = {
        'timestamp': datetime.now().isoformat(),
        'user_message': user_message,
        'corrected_message': corrected_message if corrected_message != user_message else None,
        'intent_tag': intent_tag,
        'is_compound_question': is_compound,
        'response': response
    }
    
    # Log to file
    logging.info(json.dumps(interaction_data))
    
    # Save to interactions history file
    try:
        with open('interactions_history.jsonl', 'a') as f:
            f.write(json.dumps(interaction_data) + '\n')
    except Exception as e:
        logging.error(f"Failed to save interaction history: {str(e)}")

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
        # Log the raw user message
        print(f"\n=== New chat request ===")
        print(f"Raw user message: '{user_message}'")
        
        # Correct typos in the user message
        corrected_message = correct_ml_typos(user_message)
        if corrected_message != user_message:
            print(f"Corrected message: '{corrected_message}'")
        
        # Analyze question complexity
        analysis = analyze_question_complexity(corrected_message)
        
        # Find matching intent using the corrected message
        intent = find_intent(corrected_message)
        
        # Get response based on intent
        if intent:
            response = get_response(intent, corrected_message)
            is_ml_related = True
            
            # Log the successful interaction
            log_interaction(
                user_message=user_message,
                corrected_message=corrected_message,
                intent_tag=intent.get('tag'),
                response=response,
                is_compound=analysis['is_compound']
            )
            
            print(f"Response (intent: {intent.get('tag')}): {response[:100]}...")
        else:
            # This should never happen now with our fallback intent
            response = "I'm sorry, I couldn't understand your question. Please try asking about a specific machine learning topic."
            is_ml_related = False
            
            # Log the failed interaction
            log_interaction(
                user_message=user_message,
                corrected_message=corrected_message,
                intent_tag='unknown',
                response=response,
                is_compound=analysis['is_compound']
            )
            
            print(f"No intent found, using default response")
        
        return jsonify({
            'is_ml_related': is_ml_related,
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

@app.route('/service-worker.js')
def service_worker():
    # Simple service worker for PWA support
    return """
    self.addEventListener('install', function(event) {
        event.waitUntil(
            caches.open('ml-chatbot-v1').then(function(cache) {
                return cache.addAll([
                    '/',
                    '/api/chat'
                ]);
            })
        );
    });

    self.addEventListener('fetch', function(event) {
        event.respondWith(
            caches.match(event.request).then(function(response) {
                return response || fetch(event.request);
            })
        );
    });
    """

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads containing questions"""
    if 'file' not in request.files:
        return jsonify({
            'error': 'No file part'
        }), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            'error': 'No selected file'
        }), 400
        
    try:
        # Process different file types
        filename = file.filename.lower()
        content = file.read().decode('utf-8')
        
        # Process based on file type
        if filename.endswith('.txt'):
            # Process as plain text file with one question per line
            questions = [line.strip() for line in content.split('\n') if line.strip()]
        elif filename.endswith('.csv'):
            # Process as CSV file, assuming first column contains questions
            import csv
            from io import StringIO
            questions = []
            csv_reader = csv.reader(StringIO(content))
            for row in csv_reader:
                if row and row[0].strip():
                    questions.append(row[0].strip())
        elif filename.endswith('.json'):
            # Process as JSON file, expecting an array of questions or objects with a 'question' field
            import json
            data = json.loads(content)
            questions = []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        questions.append(item)
                    elif isinstance(item, dict) and 'question' in item:
                        questions.append(item['question'])
        else:
            return jsonify({
                'error': 'Unsupported file type. Please upload .txt, .csv, or .json files.'
            }), 400
            
        # Limit the number of questions to process
        MAX_QUESTIONS = 10
        if len(questions) > MAX_QUESTIONS:
            truncated_message = f"File contains {len(questions)} questions. Processing only the first {MAX_QUESTIONS}."
            questions = questions[:MAX_QUESTIONS]
        else:
            truncated_message = None
            
        if not questions:
            return jsonify({
                'error': 'No valid questions found in the file.'
            }), 400
            
        # Process the first question as the main response
        first_question = questions[0]
        
        # Find intent for the first question
        corrected_message = correct_ml_typos(first_question)
        intent = find_intent(corrected_message)
        
        if intent:
            main_response = get_response(intent, corrected_message)
            
            # Log the interaction
            log_interaction(
                user_message=first_question,
                corrected_message=corrected_message,
                intent_tag=intent.get('tag'),
                response=main_response
            )
        else:
            main_response = "I couldn't understand the first question in your file. Please try rephrasing it."
            
        # Process additional questions if any
        additional_responses = []
        if len(questions) > 1:
            for question in questions[1:]:
                if question:
                    corrected = correct_ml_typos(question)
                    q_intent = find_intent(corrected)
                    if q_intent:
                        resp = get_response(q_intent, corrected)
                        additional_responses.append(f"Q: {question}\nA: {resp}")
                        
                        # Log each interaction
                        log_interaction(
                            user_message=question,
                            corrected_message=corrected,
                            intent_tag=q_intent.get('tag'),
                            response=resp
                        )
        
        # Prepare the response
        response_text = main_response
        if truncated_message:
            response_text = f"{truncated_message}\n\nFirst question: {first_question}\n{response_text}"
            
        return jsonify({
            'response': response_text,
            'additional_responses': additional_responses,
            'total_questions': len(questions)
        })
        
    except Exception as e:
        logging.error(f"Error processing uploaded file: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error processing file: {str(e)}'
        }), 500

if __name__ == "__main__":
    print("Starting ML Chatbot server on http://localhost:5000")
    try:
        # Run with debug=True to see errors, but use threaded=True for better performance
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    except Exception as e:
        print(f"Error starting server: {e}") 