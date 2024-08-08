from openai import OpenAI


OPENAI_API_KEY = "sk-proj-b2x05FmtNy1Q2cfocAUGT3BlbkFJvmLMXpUHJM5TXCyb7o95"


def whisper_inference(audio_file):
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    audio_file = open(audio_file, "rb")
    translation  = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
    )

    return translation.language, translation.text
