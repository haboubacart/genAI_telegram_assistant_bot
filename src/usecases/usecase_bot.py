from telegram import Update
from telegram.ext import CallbackContext
from src.google.speech_to_text import transcribe_voice
from src.telegram_bot.bot import save_voice_message
from src.chatgpt.chatgpt import response_to_query
from src.chatgpt.prompts import get_qa_prompt
from src.google.google_calandar import create_calandar_event
from src.google.google_calandar import get_creds
from googleapiclient.discovery import build
import json

async def reply_voice_message(update: Update, context: CallbackContext):
    audio_filepath =  await save_voice_message(update, context)
    audio_to_text = transcribe_voice(audio_filepath)
    reponse_gpt = execute_action(response_to_query(get_qa_prompt(), audio_to_text))
    print(audio_to_text)
    print(json.dumps(reponse_gpt), 2)    
    await update.message.reply_text( f"Vous avez dit : \n{audio_to_text}\nCorrection par GPT\n{reponse_gpt}")


async def reply_text_message(update: Update, context: CallbackContext) : 
    message = update.message.text
    print("votre msessage : ", message)
    gpt = response_to_query(get_qa_prompt(), message)
    reponse_gpt = execute_action(gpt)

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


