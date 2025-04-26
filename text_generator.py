"""
Text generation module for the Video Modification Bot.
Handles generating motivational, fun, and philosophical text using Ollama's DeepSeek model.
"""

import os
import requests
import json
from typing import Optional
import config
import re

def generate_text(prompt: str = config.TEXT_PROMPT, model: str = config.TEXT_MODEL) -> Optional[str]:
    """
    Generate text using Ollama with a local model.
    
    Args:
        prompt: The prompt to send to the language model
        model: The model name to use (defaults to config.TEXT_MODEL)
        
    Returns:
        Generated text or None if generation fails
    """
    try:
        print(f"Using Ollama with model: {model}")
        
        # Let's try a more direct prompt that skips the thinking
        direct_prompt = "Create one short, motivational quote (higher than 200 characters and under 500 characters). Don't include any explanations, just the quote."
        
        # Try with the chat API first since it tends to follow instructions better
        return generate_text_with_chat(direct_prompt, model)
        
    except Exception as e:
        print(f"Error generating text: {e}")
        # Return a default quote as fallback
        default_quote = "Every journey begins with a single step. The path to success is paved with small victories."
        print(f"Using default quote as fallback: {default_quote}")
        return default_quote

def generate_text_with_chat(prompt: str, model: str) -> Optional[str]:
    """
    Generate text using Ollama's chat API.
    """
    try:
        print("Using chat API for text generation...")
        api_url = f"{config.OLLAMA_API_BASE}/api/chat"
        request_data = {
            "model": model,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a creative writer who specializes in short, impactful motivational quotes. Always respond with ONLY the quote, no explanations."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.7
            }
        }
        
        print(f"Sending request to: {config.OLLAMA_API_BASE}/api/chat")
        
        response = requests.post(
            api_url,
            json=request_data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"Error from Ollama Chat API: {response.status_code} - {response.text}")
            return None
        
        response_json = response.json()
        message = response_json.get("message", {})
        generated_text = message.get("content", "").strip()
        
        # Clean up the text - extract just the quote
        # Remove any thinking tags
        if '<think>' in generated_text:
            # Remove everything between <think> and </think> tags
            generated_text = re.sub(r'<think>.*?</think>', '', generated_text, flags=re.DOTALL).strip()
        
        # If there are quotes in the text, try to extract just the quoted part
        quote_match = re.search(r'"([^"]*)"', generated_text)
        if quote_match:
            generated_text = quote_match.group(1).strip()
        
        # If the text is too long or empty, use a default quote
        if not generated_text or len(generated_text) > 150:
            default_quotes = [
                "Life isn't about finding yourself; it's about creating yourself.",
                "The best way to predict the future is to create it.",
                "Every mountain top is within reach if you just keep climbing.",
                "Stars can't shine without darkness.",
                "Dream big, stay positive, work hard, and enjoy the journey."
            ]
            import random
            generated_text = random.choice(default_quotes)
            print(f"Using random default quote: {generated_text}")
        else:
            print(f"Generated text from API: {generated_text}")
            
        return generated_text
        
    except Exception as e:
        print(f"Error generating text with chat API: {e}")
        
        # Last resort: return a default quote
        default_quote = "Every journey begins with a single step. The path to success is paved with small victories."
        print(f"Using default quote as fallback: {default_quote}")
        return default_quote

# For testing
if __name__ == "__main__":
    text = generate_text()
    if text:
        print(f"Final quote: {text}")
        print(f"Character count: {len(text)}")
    else:
        print("Failed to generate text.")
