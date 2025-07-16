from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    fullname = db.Column(db.String(150), nullable=False)
    qualification = db.Column(db.String(150), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    role = db.Column(db.Text, nullable=False, default='User')
    quizzes = db.relationship('Quiz', secondary='user_quiz', backref=db.backref('users', lazy='dynamic'))
    scores = db.relationship('Score', backref='user', lazy=True)
    leaderboard_entries = db.relationship('Leaderboard', backref='user', lazy=True)
    
# Subject model
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    chapters = db.relationship('Chapter', backref='subject', lazy=True)

# Chapter model
class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)
    questions = db.relationship('Question', backref='chapter', lazy=True)
    
# Quiz model
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.DateTime, default=datetime.utcnow)
    time_duration = db.Column(db.String(10), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    questions = db.relationship('Question', backref='quiz', lazy=True)
    scores = db.relationship('Score', backref='quiz', lazy=True)
    leaderboard_entries = db.relationship('Leaderboard', backref='quiz', lazy=True)
    
# Question model    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(150), nullable=False)
    option2 = db.Column(db.String(150), nullable=False)
    option3 = db.Column(db.String(150), nullable=True)
    option4 = db.Column(db.String(150), nullable=True)
    correct_option = db.Column(db.String(150), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

# Score model   
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    total_scored = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    questions_attempted = db.Column(db.Integer, nullable=False)
    questions_correct = db.Column(db.Integer, nullable=False)
    questions_wrong = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    remarks = db.Column(db.Text, nullable=True)
 
# Leaderboard model    
class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)
    
user_quiz = db.Table('user_quiz',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('quiz_id', db.Integer, db.ForeignKey('quiz.id'), primary_key=True)
)
