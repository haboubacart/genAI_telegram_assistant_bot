from telegram import Update
from telegram.ext import (
    ContextTypes,
    CallbackContext
)


# Cette fonction sera appelée chaque fois qu'un message vocal est reçu
async def save_voice_message(update: Update, context: CallbackContext):
    file = await  context.bot.get_file(update.message.voice.file_id)
    filepath = f"./voice_messages/{update.message.voice.file_id}.wav"
    await file.download_to_drive(filepath)  
    #await update.message.reply_text("Message audio enregistré !")
    return filepath

async def reply_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) : 
     await update.message.reply_text("Hello, comment ça va ?")
