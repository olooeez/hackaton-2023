from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from snapcorrect.auth import login_required
from snapcorrect.db import get_db

bp = Blueprint("grade", __name__)


@bp.route("/<int:id>/index")
@login_required
def index(id):
    return render_template("grade/index.html")


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")

        db = get_db()

        error = None

        grade_id = None

        if not name:
            error = "O nome da turma não pode estar vazio."

        if error is None:
            try:
                cursor = db.execute("INSERT INTO grade (professor_id, title) VALUES (?, ?)", (session.get("professor_id"), name,))
                db.commit()
                grade_id = cursor.lastrowid
            except db.IntegrityError:
                error = f"Turma '{name}' já existe."
            else:
                return redirect(url_for('grade.index', id=grade_id))

        flash(error)

    return render_template("grade/create.html")
