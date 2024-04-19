import ollama
from typing import List

def get_response(messages: List, model: str = 'wizardlm2'):
    output = ""
    try:
        response = ollama.chat(model=model, messages=messages)
        output = response['message']['content']
    except Exception as e:
        output = f"Error in model_modules/ollama_main: {e}"
        return f"Error in model_modules/ollama_main: {e}"
    return output
