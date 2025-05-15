from flask_restful import Api, Resource, fields, marshal_with, marshal, reqparse, inputs
from flask import request, abort
from .models import *
from flask_security import auth_required, roles_required, current_user, verify_password, hash_password

api = Api()


# Marshaling Fields for Output Formatting

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'full_name': fields.String,
    'qualification': fields.String,
    'dob': fields.String,  # You can convert Date to string (or use a custom formatter)
}

subject_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
}

chapter_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'subject_id': fields.Integer,
}

quiz_fields = {
    'id': fields.Integer,
    'chapter_id': fields.Integer,
    'date_of_quiz': fields.DateTime(dt_format='iso8601'),
    'time_duration': fields.String,
    'remarks': fields.String,
}

question_fields = {
    'id': fields.Integer,
    'quiz_id': fields.Integer,
    'chapter_id': fields.Integer,
    'question_statement': fields.String,
    'option1': fields.String,
    'option2': fields.String,
    'option3': fields.String,
    'option4': fields.String,
    'correct_option': fields.String,
    'marks': fields.Integer,
}

score_fields = {
    'id': fields.Integer,
    'quiz_id': fields.Integer,
    'user_id': fields.Integer,
    'time_stamp_of_attempt': fields.DateTime(dt_format='iso8601'),
    'total_scored': fields.Integer,
    'total_questions': fields.Integer,
    'questions_attempted': fields.Integer,
    'questions_correct': fields.Integer,
    'questions_wrong': fields.Integer,
    'percentage': fields.Float,
    'remarks': fields.String,
}

leaderboard_fields = {
    'id': fields.Integer,
    'quiz_id': fields.Integer,
    'user_id': fields.Integer,
    'score': fields.Integer,
    'rank': fields.Integer,
    'time_stamp': fields.DateTime(dt_format='iso8601'),
}


# Request Parsers (Input Validation with reqparse)

# Parser for creating/updating Subjects
subject_parser = reqparse.RequestParser()
subject_parser.add_argument('name', type=str, required=True, help='Subject name is required')
subject_parser.add_argument('description', type=str)

# Parser for Chapters
chapter_parser = reqparse.RequestParser()
chapter_parser.add_argument('name', type=str, required=True, help='Chapter name is required')
chapter_parser.add_argument('description', type=str)
chapter_parser.add_argument('subject_id', type=int, required=True, help='Subject ID is required')

# Parser for Quizzes
quiz_parser = reqparse.RequestParser()
quiz_parser.add_argument('chapter_id', type=int, required=True, help='Chapter ID is required')
quiz_parser.add_argument('time_duration', type=str, required=True, help='Time duration is required')
quiz_parser.add_argument('remarks', type=str)

# Parser for Questions
question_parser = reqparse.RequestParser()
question_parser.add_argument('quiz_id', type=int, required=True, help='Quiz ID is required')
question_parser.add_argument('chapter_id', type=int, required=True, help='Chapter ID is required')
question_parser.add_argument('question_statement', type=str, required=True, help='Question statement is required')
question_parser.add_argument('option1', type=str, required=True, help='Option 1 is required')
question_parser.add_argument('option2', type=str, required=True, help='Option 2 is required')
question_parser.add_argument('option3', type=str)
question_parser.add_argument('option4', type=str)
question_parser.add_argument('correct_option', type=str, required=True, help='Correct option is required')
question_parser.add_argument('marks', type=int, required=True, help='Marks are required')

# Parser for deletion of Users (admin-only)
user_delete_parser = reqparse.RequestParser()
user_delete_parser.add_argument('user_id', type=int, required=True, help='User ID is required')

# Generic Search Parser (for query string parameters)
search_parser = reqparse.RequestParser()
search_parser.add_argument('query', type=str, location='args')
search_parser.add_argument('subject_id', type=int, location='args')
search_parser.add_argument('chapter_id', type=int, location='args')
search_parser.add_argument('question_type', type=str, location='args')  # Customize as needed


# Resources (Endpoints)


# Subject Endpoints


