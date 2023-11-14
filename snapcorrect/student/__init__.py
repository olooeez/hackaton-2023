from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from snapcorrect.auth import login_required
from snapcorrect.db import get_db

bp = Blueprint("student", __name__, url_prefix="/student")


@bp.route("/index/<int:id>")
@login_required
def index(id):
    db = get_db()

    query = """
        SELECT
            g.title AS class_title
        FROM
            student s
        JOIN
            grade g ON s.grade_id = g.id
        WHERE
            s.id = ?
    """

    student_classes = db.execute(query, (id,)).fetchall()

    query = """
        SELECT
            g.id AS grade_id,
            g.title AS grade_title,
            t.id AS test_id,
            t.title AS test_title,
            sc.score AS test_score
        FROM
            student s
        JOIN
            student_correction sc ON s.id = sc.student_id
        JOIN
            test t ON sc.test_id = t.id
        JOIN
            grade g ON s.grade_id = g.id
        WHERE
            s.id = ?
    """

    student_exams = db.execute(query, (id,)).fetchall()

    query = """
        SELECT
            s.username AS student_name
        FROM
            student s
        WHERE
            s.id = ?
    """

    student_name = db.execute(query, (id,)).fetchone()["student_name"]

    query = """
        SELECT
            AVG(sc.score) AS average_grade
        FROM
            student_correction sc
        JOIN
            student s ON sc.student_id = s.id
        WHERE
            s.id = ?
    """

    average_grade = db.execute(query, (id,)).fetchone()["average_grade"]

    return render_template("student/index.html", student_classes=student_classes, student_exams=student_exams, student_name=student_name, average_grade=average_grade)


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
