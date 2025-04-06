import os
import json
import requests
import logging
import datetime
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatgpt_api.log'),
        logging.StreamHandler()
    ]
)

class ChatGPTHandler:
    """
    A class to handle interactions with the OpenAI ChatGPT API.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the ChatGPT handler.
        
        Args:
            api_key (str, optional): The OpenAI API key. Defaults to None.
        """
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"  # Can be changed to "gpt-4" if available
        self.conversation_history = []
        self.max_history = 10  # Maximum number of messages to keep in history
        
        # System prompt that defines the chatbot's role
        self.system_prompt = {
            "role": "system",
            "content": """You are an AI assistant specialized in machine learning and data science. 
            Your purpose is to provide accurate, educational information about machine learning concepts, 
            algorithms, techniques, and best practices. 
            
            You should:
            - Provide clear, concise explanations of ML concepts
            - Include relevant examples when helpful
            - Explain complex ideas in an accessible way
            - Cite common libraries or tools used for implementing specific techniques
            - Correct misconceptions politely
            - Acknowledge when topics are debated in the field
            
            You should NOT:
            - Provide information on harmful or unethical applications of ML
            - Make up information if you're unsure
            - Provide personal opinions on controversial topics
            - Answer questions that are completely unrelated to machine learning or data science
            
            If asked about topics outside of machine learning and data science, politely redirect 
            the conversation back to ML-related topics.
            """
        }
        
        # Add system prompt to conversation history
        self.conversation_history.append(self.system_prompt)
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
    
    def get_response(self, user_message: str) -> str:
        """
        Get a response from the ChatGPT API.
        
        Args:
            user_message (str): The user's message.
            
        Returns:
            str: The response from ChatGPT.
        """
        if not self.api_key:
            return "Please provide an OpenAI API key to use this service."
        
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare the messages for the API call
        messages = self.conversation_history[-self.max_history:]
        
        try:
            # Make the API call
            response = requests.post(
                self.api_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1000,
                    "top_p": 1.0,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0
                },
                timeout=30  # 30 second timeout
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Parse the response
            response_data = response.json()
            
            # Extract the assistant's message
            assistant_message = response_data["choices"][0]["message"]["content"]
            
            # Add assistant message to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Log the interaction
            self._log_interaction(user_message, assistant_message)
            
            return assistant_message
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error communicating with OpenAI API: {str(e)}"
            logging.error(error_msg)
            
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    if 'error' in error_data:
                        error_msg = f"OpenAI API Error: {error_data['error']['message']}"
                except:
                    pass
            
            return f"Sorry, I encountered an error: {error_msg}"
        
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logging.error(error_msg)
            return f"Sorry, I encountered an unexpected error. Please try again later."
    
    def reset_conversation(self) -> str:
        """
        Reset the conversation history.
        
        Returns:
            str: A message indicating the conversation has been reset.
        """
        # Keep only the system prompt
        self.conversation_history = [self.system_prompt]
        return "Conversation has been reset."
    
    def _log_interaction(self, user_message: str, assistant_message: str) -> None:
        """
        Log the interaction between the user and the assistant.
        
        Args:
            user_message (str): The user's message.
            assistant_message (str): The assistant's response.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "user_message": user_message,
            "assistant_message": assistant_message
        }
        
        # Log to file
        log_file = os.path.join('logs', f"chat_log_{datetime.datetime.now().strftime('%Y-%m-%d')}.jsonl")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')

# Example usage
if __name__ == "__main__":
    # This is just for testing
    handler = ChatGPTHandler(api_key="your_api_key_here")
    response = handler.get_response("What is machine learning?")
    print(response) 