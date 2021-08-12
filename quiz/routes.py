from flask_cors import cross_origin

from quiz import app, db
from flask import request, Response
from quiz.models import Questions
import json


@app.route("/api/questions/")
@cross_origin(supports_credentials=True)
def questions():
    amount = int(request.args.get('amount'))
    if amount:
        questions = Questions.query.limit(amount).all()
        questions_list = []
        for q in questions:
            data = {
                'question': q.question,
                'correct_answer': q.correct_answer,
                'incorrect_answers': list(q.incorrect_answers)
            }
            questions_list.append(data)

        for i in range(len(questions)):
            incorrect_answers = []
            for incorrect in questions_list[i]['incorrect_answers']:
                incorrect_answers.append(incorrect.as_dict()['answer'])
            questions_list[i]['incorrect_answers'] = incorrect_answers

        json_data = json.dumps(questions_list)
        return Response(json_data)
