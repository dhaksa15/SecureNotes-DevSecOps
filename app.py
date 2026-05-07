"""SecureNotes - A modern Flask notes app with cybersecurity-inspired dark UI."""
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Note

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///securenotes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def login_required(view):
    from functools import wraps
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def current_user():
    uid = session.get("user_id")
    return User.query.get(uid) if uid else None


@app.context_processor
def inject_user():
    return {"current_user": current_user()}


# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if not username or not password:
            flash("Username and password are required.", "danger")
        elif password != confirm:
            flash("Passwords do not match.", "danger")
        elif User.query.filter_by(username=username).first():
            flash("That username is already taken.", "danger")
        else:
            user = User(username=username, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash("Account created. You can log in now.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            flash(f"Welcome back, {user.username}.", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user = current_user()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if not title:
            flash("Note title is required.", "danger")
        else:
            note = Note(title=title, content=content, user_id=user.id)
            db.session.add(note)
            db.session.commit()
            flash("Note created.", "success")
        return redirect(url_for("dashboard"))
    notes = Note.query.filter_by(user_id=user.id).order_by(Note.updated_at.desc()).all()
    return render_template("dashboard.html", notes=notes)


@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    user = current_user()
    note = Note.query.filter_by(id=note_id, user_id=user.id).first_or_404()
    if request.method == "POST":
        note.title = request.form.get("title", "").strip() or note.title
        note.content = request.form.get("content", "").strip()
        note.updated_at = datetime.utcnow()
        db.session.commit()
        flash("Note updated.", "success")
        return redirect(url_for("dashboard"))
    return render_template("edit_note.html", note=note)


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    user = current_user()
    note = Note.query.filter_by(id=note_id, user_id=user.id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "info")
    return redirect(url_for("dashboard"))


# ---------- Bootstrap DB + dummy data ----------
def seed():
    if not User.query.filter_by(username="demo").first():
        demo = User(username="demo", password_hash=generate_password_hash("demo1234"))
        db.session.add(demo)
        db.session.commit()
        samples = [
            ("Welcome to SecureNotes", "This is your private encrypted-feeling vault. Try editing or deleting this note."),
            ("Security checklist", "- Use a password manager\n- Enable 2FA\n- Patch systems weekly\n- Review access logs"),
            ("Ideas", "Draft a write-up on session management and CSRF mitigation."),
        ]
        for t, c in samples:
            db.session.add(Note(title=t, content=c, user_id=demo.id))
        db.session.commit()


with app.app_context():
    db.create_all()
    seed()


if __name__ == "__main__":
    app.run(debug=True)
