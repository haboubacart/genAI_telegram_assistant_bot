from dotenv import load_dotenv
import time
import os
from pprint import pprint
from src.google.speech_to_text import transcribe_voice
from src.telegram_bot.bot import save_voice_message
from src.chatgpt.chatgpt import response_to_query
from src.google.google_calandar import (get_calandar_events,
                                 create_calandar_event,
                                 get_creds)

from src.notion.text_block import (get_id_livre_database,
                                    create_new_block,
                                    write_text_to_block)
                                    

from src.notion.quizz import (add_grade_to_quizz_row, 
                                 create_new_quizz_row,
                                 get_last_quizz_row_id)


from src.notion.tache import (get_all_taches,
                              create_new_tache)

from src.chatgpt.prompts import (get_corrector_prompt,
                                 get_qa_prompt,
                                 get_quizz_prompt)

from config import (NOTION_TOKEN,
                    BOT_TOKEN,
                    SPEECH_KEY,
                    NOTION_LIST_LECTURE_PAGE_ID,
                    NOTION_DATABASE_LIVRE_ID,
                    NOTION_DATABASE_QUIZZ_ID,
                    NOTION_DATABASE_TACHE_ID,
                    CLIENT)

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

responses_to_quizz = '''
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
    '''quizz = response_to_query(get_quizz_prompt(retrieved_texte))
    print(quizz)
    create_new_quizz_row(client, NOTION_DATABASE_QUIZZ_ID, str(quizz[0]), str(quizz[1]))
    time.sleep(10)
    last_quizz_row_id = get_last_quizz_row_id(client, NOTION_DATABASE_QUIZZ_ID)
    grades = response_to_query(get_corrector_prompt(responses_to_quizz))
    print(grades)
    add_grade_to_quizz_row(client, NOTION_DATABASE_QUIZZ_ID, last_quizz_row_id, grades, grades>9)'''
    pprint(get_all_taches(CLIENT, NOTION_DATABASE_TACHE_ID))
    #create_new_tache(client, NOTION_DATABASE_TACHE_ID, "tache de test")

    