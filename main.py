import os
from config import (BOT_TOKEN,
                    NOTION_TOKEN,
                    SPEECH_KEY)

from src.usecases.usecase_bot import (reply_voice_message,
                        reply_text_message,
                        error_handler)

from telegram import Update
from telegram.ext import (
    MessageHandler,
    Updater,
    ApplicationBuilder,
    CallbackContext,
    filters,
)
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