class SubjectListResource(Resource):
    @auth_required()
    @roles_required('admin')
    @marshal_with(subject_fields)
    def get(self):
        """List all subjects with optional search query"""
        args = search_parser.parse_args()
        query_str = args.get('query')
        subjects_query = Subject.query
        if query_str:
            subjects_query = subjects_query.filter(Subject.name.ilike(f"%{query_str}%"))
        subjects = subjects_query.all()
        return subjects

    @auth_required()
    @roles_required('admin')
    @marshal_with(subject_fields)
    def post(self):
        """Create a new subject"""
        args = subject_parser.parse_args()
        new_subject = Subject(name=args['name'], description=args.get('description'))
        db.session.add(new_subject)
        db.session.commit()
        return new_subject, 201

class SubjectResource(Resource):
    @auth_required()
    @roles_required('admin')
    @marshal_with(subject_fields)
    def get(self, subject_id):
        """Get a single subject by ID"""
        subject = Subject.query.get_or_404(subject_id)
        return subject

    @auth_required()
    @roles_required('admin')
    @marshal_with(subject_fields)
    def put(self, subject_id):
        """Update a subject"""
        subject = Subject.query.get_or_404(subject_id)
        args = subject_parser.parse_args()
        subject.name = args['name']
        subject.description = args.get('description')
        db.session.commit()
        return subject

    @auth_required()
    @roles_required('admin')
    def delete(self, subject_id):
        """Delete a subject"""
        subject = Subject.query.get_or_404(subject_id)
        db.session.delete(subject)
        db.session.commit()
        return {'message': 'Subject deleted'}, 200


# Chapter Endpoints (Nested under Subject)


