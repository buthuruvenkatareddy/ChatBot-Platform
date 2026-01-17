"""
OpenRouter API integration service
"""
import requests
from django.conf import settings


def call_openrouter_api(system_prompt, messages):
    """
    Call OpenRouter API with system prompt and chat history
    
    Args:
        system_prompt (str): The agent's system prompt
        messages (list): List of message dicts with 'role' and 'content'
    
    Returns:
        str: AI response content
    """
    api_key = settings.OPENROUTER_API_KEY
    api_url = settings.OPENROUTER_API_URL
    
    # List of free models to try in order
    free_models = [
        'meta-llama/llama-3.2-3b-instruct:free',
        'google/gemini-2.0-flash-exp:free',
        'mistralai/mistral-7b-instruct:free',
        'nousresearch/hermes-3-llama-3.1-405b:free',
        'qwen/qwen-2-7b-instruct:free'
    ]
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not configured")
    
    # Prepare messages with system prompt
    api_messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    # Add chat history (limit to last 10 messages to avoid token limits)
    api_messages.extend(messages[-10:])
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Chatbot Platform"
    }
    
    last_error = None
    
    # Try each model until one works
    for model in free_models:
        payload = {
            "model": model,
            "messages": api_messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            
            # Check for errors
            if response.status_code == 200:
                data = response.json()
                
                # Extract the assistant's message
                if 'choices' in data and len(data['choices']) > 0:
                    return data['choices'][0]['message']['content']
            else:
                # Log error and try next model
                error_data = response.json() if response.content else {}
                error_msg = error_data.get('error', {}).get('message', response.text)
                last_error = f"Model {model} failed ({response.status_code}): {error_msg}"
                continue
                
        except Exception as e:
            last_error = f"Model {model} failed: {str(e)}"
            continue
    
    # If all models failed, raise the last error
    raise Exception(f"All models failed. Last error: {last_error}")
