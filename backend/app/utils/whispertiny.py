from transformers import pipeline
# import the openai pipeline
whisper = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en")

def transcribe_text(file_content):
    # input the uploaded audio file into the ml model
    text = whisper(file_content)
    return text