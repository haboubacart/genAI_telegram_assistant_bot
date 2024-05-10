import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

prompt_QA = '''
              Tu es un assitant, et tu t'appelles Habou Assist. 
              Tu dois traiter la requete de l'utilisateur et lui repondre. 
              Tu dois être synthetique dans tes reponses.
              Dans ta reponse, tu peux mettre des mots important entre deux etoiles : **mot important** pour l'afficher en gras dans telegram. Chaque mot pertinent doit etre en gras
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
                "reponse" : "ta reponse la plus appropriee"
              }

            '''
retrieved_texte = '''
**Quelques passages importants** 

« Il existe une différence entre être pauvre et être sans le sou. Quand on est pauvre c’est pour toujours, être sans le sou c’est temporaire. » R. Kiyosaki

« L’Histoire prouve que de grandes civilisations s’écroulèrent quand le fossé entre les riches et les pauvres fut trop considérable. Malheureusement, l’Amérique est sur la même voie, car nous ne retenons pas les leçons de l’histoire. Nous ne faisons que mémoriser les dates et les personnages historiques, et non pas les leçons qu’elle enseigne » R. Kiyosaki

« L’argent braque fréquemment un projecteur sur certains côtés de nous qui nous échappent »

« Notre esprit est l’actif le plus puissant et le plus unique que nous possédons tous. S’il est bien entraîné, il peut produire d’énormes richesses »

« L’échec inspire les gagnants et met en déroute les perdants »

L’intelligence financière est composée de ces 3 piliers :

- la comptabilité
- L’investissement
- La compréhension des marchés
- La loi

10 points tres importants :

- 1. Trouvez une raison plus grande que nature : Le pouvoir de l’esprit
- 2. Faites des choix quotidiens : Le pouvoir du choix
- 3. Choisissez vos amis prudemment : Le pouvoir de l’association
- 4. Maîtrisez une formule et apprenez-en une nouvelle : Le pouvoir d’apprendre rapidement
- 5. Payez-vous en priorité : Le pouvoir de l’autodiscipline

**Fil a voir : le film Jerry Maguire,**
'''
prompt_QUIZ = '''
              Tu es un expert en quiz. A partir du texte ci-dessus qui represente des notes que j'ai prises pendant la lecture d'un livre
              tu dois creer un quiz composé de 3 questions les plus pertinentes qui permettent d'évaluer la 
              bonne compréhension du livre. Si tu reconnais de quel livre il s'agit, tu peux enrichir le quiz avec 
              des questions plus poussées, et tu peux même mentionner le livre si tu y arrives. \n 
              Tu dois retourner un json comme ça : \n
              {
                  "action" : "quiz",
                  "quiz_qa" : [
                                {
                                  "q" : "question1",
                                  "a" : "response1"
                                },
                                {
                                  "q" : "question2",
                                  "r" : "response2"
                                },
                                {
                                  "q" : "question3",
                                  "r" : "response3"
                                }
                              ]
              }   
              ''' + f'\n\n Texte = {retrieved_texte}'

prompt_CORRECTOR = '''
                  Tu es un expert en quiz et tu dois avoir corriger et attribuer une note entre 0 et 5 à un utilisateur qui repond 
                  à un quiz composé de 3 questions.\n
                  Tu reçois un json comportant les questions, les reponses attendues et les reponse de l'utilisateur.\n
                  Voici le json que tu peux recevoir : \n
                  [
                    {
                      "q" : "question1",
                      "a" : "response1",
                      "r_user" : "reponse1_user"
                    },
                    {
                      "q" : "question2",
                      "r" : "response2",
                      "r_user" : "reponse2_user"
                    },
                    {
                      "q" : "question3",
                      "r" : "response3",
                      "r_user" : "reponse3_user"
                    }
                  ]
                  \n
                  q : correspond à la question posée. \n
                  r : correspond à la reponse attendue. \n
                  r_user : correspond à la reponse proposée par l'utilisateur.\n
                  \n
                  Tu dois retourner un json comme ça : \n
                  [
                    {
                      "note" : "note de la question 1"
                    },
                    {
                      "note" : "note de la question 2"
                    },
                    {
                      "note" : "note de la question 3"
                    }
                  ]
                  \n
                  note : est la note que tu attribues à l'utilisateur. Tu évalues la reponse de l'utilisateur par rapport à la reponse attendue. Elle doit sous la forme d'un nombre.
                  '''
             
def response_to_query(query : str, prompt = prompt_QA) -> json:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}, 
            ]
        )
    return json.loads(response.choices[0].message.content)


query = '''
    [
    {
      "q": "Quelle est la diff\u00e9rence entre \u00eatre pauvre et \u00eatre sans le sou selon R. Kiyosaki?",
      "a": "Etre pauvre est une condition permanente, \u00eatre sans le sou est temporaire.",
      "r_user" : "Quand tu es pauvre c'est pour toujours alors ne pas avoir d'argent est passager"
    },
    {
      "q": "Quels sont les trois piliers de l'intelligence financi\u00e8re selon l'auteur?",
      "r": "La comptabilit\u00e9, l'investissement, et la compr\u00e9hension des march\u00e9s.",
      "r_user" : "la comptabilité et l'investissement"
    },
    {
      "q": "Quelle est la signification de 'Payez-vous en priorit\u00e9' selon le livre?",
      "r": "Cela renvoie \u00e0 l'autodiscipline et l'importance d'investir d'abord dans soi-m\u00eame, economiser ou investir avant de d\u00e9penser.",
      "r_user" : "je ne sais pas"
    }
  ]
'''

if __name__ == '__main__':
    print(json.dumps(response_to_query(query, prompt_CORRECTOR), indent=2))


