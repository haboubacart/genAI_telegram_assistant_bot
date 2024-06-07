from dotenv import load_dotenv
from notion_client import Client
import os
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPEECH_KEY = os.getenv("SPEECH_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SPEECH_KEY

NOTION_TOKEN = os.getenv("NOTION_KEY")
NOTION_LIST_LECTURE_PAGE_ID = os.getenv("NOTION_LIST_LECTURE_PAGE_ID") 
NOTION_DATABASE_LIVRE_ID = os.getenv("NOTION_DATABASE_LIVRE_ID")
NOTION_DATABASE_QUIZZ_ID = os.getenv("NOTION_DATABASE_QUIZZ_ID")
NOTION_DATABASE_TACHE_ID = os.getenv("NOTION_DATABASE_TACHE_ID")
LIVRE = os.getenv("LIVRE")
CLIENT = Client(auth=NOTION_TOKEN)

print(LIVRE)