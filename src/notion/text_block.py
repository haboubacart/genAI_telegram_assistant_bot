from pprint import pprint

def get_id_livre_database(client, database_id):
    bd_data_response =  client.databases.query(database_id=database_id)
    content = []
    for item in bd_data_response['results']:
       content.append(
          {
             "id_page_notion_livre" : item["properties"]["id_page_notion_livre"]["title"][0]["text"]["content"],
             "intitule_livre" : item["properties"]["intitule_livre"]["rich_text"][0]["text"]["content"]
          }
       )
    return(content)

def write_text_to_block(client, block_id, text, type):
  client.blocks.children.append(
        block_id=block_id,
        children=[
            {
                "object": "block",
                "type": type,
                type: {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": text
                            }
                        }
                    ]
                }
            }
        ]
    )
  
def get_page_text():
   return

def read_text(client, page_id):
    response = client.blocks.children.list(block_id=page_id)
    return response['results']

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from config import (NOTION_TOKEN,
                    BOT_TOKEN,
                    SPEECH_KEY,
                    NOTION_LIST_LECTURE_PAGE_ID,
                    NOTION_DATABASE_LIVRE_ID,
                    NOTION_DATABASE_QUIZZ_ID,
                    NOTION_DATABASE_TACHE_ID,
                    CLIENT)

if __name__=='__main__' : 
   print(NOTION_LIST_LECTURE_PAGE_ID)
   pprint(read_text(CLIENT, NOTION_LIST_LECTURE_PAGE_ID))
