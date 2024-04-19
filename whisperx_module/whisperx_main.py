import whisperx
import gc 

def get_transcription(path: str):
    device = "cpu" 
    audio_file = path
    batch_size = 8
    compute_type = "int8"

    output = ""
    try:
        model = whisperx.load_model("large-v2", device, compute_type=compute_type)

        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio, batch_size=batch_size)
        output = result["segments"]
        del model
    except Exception as e:
        output = f"Error in whisperx_main.get_transcription: {e}"
    return output