# Import necessary modules and libraries
from flask import current_app as app, jsonify, render_template, request, abort
from flask_security import (
    auth_required,
    roles_required,
    current_user,
    verify_password,
    hash_password,
)
from Backend.models import db, User, Role, Subject, Chapter, Quiz, Question, Score
from datetime import datetime
import json

# Initialize the user datastore for managing user data
userdatastore = app.security.datastore

# Route to serve the main index.html file
@app.get("/")
def hello():
    return app.send_static_file("index.html")

# Protected route accessible only by authenticated users
@app.get("/protected")
@auth_required("token")
def protected():
    return "<h1>Only accesible by auth User</h1>"

# API endpoint for user login
@app.route("/api/login", methods=["POST"])
def login():
    # Parse JSON data from the request
    data = request.get_json()

    # Extract username and password from the request
    username = data.get("username")
    password = data.get("password")

    # Validate input
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # Find the user in the datastore
    user = userdatastore.find_user(username=username)

    # Check if user exists and password is correct
    if not user:
        return jsonify({"message": "Please enter valid username and password"}), 400

    if verify_password(password, user.password):
        # Return user details and authentication token
        return jsonify(
            {
                "token": user.get_auth_token(),
                "username": user.username,
                "email": user.email,
                "role": user.roles[0].name,
                "id": user.id,
            }
        )

    # Return error if authentication fails
    return jsonify({"message": "Please enter valid username and password"})

# API endpoint for user registration
@app.route("/api/register", methods=["POST"])
def register():
    # Parse JSON data from the request
    data = request.get_json()

    # Extract user details from the request
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    fullname = data.get("fullname")
    qualification = data.get("qualification")
    dob_str = data.get("dob")  # Get the string from the request
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()  # Convert to date object

    # Validate input
    if not username or not password:
        return jsonify({"message": "Invalid credentials"}), 404

    # Check if the username already exists
    user = userdatastore.find_user(username=username)
    if user:
        return jsonify({"message": "Username already exists!"}), 404

    # Get or create the user role
    user_role = userdatastore.find_role("user")
    if not user_role:
        # Create the role if it doesn't exist
        user_role = userdatastore.create_role(name="user", description="Regular user")
        
    # Create a new user with the provided details
    userdatastore.create_user(
        username=username,
        password=hash_password(password),
        roles=[user_role],
        full_name=fullname,
        qualification=qualification,
        dob=dob,
        email=email,
        active=True,
    )
    db.session.commit()  # Commit the changes to the database
    return jsonify({"message": "User is successfully registered"}), 201

# Admin-only route, accessible by users with the "Admin" role
@app.route("/api/admin")
@auth_required("token")
@roles_required("Admin")
def admin_home():
    return jsonify({"message": "Welcome Admin"})

# User dashboard route, accessible by users with the "user" role
@app.route("/api/user_dashboard")
@auth_required("token")
@roles_required("user")
def user_home():
    user = current_user  # Get the current authenticated user
    return jsonify(
        {"username": user.username, "email": user.email}
    )

# --------- Subject Management Routes ---------

# Get all subjects
@app.route("/api/subjects", methods=["GET"])
@auth_required("token")
def get_subjects():
    subjects = Subject.query.all()
    result = []
    for subject in subjects:
        result.append({
            "id": subject.id,
            "name": subject.name,
            "description": subject.description,
            "created_at": subject.created_at,
            "updated_at": subject.updated_at
        })
    return jsonify(result)

# Get a specific subject
@app.route("/api/subjects/<int:subject_id>", methods=["GET"])
@auth_required("token")
def get_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    return jsonify({
        "id": subject.id,
        "name": subject.name,
        "description": subject.description,
        "created_at": subject.created_at,
        "updated_at": subject.updated_at
    })

# Create a new subject (admin only)
@app.route("/api/subjects", methods=["POST"])
@auth_required("token")
@roles_required("Admin")
def create_subject():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")
    
    if not name:
        return jsonify({"message": "Subject name is required"}), 400
    
    # Check if subject with same name already exists
    existing_subject = Subject.query.filter_by(name=name).first()
    if existing_subject:
        return jsonify({"message": "Subject with this name already exists"}), 400
    
    new_subject = Subject(name=name, description=description)
    db.session.add(new_subject)
    db.session.commit()
    
    return jsonify({
        "message": "Subject created successfully",
        "subject": {
            "id": new_subject.id,
            "name": new_subject.name,
            "description": new_subject.description
        }
    }), 201

