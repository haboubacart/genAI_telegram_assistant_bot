import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

             
def response_to_query(prompt, query='') -> json:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}, 
            ]
        )
    response = json.loads(response.choices[0].message.content)
    
    if response["action"] == "quiz" :
      list_questions, list_reponses = [],[]
      for q_a in response["quiz_qa"] :
         list_questions.append(q_a["q"])
         list_reponses.append(q_a["a"])
      return (list_questions, list_reponses)
    
    if response["action"] == "evaluate_user_reponses" :
      grade = 0
      for elm in response["grades"] : 
        grade+=elm["note"]
      return (grade)
        
    return response



