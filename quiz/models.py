from quiz import db

records = registrations = db.Table('registrations',
                            db.Column('user_id', db.Integer,
                            db.ForeignKey('user.id')),
                            db.Column('question_id', db.Integer,
                            db.ForeignKey('questions.id'))
                        )


class JsonModel(object):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(db.Model, JsonModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)
    quizzes = db.relationship('Questions', secondary=records, backref=db.backref('user', lazy='dynamic'), lazy='dynamic')
    score = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'User: {self.name}'


class Questions(db.Model, JsonModel):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, unique=True, nullable=False)
    correct_answer = db.Column(db.String(120), nullable=True)

    incorrect_answers = db.relationship('IncorrectAnswers', backref='question', lazy=True)


class IncorrectAnswers(db.Model, JsonModel):
    id = db.Column(db.Integer, primary_key=True) 
    answer = db.Column(db.String(120), nullable=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)

