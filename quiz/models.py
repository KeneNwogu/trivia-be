import base64
import os
from datetime import datetime, timedelta

from quiz import db
from werkzeug.security import generate_password_hash, check_password_hash


class JsonModel(object):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(db.Model, JsonModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    hearts = db.Column(db.Integer, nullable=False, default=5)
    rank = db.Column(db.Integer, nullable=True)
    high_score = db.Column(db.Integer, nullable=False, default=0)
    account_number = db.Column(db.String(15), nullable=True)
    token = db.relationship('UserToken', backref='user', uselist=False, lazy=True)

    @staticmethod
    def generate_hash(password):
        return generate_password_hash(password)

    def create_or_get_token(self, expires_in):
        now = datetime.utcnow()
        if self.token and self.token.expiration_time > now + timedelta(seconds=60):
            return self.token
        token = base64.b64encode(os.urandom(24)).decode('utf-8')
        expiration_time = now + timedelta(seconds=expires_in)
        user_token = UserToken(token=token, expiration_time=expiration_time)
        user_token.user = self
        print(user_token.user)
        db.session.add(user_token)
        db.session.commit()
        return user_token

    @staticmethod
    def check_token(token):
        now = datetime.utcnow()
        user_token = UserToken.query.filter_by(token=token).first()
        if user_token and user_token.expiration_time > now + timedelta(seconds=2):
            return user_token.user
        return None

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        data = {
            'status_code': 201,
            'response_message': "Successfully registered user",
            'username': self.username,
            'email': self.email,
            'rank': self.rank,
            'high_score': self.high_score,
            'hearts': self.hearts,
            'account_number': self.account_number
        }
        return data

    def __repr__(self):
        return f'User: {self.username}'


class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    expiration_time = db.Column(db.DateTime, default=datetime.utcnow)


class Questions(db.Model, JsonModel):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, unique=True, nullable=False)
    correct_answer = db.Column(db.String(120), nullable=True)

    incorrect_answers = db.relationship('IncorrectAnswers', backref='question', lazy=True)


class IncorrectAnswers(db.Model, JsonModel):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(120), nullable=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)

