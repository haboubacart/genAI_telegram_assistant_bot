import openai
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def response_to_query(query):
    prompt = '''Tu es un assitant bureatique. 
              tu dois repondre a la requete de l'utilsateur, comment resumer un sujet en quelques mots : 
              {
                "action" : "defaut",
                "reponse" : "ta reponse"
              }
            '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}, 
            ]
        )
    return json.loads(response.choices[0].message.content)

#print(json.dumps(response_to_query("Bonjour commen ca va ?"), indent=2))
