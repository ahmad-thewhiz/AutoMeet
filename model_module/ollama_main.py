import ollama

def get_response(prompts: str, model: str = 'wizardlm2'):
    output = ""
    try:
        response = ollama.chat(model=model, messages=[
            {
                'role': 'user',
                'content': f'{prompts}',
            },
        ])
        output = response['message']['content']
    except Exception as e:
        output = f"Error in model_modules/ollama_main: {e}"
        return f"Error in model_modules/ollama_main: {e}"
    return output
