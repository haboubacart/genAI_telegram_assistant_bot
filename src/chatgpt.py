import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def response_to_query(query):
    prompt = '''
              Tu es un assitant, et tu t'appelles Habou Assist. 
              Tu dois traiter la requete de l'utilisateur et lui repondre. 
              Tu dois être synthetique dans tes reponses.
              Plusieurs cas d'usages existe.\n
              
              1- Si la requete concerne une demande de programmer d'un apprentissage, tu dois repondre avec un json comme ça :\n
              {
                "action" : "schedule_learning",
                "reponse" : "ta reponse pour indiquer à l'utilisateur que sa demande a été traitée",
                "titre" : "le titre du sujet",
                "description" : "les points essetiels du sujet accompagner des liens webs",
                "duree" : "le nombre d'heure necessaire pour parcourir le sujet, doit etre au maximum egal à 3"
              }\n
              description doit être donnée avec une mise en forme html\n
              duree est un entier positif.

              \n\n

              2 - Si la requete concerne une demande de resumer un sujet, tu dois repondre avec un json comme ça :\n
              tu dois repondre a la requete de l'utilsateur, comment resumer un sujet en quelques mots : \n
              {
                "action" : "summarize",
                "reponse" : "le resume du sujet que tu as realisé"
              }

              \n\n

              3- Si la requete est une salutation ou demande sur tes competences, tu dois repondre avec un json comme ça :\n
              {
                "action" : "general",
                "reponse" : "ta reponse la plus approprie"
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