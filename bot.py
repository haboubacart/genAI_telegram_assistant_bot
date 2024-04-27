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
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Cette fonction sera appelée chaque fois qu'un message vocal est reçu
async def save_voice_message(update: Update, context: CallbackContext):
    file = await  context.bot.get_file(update.message.voice.file_id)
    filepath = f"voice_messages/{update.message.voice.file_id}.ogg"
    await file.download_to_drive(filepath)  
    await update.message.reply_text("Message audio enregistré !")

async def reply_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) : 
     await update.message.reply_text("Hello, comment ça va ?")
    
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, save_voice_message))
    app.add_handler(MessageHandler(filters.TEXT, reply_text_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    if not os.path.exists("voice_messages"):
        os.makedirs("voice_messages")
    print("starting telegram bot...")
    main()    


