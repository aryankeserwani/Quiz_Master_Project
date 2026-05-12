from flask import current_app as app, jsonify, request
from flask_security import auth_required, roles_required, current_user
from Backend.models import db, Score, Quiz, Question
from datetime import datetime

# Get scores for current user
@app.route("/api/scores", methods=["GET"])
@auth_required("token")
def get_user_scores():
    scores = Score.query.filter_by(student_id=current_user.id).all()
    result = []
    
    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        result.append({
            "id": score.id,
            "quiz_id": score.quiz_id,
            "quiz_title": quiz.title if quiz else "Unknown",
            "score": score.score,
            "total_questions": score.total_questions,
            "date_taken": score.date_taken.strftime("%Y-%m-%d %H:%M:%S"),
        })
    
    return jsonify(result)

# Get all scores for a specific quiz (admin only)
@app.route("/api/quizzes/<int:quiz_id>/scores", methods=["GET"])
@auth_required("token")
@roles_required("Admin")
def get_quiz_scores(quiz_id):
    # Check if quiz exists
    Quiz.query.get_or_404(quiz_id)
    
    scores = Score.query.filter_by(quiz_id=quiz_id).all()
    result = []
    
    for score in scores:
        student = score.student
        result.append({
            "id": score.id,
            "quiz_id": score.quiz_id,
            "student_id": score.student_id,
            "student_name": f"{student.first_name} {student.last_name}" if student else "Unknown",
            "score": score.score,
            "total_questions": score.total_questions,
            "date_taken": score.date_taken.strftime("%Y-%m-%d %H:%M:%S"),
        })
    
    return jsonify(result)

# Submit a quiz and calculate score
@app.route("/api/quizzes/<int:quiz_id>/submit", methods=["POST"])
@auth_required("token")
def submit_quiz(quiz_id):
    # Check if quiz exists
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Get answers from request
    data = request.get_json()
    answers = data.get("answers", {})
    
    if not answers:
        return jsonify({"message": "No answers provided"}), 400
    
    # Get all questions for the quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    if not questions:
        return jsonify({"message": "No questions found for this quiz"}), 404
    
    total_questions = len(questions)
    correct_answers = 0
    detailed_results = []
    
    # Check each answer
    for question in questions:
        question_id = str(question.id)
        if question_id in answers:
            user_answer = answers[question_id]
            is_correct = user_answer == question.correct_option
            
            if is_correct:
                correct_answers += 1
            
            detailed_results.append({
                "question_id": question.id,
                "question": question.question_statement,
                "user_answer": user_answer,
                "correct_answer": question.correct_option,
                "is_correct": is_correct
            })
    
    # Calculate score as percentage
    score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    # Save score to database
    new_score = Score(
        quiz_id=quiz_id,
        student_id=current_user.id,
        score=score_percentage,
        total_questions=total_questions,
        date_taken=datetime.now()
    )
    
    db.session.add(new_score)
    db.session.commit()
    
    return jsonify({
        "message": "Quiz submitted successfully",
        "score": score_percentage,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "detailed_results": detailed_results,
        "score_id": new_score.id
    })

# Get detailed results for a specific score
@app.route("/api/scores/<int:score_id>/details", methods=["GET"])
@auth_required("token")
def get_score_details(score_id):
    score = Score.query.get_or_404(score_id)
    
    # Check if user is authorized to view this score
    if score.student_id != current_user.id and not current_user.has_role("Admin"):
        return jsonify({"message": "Unauthorized access"}), 403
    
    quiz = Quiz.query.get(score.quiz_id)
    questions = Question.query.filter_by(quiz_id=score.quiz_id).all()
    
    # Get user answers (this would require extending the Score model to store user answers)
    # For now, we'll just return the questions and correct answers
    
    result = {
        "id": score.id,
        "quiz_id": score.quiz_id,
        "quiz_title": quiz.title if quiz else "Unknown",
        "score": score.score,
        "total_questions": score.total_questions,
        "date_taken": score.date_taken.strftime("%Y-%m-%d %H:%M:%S"),
        "questions": [
            {
                "id": q.id,
                "question": q.question_statement,
                "correct_option": q.correct_option,
                "option1": q.option1,
                "option2": q.option2,
                "option3": q.option3,
                "option4": q.option4,
            }
            for q in questions
        ]
    }
    
    return jsonify(result)

# Delete a score (admin only)
@app.route("/api/scores/<int:score_id>", methods=["DELETE"])
@auth_required("token")
@roles_required("Admin")
def delete_score(score_id):
    score = Score.query.get_or_404(score_id)
    db.session.delete(score)
    db.session.commit()
    
    return jsonify({"message": "Score deleted successfully"}) 