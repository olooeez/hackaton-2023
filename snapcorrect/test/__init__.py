from flask import Blueprint, request, flash, redirect, render_template, session, url_for
from snapcorrect.auth import login_required
from snapcorrect.db import get_db

bp = Blueprint("test", __name__, url_prefix="/test")


@bp.route("/<int:id>/index")
@login_required
def index(id):
    return render_template("test/index.html")


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")
        template = request.files.get("template")
        grade = request.form.get("grade")

        db = get_db()

        error = None

        test_id = None

        if not template:
            error = "Foto do gabarito tem que ser enviada."

        if not name:
            error = "Nome da turma não pode estar vazio."

        if not grade:
            error = "Turma não foi especificada."

        if error is None:
            try:
                cursor = db.execute("INSERT INTO test (professor_id, grade_id, title, template) VALUES (?, ?, ?, ?)", (session.get(
                    "professor_id"), grade, name, template.read(),))
                db.commit()
                test_id = cursor.lastrowid
            except db.IntegrityError:
                error = f"Prova '{name}' já existe."
            else:
                return redirect(url_for("test.index", id=test_id))

        flash(error)
    
    db = get_db()

    error = None

    grades = db.execute("SELECT id, title FROM grade").fetchall()

    return render_template("test/create.html", grades=grades)