class ChapterListResource(Resource):
    @auth_required()
    @roles_required('admin')
    @marshal_with(chapter_fields)
    def get(self, subject_id):
        """List chapters for a given subject"""
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        return chapters

    @auth_required()
    @roles_required('admin')
    @marshal_with(chapter_fields)
    def post(self, subject_id):
        """Create a new chapter within a subject"""
        args = chapter_parser.parse_args()
        # Ensure the subject_id in the URL matches the payload
        if args['subject_id'] != subject_id:
            abort(400, description="Subject ID in payload does not match URL")
        new_chapter = Chapter(name=args['name'], description=args.get('description'), subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        return new_chapter, 201

class ChapterResource(Resource):
    @auth_required()
    @roles_required('admin')
    @marshal_with(chapter_fields)
    def get(self, chapter_id):
        """Get details of a specific chapter"""
        chapter = Chapter.query.get_or_404(chapter_id)
        return chapter

    @auth_required()
    @roles_required('admin')
    @marshal_with(chapter_fields)
    def put(self, chapter_id):
        """Update a chapter"""
        chapter = Chapter.query.get_or_404(chapter_id)
        args = chapter_parser.parse_args()
        chapter.name = args['name']
        chapter.description = args.get('description')
        chapter.subject_id = args['subject_id']
        db.session.commit()
        return chapter

    @auth_required()
    @roles_required('admin')
    def delete(self, chapter_id):
        """Delete a chapter"""
        chapter = Chapter.query.get_or_404(chapter_id)
        db.session.delete(chapter)
        db.session.commit()
        return {'message': 'Chapter deleted'}, 200


# Quiz Endpoints (Nested under Chapter)


class QuizListResource(Resource):
    @auth_required()
    @roles_required('admin')
    @marshal_with(quiz_fields)
    def get(self, chapter_id):
        """List quizzes for a given chapter"""
        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        return quizzes

    @auth_required()
    @roles_required('admin')
    @marshal_with(quiz_fields)
    def post(self, chapter_id):
        """Create a new quiz for a chapter"""
        args = quiz_parser.parse_args()
        if args['chapter_id'] != chapter_id:
            abort(400, description="Chapter ID in payload does not match URL")
        new_quiz = Quiz(chapter_id=chapter_id, time_duration=args['time_duration'], remarks=args.get('remarks'))
        db.session.add(new_quiz)
        db.session.commit()
        return new_quiz, 201

class QuizResource(Resource):
    @auth_required()
    @roles_required('admin')
    @marshal_with(quiz_fields)
    def get(self, quiz_id):
        """Retrieve a quiz by ID"""
        quiz = Quiz.query.get_or_404(quiz_id)
        return quiz

    @auth_required()
    @roles_required('admin')
    @marshal_with(quiz_fields)
    def put(self, quiz_id):
        """Update a quiz"""
        quiz = Quiz.query.get_or_404(quiz_id)
        args = quiz_parser.parse_args()
        quiz.chapter_id = args['chapter_id']
        quiz.time_duration = args['time_duration']
        quiz.remarks = args.get('remarks')
        db.session.commit()
        return quiz

    @auth_required()
    @roles_required('admin')
    def delete(self, quiz_id):
        """Delete a quiz"""
        quiz = Quiz.query.get_or_404(quiz_id)
        db.session.delete(quiz)
        db.session.commit()
        return {'message': 'Quiz deleted'}, 200


# Question Endpoints (Nested under Quiz)


class QuestionListResource(Resource):
    @auth_required()
    @roles_required('admin')
    @marshal_with(question_fields)
    def get(self, quiz_id):
        """List questions for a given quiz"""
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        return questions

    @auth_required()
    @roles_required('admin')
    @marshal_with(question_fields)
    def post(self, quiz_id):
        """Create a new question for a quiz"""
        args = question_parser.parse_args()
        if args['quiz_id'] != quiz_id:
            abort(400, description="Quiz ID in payload does not match URL")
        new_question = Question(
            quiz_id=quiz_id,
            chapter_id=args['chapter_id'],
            question_statement=args['question_statement'],
            option1=args['option1'],
            option2=args['option2'],
            option3=args.get('option3'),
            option4=args.get('option4'),
            correct_option=args['correct_option'],
            marks=args['marks']
        )
        db.session.add(new_question)
        db.session.commit()
        return new_question, 201

class QuestionResource(Resource):
    @auth_required()
    @roles_required('admin')
    @marshal_with(question_fields)
    def get(self, question_id):
        """Retrieve a specific question"""
        question = Question.query.get_or_404(question_id)
        return question

    @auth_required()
    @roles_required('admin')
    @marshal_with(question_fields)
    def put(self, question_id):
        """Update a question"""
        question = Question.query.get_or_404(question_id)
        args = question_parser.parse_args()
        question.quiz_id = args['quiz_id']
        question.chapter_id = args['chapter_id']
        question.question_statement = args['question_statement']
        question.option1 = args['option1']
        question.option2 = args['option2']
        question.option3 = args.get('option3')
        question.option4 = args.get('option4')
        question.correct_option = args['correct_option']
        question.marks = args['marks']
        db.session.commit()
        return question

    @auth_required()
    @roles_required('admin')
    def delete(self, question_id):
        """Delete a question"""
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return {'message': 'Question deleted'}, 200


# User Deletion Endpoint (Admin Only)


class UserDeleteResource(Resource):
    @auth_required()
    @roles_required('admin')
    def delete(self, user_id):
        """Delete a user"""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User {user.username} deleted'}, 200


# Search Endpoints for Admin Dashboard


class AdminSearchResource(Resource):
    @auth_required()
    @roles_required('admin')
    def get(self):
        """
        Search across various models:
          - users (by username)
          - quizzes (by remarks)
          - subjects (by name)
          - chapters (by name)
          - scores (by total_scored as substring)
          - leaderboard (by rank as substring)
        """
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=True, help="Search type required", location='args')
        parser.add_argument('query', type=str, required=True, help="Search query required", location='args')
        args = parser.parse_args()
        search_type = args['type']
        query_str = args['query']
        results = {}

        if search_type == 'users':
            results['users'] = [marshal(user, user_fields) for user in User.query.filter(User.username.ilike(f"%{query_str}%")).all()]
        elif search_type == 'quizzes':
            results['quizzes'] = [marshal(quiz, quiz_fields) for quiz in Quiz.query.filter(Quiz.remarks.ilike(f"%{query_str}%")).all()]
        elif search_type == 'subjects':
            results['subjects'] = [marshal(subject, subject_fields) for subject in Subject.query.filter(Subject.name.ilike(f"%{query_str}%")).all()]
        elif search_type == 'chapters':
            results['chapters'] = [marshal(chapter, chapter_fields) for chapter in Chapter.query.filter(Chapter.name.ilike(f"%{query_str}%")).all()]
        elif search_type == 'scores':
            results['scores'] = [marshal(score, score_fields) for score in Score.query.all() if query_str in str(score.total_scored)]
        elif search_type == 'leaderboard':
            results['leaderboard'] = [marshal(lb, leaderboard_fields) for lb in Leaderboard.query.all() if query_str in str(lb.rank)]
        else:
            abort(400, description="Invalid search type")
        return results, 200


