from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI()

load_dotenv()

def get_whisper_transcription(path: str):

    try:
        audio_file = open(f"{path}", "rb")
        transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
        )
        output = transcription
    except Exception as e:
        output = f"Error in whisper.py: {e}"
    
    return output