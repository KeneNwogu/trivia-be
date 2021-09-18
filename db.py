# # Fill in dtabase tables with the quiz APi
# from pprint import pprint
# import json

import requests
from quiz import db
from quiz.models import Questions, IncorrectAnswers

url = 'https://opentdb.com/api.php'
payload = {
    'amount': 10,
    'category': 11,
    'difficulty': 'easy'
}
r = requests.get(url, params=payload)
questions = r.json()
print(questions)
for question in questions['results']:
    q = Questions(question=question['question'], correct_answer=question['correct_answer'])
    for incorrect in question['incorrect_answers']:
        incorrect_answer = IncorrectAnswers(answer=incorrect)
        incorrect_answer.question = q
        db.session.add(incorrect_answer)
    db.session.add(q)

db.session.commit()

