from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from snapcorrect.auth import login_required
from snapcorrect.db import get_db

bp = Blueprint("grade", __name__, url_prefix="/grade")


@bp.route("/<int:id>/index")
@login_required
def index(id):
    db = get_db()

    grade = db.execute("SELECT * FROM grade WHERE professor_id = ? AND id = ?",
                       (session.get("professor_id"), id,)).fetchone()

    query = """
        SELECT g.id AS grade_id, g.title AS grade_title, s.id AS student_id, s.username AS student_username, COALESCE(SUM(sc.score), 0) AS total_score 
        FROM student AS s JOIN grade AS g ON s.grade_id = g.id LEFT JOIN student_correction AS sc ON s.id = sc.student_id
        WHERE s.grade_id = ? GROUP BY s.id, g.id
    """

    students = db.execute(query, (id,)).fetchall()

    return render_template("grade/index.html", grade=grade, students=students)


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
                cursor = db.execute(
                    "INSERT INTO grade (professor_id, title) VALUES (?, ?)", (session.get("professor_id"), name,))
                db.commit()
                grade_id = cursor.lastrowid
            except db.IntegrityError:
                error = f"Turma '{name}' já existe."
            else:
                return redirect(url_for('grade.index', id=grade_id))

        flash(error)

    return render_template("grade/create.html")
