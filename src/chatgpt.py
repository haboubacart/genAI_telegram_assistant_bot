import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def response_to_query(query):
    prompt = '''Tu es un assitant, et tu t'appelles Habou Assist. 
              tu dois repondre a la requete de l'utilsateur, comment resumer un sujet en quelques mots : 
              {
                "action" : "defaut",
                "reponse" : "ta reponse"
              }
            '''
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}, 
            ]
        )
    return json.loads(response.choices[0].message.content)