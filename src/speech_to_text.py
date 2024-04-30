from google.cloud import speech

def transcribe_voice(file_path):
    client = speech.SpeechClient()
    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000,
            enable_automatic_punctuation=True,
            audio_channel_count=1,
            language_code="fr-FR",
            model='phone_call'
        )
    response = client.recognize(config=config, audio=audio)
    results = ""
    for result in response.results:
        results += result.alternatives[0].transcript
    return results