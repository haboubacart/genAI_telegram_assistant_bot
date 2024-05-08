from telegram import Update
from telegram.ext import (
    MessageHandler,
    Updater,
    ApplicationBuilder,
    CallbackContext,
    filters,
)
from dotenv import load_dotenv
from src.speech_to_text import transcribe_voice
from src.bot import save_voice_message
from src.chatgpt import response_to_query
from src.google_calandar import get_calandar_events
from src.google_calandar import create_calandar_event
from src.google_calandar import get_creds
from googleapiclient.discovery import build


import os
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
speech_key = os.getenv("SPEECH_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = speech_key

import json
async def reply_voice_message(update: Update, context: CallbackContext):
    audio_filepath =  await save_voice_message(update, context)
    audio_to_text = transcribe_voice(audio_filepath)
    reponse_gpt = execute_action(response_to_query(audio_to_text))
    print(audio_to_text)
    print(json.dumps(reponse_gpt), 2)    
    await update.message.reply_text( f"Vous avez dit : \n{audio_to_text}\nCorrection par GPT\n{reponse_gpt}")


async def reply_text_message(update: Update, context: CallbackContext) : 
     message = update.message.text
     reponse_gpt = execute_action(response_to_query(message))
     print(message)
     print(json.dumps(reponse_gpt, indent=2))
     await update.message.reply_text(f"Votre assistant : \n{reponse_gpt}")


def execute_action(action_json):
    """Cette fonction execute l'action specifier dans le json. 

    Args:
        action_json (_type_): _description_
    """
    if action_json["action"] == "schedule_learning":
        creds = get_creds()
        service = build("calendar", "v3", credentials=creds)
        event_object = {
        "title" : action_json["titre"],
        "description" : action_json["description"],
        "datetime_debut": "2024-05-04T15:00:00+02:00",
        "duree" : action_json["duree"],
        }
        scheduling_status = create_calandar_event(service, event_object)
        if scheduling_status and scheduling_status == "confirmed":
            print("Apprentissage programmé avec succès")
    
    return action_json["reponse"]

async def error_handler(update: Update, context: CallbackContext):
    print(f"An error occurred: {context.error}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()
    app.add_handler(MessageHandler(filters.VOICE, reply_voice_message))
    app.add_handler(MessageHandler(filters.TEXT, reply_text_message))
    print("starting telegram bot...", flush=True)
    app.add_error_handler(error_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    

if __name__ == "__main__":

    if not os.path.exists("voice_messages"):
        os.makedirs("voice_messages")
    main()
    #print(transcribe_voice("voice_messages/test2.wav"))
