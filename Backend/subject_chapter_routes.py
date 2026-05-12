from flask import current_app as app, jsonify, request
from flask_security import auth_required, roles_required, current_user
from Backend.models import db, Subject, Chapter, Quiz

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
            "description": subject.description
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
        "description": subject.description
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
    
    # Check if subject with the same name already exists
    existing_subject = Subject.query.filter_by(name=name).first()
    if existing_subject:
        return jsonify({"message": "Subject with this name already exists"}), 400
    
    new_subject = Subject(
        name=name,
        description=description
    )
    
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
        # Check if another subject with the same name already exists
        existing_subject = Subject.query.filter_by(name=name).first()
        if existing_subject and existing_subject.id != subject_id:
            return jsonify({"message": "Subject with this name already exists"}), 400
        
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
    
    # Check if subject has associated chapters
    chapters = Chapter.query.filter_by(subject_id=subject_id).first()
    if chapters:
        return jsonify({"message": "Cannot delete subject with associated chapters"}), 400
    
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
            "subject_id": chapter.subject_id
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
        "subject_id": chapter.subject_id
    })

# Create a new chapter (admin only)
@app.route("/api/subjects/<int:subject_id>/chapters", methods=["POST"])
@auth_required("token")
@roles_required("Admin")
def create_chapter(subject_id):
    Subject.query.get_or_404(subject_id)  # Check if subject exists
    data = request.get_json()
    
    name = data.get("name")
    description = data.get("description", "")
    
    if not name:
        return jsonify({"message": "Chapter name is required"}), 400
    
    # Check if chapter with the same name already exists for this subject
    existing_chapter = Chapter.query.filter_by(name=name, subject_id=subject_id).first()
    if existing_chapter:
        return jsonify({"message": "Chapter with this name already exists for this subject"}), 400
    
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
        # Check if another chapter with the same name already exists for this subject
        existing_chapter = Chapter.query.filter_by(name=name, subject_id=chapter.subject_id).first()
        if existing_chapter and existing_chapter.id != chapter_id:
            return jsonify({"message": "Chapter with this name already exists for this subject"}), 400
        
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
    
    # Check if chapter has associated quizzes
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).first()
    if quizzes:
        return jsonify({"message": "Cannot delete chapter with associated quizzes"}), 400
    
    db.session.delete(chapter)
    db.session.commit()
    
    return jsonify({"message": "Chapter deleted successfully"}) 