from openai import OpenAI


OPENAI_API_KEY = "your_key"


def whisper_inference(audio_file):
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    audio_file = open(audio_file, "rb")
    translation  = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
    )

    return translation.language, translation.text
