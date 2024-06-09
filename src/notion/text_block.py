
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


def update_id_livres_database(client, lecture_page_id, database_livre_id) :
     blocks = client.databases.query(database_id=lecture_page_id)
     for livre in blocks['results'] : 
        id = livre["id"]
        intitule = livre["properties"]["Name"]["title"][0]["text"]["content"]
        # Vérifier si la page existe déjà
        existing_pages = client.databases.query(
                **{
                "database_id": database_livre_id,
                "filter": {
                    "property": "id_page_notion_livre",
                    "title": {
                        "equals": id
                    }
                }
            }
        )
        # Si aucune page existante n'est trouvée, créer une nouvelle page
        if not existing_pages['results']:
            print("adding")
            client.pages.create(
                    **{
                        "parent": {
                            "database_id": database_livre_id
                        },
                        'properties': {
                            "id_page_notion_livre" : {'title': [{'text': {'content': id}}]},
                            "intitule_livre" : {'rich_text': [{'text': {'content': intitule}}]}
                        }
                    }
                )
       

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
  
def extract_text_from_block(client, block_id) :
    blocks = client.blocks.children.list(block_id=block_id)['results']
    extracted_text = ""
    for block in blocks :
        for _, value in block.items() :
            if isinstance(value, dict) and 'rich_text' in value :
                for text_item in value['rich_text'] :
                    if 'text' in text_item :
                        extracted_text += text_item['text']['content']
                extracted_text += "\n"
    return extracted_text    