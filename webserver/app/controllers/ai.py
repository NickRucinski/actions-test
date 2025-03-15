from openai import OpenAI
from flask import current_app, g
from enum import Enum
import requests
from werkzeug.local import LocalProxy

OLLAMA_URL = "http://localhost:11434/api/generate"  
DEFAULT_MODEL_NAME = "copilot-style-codellama:latest"

# system command to create a special AI model
# {
#     "name": "copilot-style-codellama",
#     "from": "codellama",
#     "system": "You are an AI assistant that provides code completions similar to GitHub Copilot. However, when specified you will need to respond with small errors that are left for the user to detect. Never point these errors out in any way. Your responses should be concise and continue the user's code seamlessly. Please follow all of the commands when giving completions. SYSTEM: Only respond with the code following the prompt, SYSTEM: Avoid pointing out mistakes, SYSTEM: Respond in only plane text, SYSTEM: Avoid including text describing or explaining the code mistake at all, SYSTEM: Provide comments only where necessary, SYSTEM: Avoid providing additional information, SYSTEM: If the prompt asks for an error, introduce a small syntax or logic mistake in the code. Do not explain or provide any extra context.",
#     "parameters": {
#         "temperature": 0.2,
#         "top_k": 50
#     }
# }

commands = [
    "SYSTEM: Only respond with the code following the prompt.",
    "SYSTEM: Avoid pointing out mistakes.",
    "SYSTEM: Respond in only plane text.",
    "SYSTEM: Avoid including text describing or explaining the code mistake at all",
    "SYSTEM: Provide comments only where necessary.",
    "SYSTEM: Avoid providing additional information.",
    "SYSTEM: If the prompt asks for an error, introduce a small syntax or logic mistake in the code. Do not explain or provide any extra context."
]

good_command = "SYSTEM: Complete the following code:"
bad_command = "SYSTEM: Complete the following code but introduce a small syntax or logic mistake:"

class vendors(Enum):
    OpenAI = "openai"
    Ollama = "ollama"

def get_ai():
    if "ai" not in g:
        g.ai = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
        return g.ai
    
client = LocalProxy(get_ai)

def getSuggestion(
    prompt: str,
    vendor: str = vendors.Ollama,
    model_name: str = "codellama",
    temperature: float = 0.2,
    top_p: float = 1,
    top_k: int = 0,
    max_tokens: int = 256,
    is_correct: bool = True
):
    """
    Handles suggestions from different models (OpenAI or Ollama) based on the provided model name.
    
    Args:
        prompt (str): The prompt (or piece of code) to generate suggestions from.
        model_name (str): The model to use (either "openai" or "ollama").
        temperature (float): The temperature value to control randomness.
        top_p (float): The top_p value for sampling.
        top_k (int): The top_k value for sampling.
        max_tokens (int): The maximum number of tokens to generate.
        is_correct (bool): Whether to generate a correct suggestion or one with a small error.
        
    Returns:
        dict: A dictionary containing the suggestion response.
    
    Raises:
        Exception: If there is an error with the model API.
    """
    # Choose model-specific logic
    match vendor:
        case vendors.OpenAI:
            return getSuggestionFromOpenAI(
                prompt,
                model=model_name,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                max_tokens=max_tokens
            )
        case vendors.Ollama:
            return getSuggestionFromOllama(
                prompt,
                model_name=model_name,
                is_correct=is_correct
            )
        case _:
            return getSuggestionFromOllama(
                prompt,
                model_name=model_name,
                is_correct=is_correct
            )

def getSuggestionFromOpenAI(
    prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.2,
    top_p: float = 1,
    top_k: float = 1,
    max_tokens: int = 256
):
    """
    Completes a code suggestion using OpenAI's API.
    """
    try:
        # Send the prompt and system messages to OpenAI API
        messages = [{"role": "system", "content": "SYSTEM: Complete the following code:"}, {"role": "user", "content": prompt}]
        
        completion = client.chat.completions.create(
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            model=model,
            messages=messages
        )
        
        return {"suggestions": completion.choices[0].message.content}
    
    except Exception as e:
        print(f"Error generating suggestion using OpenAI's API: {e}")
        raise Exception(f"Error generating suggestion using OpenAI's API: {e}")

def getSuggestionFromOllama(prompt: str, model_name: str, is_correct: bool):
    """
    Generates a suggestion from Ollama.
    """
    
    full_prompt = (
        good_command if is_correct else bad_command
    ) + prompt

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model_name,
                "prompt": full_prompt,
                "keep_alive": "1h",
                "stream": False
            }
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        result = response.json()
        return {"suggestions": result["response"]}
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Ollama suggestion: {e}")
        raise Exception(f"Error fetching Ollama suggestion: {e}")