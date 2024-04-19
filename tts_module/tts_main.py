import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

def get_audio(prompt: str, description: str, speaker: str): 
    device = "cuda:5" if torch.cuda.is_available() else "cpu"

    try:
        model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler_tts_mini_v0.1").to(device)
        tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler_tts_mini_v0.1")

        input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
        prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

        generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
        audio_arr = generation.cpu().numpy().squeeze()
        sf.write(f"{speaker}.wav", audio_arr, model.config.sampling_rate)

        del model, tokenizer
    
    except Exception as e:
        print(f"Error in tts_main/get_audio: {e}")
        return f"Error in tts_main/get_audio: {e}"