# Update a subject (admin only)
@app.route("/api/subjects/<int:subject_id>", methods=["PUT"])
@auth_required("token")
@roles_required("Admin")
def update_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    
    name = data.get("name")
    description = data.get("description")
    
    if name:
        # Check if another subject with this name exists
        existing_subject = Subject.query.filter(Subject.name == name, Subject.id != subject_id).first()
        if existing_subject:
            return jsonify({"message": "Another subject with this name already exists"}), 400
        subject.name = name
    
    if description is not None:
        subject.description = description
    
    db.session.commit()
    
    return jsonify({
        "message": "Subject updated successfully",
        "subject": {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description
        }
    })

# Delete a subject (admin only)
@app.route("/api/subjects/<int:subject_id>", methods=["DELETE"])
@auth_required("token")
@roles_required("Admin")
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    
    return jsonify({"message": "Subject deleted successfully"})

# --------- Chapter Management Routes ---------

# Get all chapters for a subject
@app.route("/api/subjects/<int:subject_id>/chapters", methods=["GET"])
@auth_required("token")
def get_chapters(subject_id):
    Subject.query.get_or_404(subject_id)  # Check if subject exists
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    
    result = []
    for chapter in chapters:
        result.append({
            "id": chapter.id,
            "name": chapter.name,
            "description": chapter.description,
            "subject_id": chapter.subject_id,
            "created_at": chapter.created_at,
            "updated_at": chapter.updated_at
        })
    
    return jsonify(result)

# Get a specific chapter
@app.route("/api/chapters/<int:chapter_id>", methods=["GET"])
@auth_required("token")
def get_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    
    return jsonify({
        "id": chapter.id,
        "name": chapter.name,
        "description": chapter.description,
        "subject_id": chapter.subject_id,
        "created_at": chapter.created_at,
        "updated_at": chapter.updated_at
    })

# Create a new chapter (admin only)
@app.route("/api/subjects/<int:subject_id>/chapters", methods=["POST"])
@auth_required("token")
@roles_required("Admin")
def create_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)  # Check if subject exists
    data = request.get_json()
    
    name = data.get("name")
    description = data.get("description", "")
    
    if not name:
        return jsonify({"message": "Chapter name is required"}), 400
    
    new_chapter = Chapter(
        name=name,
        description=description,
        subject_id=subject_id
    )
    
    db.session.add(new_chapter)
    db.session.commit()
    
    return jsonify({
        "message": "Chapter created successfully",
        "chapter": {
            "id": new_chapter.id,
            "name": new_chapter.name,
            "description": new_chapter.description,
            "subject_id": new_chapter.subject_id
        }
    }), 201

# Update a chapter (admin only)
@app.route("/api/chapters/<int:chapter_id>", methods=["PUT"])
@auth_required("token")
@roles_required("Admin")
def update_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    data = request.get_json()
    
    name = data.get("name")
    description = data.get("description")
    
    if name:
        chapter.name = name
    
    if description is not None:
        chapter.description = description
    
    db.session.commit()
    
    return jsonify({
        "message": "Chapter updated successfully",
        "chapter": {
            "id": chapter.id,
            "name": chapter.name,
            "description": chapter.description,
            "subject_id": chapter.subject_id
        }
    })

# Delete a chapter (admin only)
@app.route("/api/chapters/<int:chapter_id>", methods=["DELETE"])
@auth_required("token")
@roles_required("Admin")
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    
    return jsonify({"message": "Chapter deleted successfully"})

# --------- Quiz Management Routes ---------

