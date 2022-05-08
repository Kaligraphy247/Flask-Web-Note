from flask import Blueprint, render_template, request, flash, jsonify
from .models import Note
from . import db
import json
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user
)

# this file is a blueprint for routes in the app


views = Blueprint(name='views', import_name=__name__)

@views.route('/', methods=["GET", "POST"])
@login_required # make sure user is logged in to acces this page
def home_view():
    if request.method == "POST":
        note = request.form.get('note')

        if len(note) < 1:
            flash(message='Note is too short! 🙃', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash(message="Note added! 😇", category='sucess')

    return render_template(template_name_or_list="home.html", user=current_user)


@views.route('/note-lists', methods=["GET"]) # methods is optional,since get is default
def view_notes():
    if request.method == "GET":
        note = request.form.get('note')
    return render_template(template_name_or_list="note_lists.html", user=current_user)


@views.route('/note-list/<int:id>', methods=["GET", "POST"]) # methods is optional,since get is default
def edit_notes():
    if request.method == "GET":
        note = request.form.get('note')
    return render_template(template_name_or_list="note_lists.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id  == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})