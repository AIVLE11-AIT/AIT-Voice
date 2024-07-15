import whisper

def whisper_inference(audio_file):
    audio = whisper.load_audio(audio_file)

    model = whisper.load_model("medium", device='cpu')
    result = model.transcribe(audio)
    
    return result['language'], result['text']
