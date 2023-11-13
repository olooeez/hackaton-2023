from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from snapcorrect.auth import login_required
from snapcorrect.db import get_db

bp = Blueprint("student", __name__, url_prefix="/student")


@bp.route("/create", methods=["POST"])
@login_required
def create():
    name = request.form.get("name")
    grade = request.form.get("grade")

    db = get_db()

    error = None

    if not name:
        error = "Nome do aluno tem que estár presente."

    if not grade:
        error = "Turma do aluno não especificada."

    if error is None:
        try:
            db.execute("INSERT INTO student (username, professor_id, grade_id) VALUES (?, ?, ?)",
                    (name, session.get("professor_id"), grade,))
            db.commit()
        except db.IntegrityError:
            error = f"Aluno '{name}' já existe"
        else:
            return redirect(url_for("grade.index", id=grade))

    flash(error)

    return render_template("professor/index.html")

@bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    grade = request.form.get("grade")

    db = get_db()

    db.execute("DELETE FROM student WHERE id = ?", (id,))
    db.commit()

    return redirect(url_for("grade.index", id=grade))

@bp.route("/edit/<int:id>", methods=["POST"])
@login_required
def edit(id):
    grade = request.form.get("grade")
    name = request.form.get("student_name")

    db = get_db()

    db.execute("UPDATE student SET username = ? WHERE id = ?", (name, id,))
    db.commit()

    return redirect(url_for('grade.index', id=grade))
