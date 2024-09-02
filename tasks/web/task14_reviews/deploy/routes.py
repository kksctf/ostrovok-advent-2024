import base64
import io
import json
from functools import wraps

from ext import db, login_manager
from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required, login_user, logout_user
from models import Log, Note, User

main = Blueprint("main", __name__)


def encode_log(text: str) -> str:
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')


def log_action(action_description: str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated:
                note_text = request.form.get("note")
                if note_text:
                    encoded_text = encode_log(note_text)
                else:
                    encoded_text = ""

                log_entry = Log(user_id=current_user.id, action=action_description, text=encoded_text)
                db.session.add(log_entry)
                db.session.commit()
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.main_pages"))
    return render_template("index.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for("main.register"))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("main.main_pages"))
    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.main_pages"))
        flash("Invalid username or password")
        return redirect(url_for("main.login"))

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main.route("/main")
@login_required
def main_pages():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes.html", notes=notes)


@main.route("/add_note", methods=["POST"])
@log_action("Added a new note")
@login_required
def add_note():
    note_text = request.form.get("note")
    new_note = Note(text=note_text, user_id=current_user.id)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for("main.main_pages"))


@main.route("/delete_note/<int:note_id>")
@log_action("Deleted a note")
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for("main.main_pages"))


@main.route("/edit_note/<int:note_id>", methods=["POST"])
@log_action("Edited a note")
@login_required
def edit_note(note_id):
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        note.text = request.form.get("note")
        db.session.commit()
    return redirect(url_for("main.main_pages"))


@main.route("/logs")
@login_required
def view_logs():
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    return render_template("logs.html", logs=logs)


@main.route('/export_logs', methods=['GET'])
@login_required
def export_logs():
    logs = Log.query.all()
    logs_data = [{
        'timestamp': log.timestamp,
        'user': log.user.username,
        'action': log.action,
        'text': log.text
    } for log in logs]

    json_data = json.dumps(logs_data, default=str)

    json_file = io.BytesIO()
    json_file.write(json_data.encode('utf-8'))
    json_file.seek(0)

    return send_file(json_file, as_attachment=True, download_name='logs.json', mimetype='application/json')
