from flask_cors import cross_origin

from quiz import app, db
from flask import request, Response
from quiz.models import Questions, User
from quiz.api.errors import bad_request
import json


@app.route("/api/questions/")
@cross_origin(supports_credentials=True)
def get_questions():
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


@app.route("/api/users/register/", methods=["POST"])
@cross_origin(supports_credentials=True)
def register():
    data = request.get_json(force=True) or {}

    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')

    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')

    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')

    if data['password'] != data['confirm_password']:
        return bad_request('confirm_password must be the same as password field')

    pwhash = User.generate_hash(data['password'])
    user = User(username=data['username'], email=data['email'], password_hash=pwhash)
    db.session.add(user)
    db.session.commit()

    return Response(json.dumps(user.to_dict()))


@app.route("/api/users/login/", methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json(force=True) or {}
    if 'username' not in data or 'password' not in data:
        return bad_request('must include username and password fields')
    user = User.query.filter_by(username=data['username']).first()
    if user:
        verified = user.verify_password(data['password'])
        if verified:
            token = user.create_or_get_token(expires_in=3600)
            success_message = {
                'token': token,
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }
            return Response(json.dumps(success_message))

    return bad_request('Invalid username or password')
