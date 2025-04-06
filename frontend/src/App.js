import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './App.css';
import mlLogo from './assets/ml-logo.png';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Add initial welcome message
  useEffect(() => {
    setMessages([
      {
        type: 'bot',
        content: "👋 Welcome to ML Chatbot! I'm specialized in answering questions about machine learning concepts and related topics. What would you like to know about machine learning today?"
      }
    ]);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    // Add user message to chat
    const userMessage = { type: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    
    // Clear input field
    setInput('');
    
    // Show loading indicator
    setIsLoading(true);
    
    try {
      // Send request to backend
      const response = await axios.post('/api/chat', { message: userMessage.content });
      
      // Add bot response to chat
      const botMessage = { 
        type: 'bot', 
        content: response.data.response,
        isML: response.data.is_ml_related
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to chat
      const errorMessage = { 
        type: 'bot', 
        content: "Sorry, I encountered an error processing your request. Please try again.",
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={mlLogo} className="App-logo" alt="ML Chatbot Logo" />
        <h1>ML Chatbot</h1>
        <p>Your AI assistant for machine learning concepts</p>
      </header>
      
      <main className="chat-container">
        <div className="messages-container">
          {messages.map((message, index) => (
            <div 
              key={index} 
              className={`message ${message.type} ${message.isError ? 'error' : ''} ${message.type === 'bot' && !message.isML && !message.isError ? 'not-ml' : ''}`}
            >
              <div className="message-content">
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message bot loading">
              <div className="loading-indicator">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        <form className="input-form" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a machine learning question..."
            className="message-input"
          />
          <button type="submit" className="send-button" disabled={isLoading || !input.trim()}>
            Send
          </button>
        </form>
      </main>
      
      <footer className="App-footer">
        <p>ML Chatbot - Specialized in machine learning concepts</p>
      </footer>
    </div>
  );
}

export default App; 