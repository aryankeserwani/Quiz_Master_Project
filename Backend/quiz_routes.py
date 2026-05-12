from flask import current_app as app, jsonify, request
from flask_security import auth_required, roles_required, current_user
from Backend.models import db, Quiz, Chapter, Question, Score, Subject
from datetime import datetime

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