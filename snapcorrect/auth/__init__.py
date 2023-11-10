import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    professor_id = session.get("professor_id")

    if professor_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM professor WHERE id = ?",
            (professor_id,)
        ).fetchone()


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        db = get_db()

        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if password != confirm:
            error = "Password must match."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO professor (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()

        error = None

        professor = db.execute(
            "SELECT * FROM professor WHERE username = ?",
            (username,)
        ).fetchone()

        if professor is None:
            error = "Incorrect username."
        elif not check_password_hash(professor["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["professor_id"] = professor["id"]

            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("index"))
