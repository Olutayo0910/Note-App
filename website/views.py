from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if 'note' in request.form:
            # Adding a new note
            note_content = request.form.get('note')
            if len(note_content) < 1:
                flash('Note is empty!', category='error')
            else:
                new_note = Note(data=note_content, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')
        elif 'note_id' in request.form and 'note_content' in request.form:
            # Editing an existing note
            note_id = request.form.get('note_id')
            note_content = request.form.get('note_content')
            note = Note.query.get(note_id)
            if note and note.user_id == current_user.id:
                note.data = note_content
                db.session.commit()
                flash('Note edited!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data.decode('utf-8'))
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return jsonify({})