# Get all quizzes for a chapter
@app.route("/api/chapters/<int:chapter_id>/quizzes", methods=["GET"])
@auth_required("token")
def get_quizzes(chapter_id):
    Chapter.query.get_or_404(chapter_id)  # Check if chapter exists
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    
    result = []
    for quiz in quizzes:
        result.append({
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "chapter_id": quiz.chapter_id,
            "date_of_quiz": quiz.date_of_quiz.strftime("%Y-%m-%d"),
            "time_duration": quiz.time_duration,
            "remarks": quiz.remarks,
            "created_at": quiz.created_at,
            "updated_at": quiz.updated_at
        })
    
    return jsonify(result)

# Get a specific quiz
@app.route("/api/quizzes/<int:quiz_id>", methods=["GET"])
@auth_required("token")
def get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    return jsonify({
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "chapter_id": quiz.chapter_id,
        "date_of_quiz": quiz.date_of_quiz.strftime("%Y-%m-%d"),
        "time_duration": quiz.time_duration,
        "remarks": quiz.remarks,
        "created_at": quiz.created_at,
        "updated_at": quiz.updated_at
    })

# Create a new quiz (admin only)
@app.route("/api/chapters/<int:chapter_id>/quizzes", methods=["POST"])
@auth_required("token")
@roles_required("Admin")
def create_quiz(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)  # Check if chapter exists
    data = request.get_json()
    
    title = data.get("title")
    description = data.get("description", "")
    date_of_quiz_str = data.get("date_of_quiz")
    time_duration = data.get("time_duration")
    remarks = data.get("remarks", "")
    
    if not title or not date_of_quiz_str or not time_duration:
        return jsonify({
            "message": "Title, date of quiz, and time duration are required"
        }), 400
    
    # Parse date
    try:
        date_of_quiz = datetime.strptime(date_of_quiz_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    # Validate time duration format (HH:MM)
    if not time_duration or len(time_duration) != 5 or time_duration[2] != ":":
        return jsonify({"message": "Time duration must be in the format HH:MM"}), 400
    
    new_quiz = Quiz(
        title=title,
        description=description,
        chapter_id=chapter_id,
        date_of_quiz=date_of_quiz,
        time_duration=time_duration,
        remarks=remarks
    )
    
    db.session.add(new_quiz)
    db.session.commit()
    
    return jsonify({
        "message": "Quiz created successfully",
        "quiz": {
            "id": new_quiz.id,
            "title": new_quiz.title,
            "description": new_quiz.description,
            "chapter_id": new_quiz.chapter_id,
            "date_of_quiz": new_quiz.date_of_quiz.strftime("%Y-%m-%d"),
            "time_duration": new_quiz.time_duration,
            "remarks": new_quiz.remarks
        }
    }), 201

# Update a quiz (admin only)
@app.route("/api/quizzes/<int:quiz_id>", methods=["PUT"])
@auth_required("token")
@roles_required("Admin")
def update_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    title = data.get("title")
    description = data.get("description")
    date_of_quiz_str = data.get("date_of_quiz")
    time_duration = data.get("time_duration")
    remarks = data.get("remarks")
    
    if title:
        quiz.title = title
    
    if description is not None:
        quiz.description = description
    
    if date_of_quiz_str:
        try:
            quiz.date_of_quiz = datetime.strptime(date_of_quiz_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    if time_duration:
        if len(time_duration) != 5 or time_duration[2] != ":":
            return jsonify({"message": "Time duration must be in the format HH:MM"}), 400
        quiz.time_duration = time_duration
    
    if remarks is not None:
        quiz.remarks = remarks
    
    db.session.commit()
    
    return jsonify({
        "message": "Quiz updated successfully",
        "quiz": {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "chapter_id": quiz.chapter_id,
            "date_of_quiz": quiz.date_of_quiz.strftime("%Y-%m-%d"),
            "time_duration": quiz.time_duration,
            "remarks": quiz.remarks
        }
    })

# Delete a quiz (admin only)
@app.route("/api/quizzes/<int:quiz_id>", methods=["DELETE"])
@auth_required("token")
@roles_required("Admin")
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    
    return jsonify({"message": "Quiz deleted successfully"})

# --------- Question Management Routes ---------

# Get all questions for a quiz
@app.route("/api/quizzes/<int:quiz_id>/questions", methods=["GET"])
@auth_required("token")
def get_questions(quiz_id):
    Quiz.query.get_or_404(quiz_id)  # Check if quiz exists
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    result = []
    for question in questions:
        result.append({
            "id": question.id,
            "quiz_id": question.quiz_id,
            "question_statement": question.question_statement,
            "option1": question.option1,
            "option2": question.option2,
            "option3": question.option3,
            "option4": question.option4,
            "correct_option": question.correct_option
        })
    
    return jsonify(result)

# Get a specific question
@app.route("/api/questions/<int:question_id>", methods=["GET"])
@auth_required("token")
def get_question(question_id):
    question = Question.query.get_or_404(question_id)
    
    return jsonify({
        "id": question.id,
        "quiz_id": question.quiz_id,
        "question_statement": question.question_statement,
        "option1": question.option1,
        "option2": question.option2,
        "option3": question.option3,
        "option4": question.option4,
        "correct_option": question.correct_option
    })

# Create a new question (admin only)
@app.route("/api/quizzes/<int:quiz_id>/questions", methods=["POST"])
@auth_required("token")
@roles_required("Admin")
def create_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)  # Check if quiz exists
    data = request.get_json()
    
    question_statement = data.get("question_statement")
    option1 = data.get("option1")
    option2 = data.get("option2")
    option3 = data.get("option3")
    option4 = data.get("option4")
    correct_option = data.get("correct_option")
    
    # Validate required fields
    if not question_statement or not option1 or not option2 or not option3 or not option4 or correct_option is None:
        return jsonify({
            "message": "Question statement, all four options, and correct option are required"
        }), 400
    
    # Validate correct_option is 1, 2, 3, or 4
    if correct_option not in [1, 2, 3, 4]:
        return jsonify({"message": "Correct option must be 1, 2, 3, or 4"}), 400
    
    new_question = Question(
        quiz_id=quiz_id,
        question_statement=question_statement,
        option1=option1,
        option2=option2,
        option3=option3,
        option4=option4,
        correct_option=correct_option
    )
    
    db.session.add(new_question)
    db.session.commit()
    
    return jsonify({
        "message": "Question created successfully",
        "question": {
            "id": new_question.id,
            "quiz_id": new_question.quiz_id,
            "question_statement": new_question.question_statement,
            "option1": new_question.option1,
            "option2": new_question.option2,
            "option3": new_question.option3,
            "option4": new_question.option4,
            "correct_option": new_question.correct_option
        }
    }), 201

# Update a question (admin only)
@app.route("/api/questions/<int:question_id>", methods=["PUT"])
@auth_required("token")
@roles_required("Admin")
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.get_json()
    
    question_statement = data.get("question_statement")
    option1 = data.get("option1")
    option2 = data.get("option2")
    option3 = data.get("option3")
    option4 = data.get("option4")
    correct_option = data.get("correct_option")
    
    if question_statement:
        question.question_statement = question_statement
    
    if option1:
        question.option1 = option1
    
    if option2:
        question.option2 = option2
    
    if option3:
        question.option3 = option3
    
    if option4:
        question.option4 = option4
    
    if correct_option is not None:
        if correct_option not in [1, 2, 3, 4]:
            return jsonify({"message": "Correct option must be 1, 2, 3, or 4"}), 400
        question.correct_option = correct_option
    
    db.session.commit()
    
    return jsonify({
        "message": "Question updated successfully",
        "question": {
            "id": question.id,
            "quiz_id": question.quiz_id,
            "question_statement": question.question_statement,
            "option1": question.option1,
            "option2": question.option2,
            "option3": question.option3,
            "option4": question.option4,
            "correct_option": question.correct_option
        }
    })

# Delete a question (admin only)
@app.route("/api/questions/<int:question_id>", methods=["DELETE"])
@auth_required("token")
@roles_required("Admin")
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    
    return jsonify({"message": "Question deleted successfully"})

# --------- Quiz Attempt Routes ---------

# Get quiz questions for users to attempt (without correct answers)
@app.route("/api/attempt/quizzes/<int:quiz_id>", methods=["GET"])
@auth_required("token")
def get_quiz_for_attempt(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Check if the user has already completed this quiz
    existing_attempt = Score.query.filter_by(
        user_id=current_user.id,
        quiz_id=quiz_id,
        completed=True
    ).first()
    
    if existing_attempt:
        return jsonify({
            "message": "You have already completed this quiz",
            "score": {
                "total_questions": existing_attempt.total_questions,
                "correct_answers": existing_attempt.correct_answers,
                "score_percentage": existing_attempt.total_scored,
                "attempt_date": existing_attempt.time_stamp_of_attempt
            }
        }), 400
    
    # Format quiz data
    quiz_data = {
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "chapter_id": quiz.chapter_id,
        "date_of_quiz": quiz.date_of_quiz.strftime("%Y-%m-%d"),
        "time_duration": quiz.time_duration,
        "questions": []
    }
    
    # Add questions without correct answers
    for question in questions:
        quiz_data["questions"].append({
            "id": question.id,
            "question_statement": question.question_statement,
            "options": [
                question.option1,
                question.option2,
                question.option3,
                question.option4
            ]
        })
    
    return jsonify(quiz_data)

# Submit quiz answers
@app.route("/api/attempt/quizzes/<int:quiz_id>/submit", methods=["POST"])
@auth_required("token")
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    answers = data.get("answers", {})
    
    if not answers:
        return jsonify({"message": "No answers provided"}), 400
    
    # Get all questions for this quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    if not questions:
        return jsonify({"message": "This quiz has no questions"}), 400
    
    # Check existing completed attempts
    existing_attempt = Score.query.filter_by(
        user_id=current_user.id,
        quiz_id=quiz_id,
        completed=True
    ).first()
    
    if existing_attempt:
        return jsonify({
            "message": "You have already completed this quiz",
            "score": {
                "total_questions": existing_attempt.total_questions,
                "correct_answers": existing_attempt.correct_answers,
                "score_percentage": existing_attempt.total_scored,
                "attempt_date": existing_attempt.time_stamp_of_attempt
            }
        }), 400
    
    # Calculate score
    total_questions = len(questions)
    correct_answers = 0
    
    for question in questions:
        str_question_id = str(question.id)
        if str_question_id in answers:
            user_answer = int(answers[str_question_id])
            if user_answer == question.correct_option:
                correct_answers += 1
    
    score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    # Create score record
    new_score = Score(
        quiz_id=quiz_id,
        user_id=current_user.id,
        total_questions=total_questions,
        correct_answers=correct_answers,
        total_scored=score_percentage,
        completed=True
    )
    
    db.session.add(new_score)
    db.session.commit()
    
    return jsonify({
        "message": "Quiz submitted successfully",
        "score": {
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "score_percentage": score_percentage
        }
    })

# Get user's quiz history
@app.route("/api/user/quiz-history", methods=["GET"])
@auth_required("token")
def get_quiz_history():
    scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.time_stamp_of_attempt.desc()).all()
    
    result = []
    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)
        
        result.append({
            "id": score.id,
            "quiz_id": score.quiz_id,
            "quiz_title": quiz.title,
            "chapter_name": chapter.name,
            "subject_name": subject.name,
            "total_questions": score.total_questions,
            "correct_answers": score.correct_answers,
            "score_percentage": score.total_scored,
            "attempt_date": score.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M:%S"),
            "completed": score.completed
        })
    
    return jsonify(result)

# Get all available quizzes for a user
@app.route("/api/user/available-quizzes", methods=["GET"])
@auth_required("token")
def get_available_quizzes():
    # Get all quizzes
    quizzes = Quiz.query.all()
    
    # Get user's completed quizzes
    completed_quiz_ids = [score.quiz_id for score in Score.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).all()]
    
    result = []
    for quiz in quizzes:
        if quiz.id not in completed_quiz_ids:
            chapter = Chapter.query.get(quiz.chapter_id)
            subject = Subject.query.get(chapter.subject_id)
            
            result.append({
                "id": quiz.id,
                "title": quiz.title,
                "description": quiz.description,
                "chapter_name": chapter.name,
                "subject_name": subject.name,
                "date_of_quiz": quiz.date_of_quiz.strftime("%Y-%m-%d"),
                "time_duration": quiz.time_duration
            })
    
    return jsonify(result)