def get_quizz_prompt(retrieved_texte):
    prompt_QUIZ = '''
              Tu es un expert en quiz. A partir du texte ci-dessus qui represente des notes que j'ai prises pendant la lecture d'un livre
              tu dois creer un quiz composé de 3 questions les plus pertinentes qui permettent d'évaluer la 
              bonne compréhension du livre. Si tu reconnais de quel livre il s'agit, tu peux enrichir le quiz avec 
              des questions plus poussées, et tu peux même mentionner le livre si tu y arrives. \n
               Si tu vex faire reference au livre, tu dois dire selon le livre ou bien selon l'auteur. \n 
              Tu dois retourner un json comme ça : \n
              {
                  "action" : "quizz",
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
    return prompt_QUIZ

def get_qa_prompt():
    prompt_QA = '''
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
              2 - Si la requete concerne une demande de connaitre une pricipe ou un sujet scientifique, tu dois repondre avec un json comme ça :\n
              tu dois repondre a la requete de l'utilsateur, comment resumer un sujet en quelques mots : \n
              {
                "action" : "discover",
                "reponse" : "un bref deeloppement du sujet avec les points les plus importants à connaitre sur le sujet"
              }\n
              Tu peux accompagner les points important dans ta réponses par des liens web de pages parlant du sujet.
              \n\n
              3- Si la requete est une salutation ou demande sur tes competences, tu dois repondre avec un json comme ça :\n
              {
                "action" : "general",
                "reponse" : "ta reponse la plus appropriee"
              }
            '''
    return prompt_QA
    
def get_corrector_prompt(q_a_user_reponses):
    prompt_CORRECTOR = '''
                  Tu es un expert en quiz et tu dois avoir corriger et attribuer une note entre 0 et 5 à un utilisateur qui repond 
                  à un quiz composé de 3 questions.\n
                  Tu reçois un json comportant les questions, les reponses attendues et les reponse de l'utilisateur.\n
                  Voici le json que tu reçois : \n ''' + f'\n\n Texte = {q_a_user_reponses}' + \
                  '''
                  q : correspond à la question posée. \n
                  r : correspond à la reponse attendue. \n
                  r_user : correspond à la reponse proposée par l'utilisateur.\n
                  \n
                  Tu dois retourner un json comme ça : \n
                  {
                    "action" : "evaluate_user_reponses"
                    "grades" : [
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
                  }
                  
                  \n
                  note : est la note que tu attribues à l'utilisateur. Tu évalues la reponse de l'utilisateur par rapport à la reponse attendue. Elle doit sous la forme d'un nombre.
                  '''
    return prompt_CORRECTOR