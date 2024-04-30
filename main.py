from telegram import Update
from telegram.ext import (
    MessageHandler,
    ApplicationBuilder,
    CallbackContext,
    filters,
)
from dotenv import load_dotenv
from src.speech_to_text import transcribe_voice
from src.bot import save_voice_message
from src.chatgpt import response_to_query
import os
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
speech_key = os.getenv("SPEECH_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = speech_key


async def reply_voice_message(update: Update, context: CallbackContext):
    audio_filepath = await save_voice_message(update, context)
    audio_to_text = transcribe_voice(audio_filepath)
    reponse_gpt = response_to_query(audio_to_text)["reponse"]
    print(audio_to_text)
    print(reponse_gpt)    
    await update.message.reply_text( f"Vous avez dit : \n{audio_to_text}\nCorrection par GPT\n{reponse_gpt}")


async def reply_text_message(update: Update, context: CallbackContext) : 
     message = update.message.text
     reponse_gpt = response_to_query(message)["reponse"]
     print(message)
     print(reponse_gpt)
     await update.message.reply_text(f"Votre assistant : \n{reponse_gpt}")

def action_sheduling():
    pass

def action_summarizing():
    pass

def execute_action(action_json):
    """Cette fonction execute l'action specifier dans le json. 

    Args:
        action_json (_type_): _description_
    """

 
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, reply_voice_message))
    app.add_handler(MessageHandler(filters.TEXT, reply_text_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    if not os.path.exists("voice_messages"):
        os.makedirs("voice_messages")
    print("starting telegram bot...")
    main()
    #print(transcribe_voice("voice_messages/test2.wav"))
