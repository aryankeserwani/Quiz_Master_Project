from flask_restful import Api, Resource, reqparse
from .models import *
from flask_security import auth_required, roles_required, current_user, verify_password, hash_password

api = Api()


class QuizApi(Resource):
    def get(self):
        quizzes = Quiz.query.all()
        return [quiz.serialize for quiz in quizzes]  # Return a list of serialized quizzes