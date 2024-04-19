import os
from dotenv import load_dotenv
from typing import List
from openai import OpenAI

load_dotenv()

client = OpenAI()

def get_response(messages: List, model: str = "gpt-3.5-turbo-0125"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages)
        output = response.choices[0].message.content
    except Exception as e:
        output = f"Error in model_module/openai_main: {e}"

    return output