# Search Endpoint for User Dashboard


class UserDashboardSearchResource(Resource):
    @auth_required()
    def get(self):
        """
        For the user dashboard, allow search for:
          - quizzes (admin created)
          - current user's scores
        """
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=True, help="Search type required", location='args')
        parser.add_argument('query', type=str, required=True, help="Search query required", location='args')
        args = parser.parse_args()
        search_type = args['type']
        query_str = args['query']
        results = {}
        if search_type == 'quizzes':
            results['quizzes'] = [marshal(quiz, quiz_fields) for quiz in Quiz.query.filter(Quiz.remarks.ilike(f"%{query_str}%")).all()]
        elif search_type == 'scores':
            results['scores'] = [marshal(score, score_fields) for score in Score.query.filter_by(user_id=current_user.id).all() if query_str in str(score.total_scored)]
        else:
            abort(400, description="Invalid search type for user dashboard")
        return results, 200


# Quiz Filtering Endpoint


class QuizFilterResource(Resource):
    @auth_required()
    def get(self):
        """
        Filter quizzes based on subject, chapter, or question type.
        Note: 'question_type' filtering would require a join with questions – customize as needed.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('subject_id', type=int, location='args')
        parser.add_argument('chapter_id', type=int, location='args')
        parser.add_argument('question_type', type=str, location='args')
        args = parser.parse_args()
        query = Quiz.query

        if args.get('chapter_id'):
            query = query.filter_by(chapter_id=args['chapter_id'])
        elif args.get('subject_id'):
            # Get all chapters for this subject then filter quizzes
            chapters = Chapter.query.filter_by(subject_id=args['subject_id']).all()
            chapter_ids = [ch.id for ch in chapters]
            query = query.filter(Quiz.chapter_id.in_(chapter_ids))
        # 'question_type' is not directly stored on Quiz; it would require joining with Question
        quizzes = query.all()
        return [marshal(quiz, quiz_fields) for quiz in quizzes], 200


# Route Registration Function


def initialize_routes(api):
    # Subject endpoints
    api.add_resource(SubjectListResource, '/subjects')
    api.add_resource(SubjectResource, '/subjects/<int:subject_id>')
    
    # Chapter endpoints (nested under Subject)
    api.add_resource(ChapterListResource, '/subjects/<int:subject_id>/chapters')
    api.add_resource(ChapterResource, '/chapters/<int:chapter_id>')
    
    # Quiz endpoints (nested under Chapter)
    api.add_resource(QuizListResource, '/chapters/<int:chapter_id>/quizzes')
    api.add_resource(QuizResource, '/quizzes/<int:quiz_id>')
    
    # Question endpoints (nested under Quiz)
    api.add_resource(QuestionListResource, '/quizzes/<int:quiz_id>/questions')
    api.add_resource(QuestionResource, '/questions/<int:question_id>')
    
    # User deletion endpoint (admin only)
    api.add_resource(UserDeleteResource, '/api/users/<int:user_id>')
    
    # Admin search endpoint
    api.add_resource(AdminSearchResource, '/api/admin/search')
    
    # User dashboard search endpoint
    api.add_resource(UserDashboardSearchResource, '/api/user/search')
    
    # Quiz filter endpoint
    api.add_resource(QuizFilterResource, '/quizzes/filter')


# End of resource.py

