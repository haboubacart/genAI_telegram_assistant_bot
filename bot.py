from telegram import Update
from telegram.ext import (
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    filters,
    CallbackContext
)
import os
from dotenv import load_dotenv
from google.cloud import speech

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
speech_key = os.getenv("SPEECH_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = speech_key

# Cette fonction sera appelée chaque fois qu'un message vocal est reçu
async def save_voice_message(update: Update, context: CallbackContext):
    file = await  context.bot.get_file(update.message.voice.file_id)
    filepath = f"voice_messages/{update.message.voice.file_id}.wav"
    await file.download_to_drive(filepath)  
    await update.message.reply_text("Message audio enregistré !")

async def reply_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) : 
     await update.message.reply_text("Hello, comment ça va ?")

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
        language_code="fr-FR",  # Changez ceci en fonction de la langue du fichier vocal
        model='phone_call'
    )
    # Envoie la requête pour la transcription
    response = client.recognize(config=config, audio=audio)
    # Récupère les résultats de la transcription
    results = ""
    for result in response.results:
        results += result.alternatives[0].transcript
        
    return results

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, save_voice_message))
    app.add_handler(MessageHandler(filters.TEXT, reply_text_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    if not os.path.exists("voice_messages"):
        os.makedirs("voice_messages")
    print("starting telegram bot...")
    #main()
    print(transcribe_voice("voice_messages/test2.wav"))


