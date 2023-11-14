from flask import Blueprint, request, flash, redirect, render_template, session, url_for
from snapcorrect.auth import login_required
from snapcorrect.db import get_db
import os
import cv2
from snapcorrect.ia import load_and_preprocess_image, find_document_contour, preprocess_paper_image, find_question_contours, analyze_answers, get_answers_tamplate
from werkzeug.utils import secure_filename
from snapcorrect.utils import generate_random_filename

bp = Blueprint("test", __name__, url_prefix="/test")


@bp.route("/<int:id>/index")
@login_required
def index(id):
    db = get_db()

    query = """
        SELECT
            title AS test_title,
            id AS test_id
        FROM
            test
        WHERE
            id = ?
    """

    test = db.execute(query, (id,)).fetchone()

    query = """
        SELECT
            s.id AS student_id,
            s.username AS student_name,
            CASE
                WHEN sc.test_id IS NOT NULL THEN 1
                ELSE 0
            END AS has_taken_test
        FROM
            student s
        JOIN test t ON s.grade_id = t.grade_id
        LEFT JOIN student_correction sc ON s.id = sc.student_id AND t.id = sc.test_id
        WHERE
            t.id = ?
    """

    students = db.execute(query, (id,)).fetchall()

    return render_template("test/index.html", test=test, students=students)

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
                template_filename = secure_filename(generate_random_filename(template.filename.rsplit('.', 1)[1]))
                template.save(os.path.join("snapcorrect/static/uploads/", template_filename))
            
                cursor = db.execute("INSERT INTO test (professor_id, grade_id, title, template) VALUES (?, ?, ?, ?)", (session.get(
                    "professor_id"), grade, name, template_filename,))
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


@bp.route("/correct/<int:id>", methods=["POST", "GET"])
@login_required
def correct(id):
    db = get_db()

    query = """
        SELECT
            template
        FROM
            test
        WHERE
            id = ?
    """

    result = db.execute(query, (id,)).fetchone()

    template = result["template"]
    template =  os.path.join("snapcorrect/static/uploads/", template)

    image, gray, edged = load_and_preprocess_image(template)
    docCnt = find_document_contour(edged)
    paper, thresh = preprocess_paper_image(image, gray, docCnt)
    templateCnts = find_question_contours(thresh)
    gab = get_answers_tamplate(templateCnts, thresh)

    test = request.files.get("test")

    test_temp = "temp" + test.filename
    test.save(test_temp)

    image, gray, edged = load_and_preprocess_image(test_temp)
    docCnt = find_document_contour(edged)
    paper, thresh = preprocess_paper_image(image, gray, docCnt)
    questionCnts = find_question_contours(thresh)
    correct = analyze_answers(questionCnts, thresh, paper, gab)

    score = (correct / 5.0) * 100

    student = request.form.get("student")

    test_filename = secure_filename(generate_random_filename(test.filename.rsplit('.', 1)[1]))
    test_path = os.path.join("snapcorrect/static/uploads/", test_filename)
    cv2.imwrite(test_path, paper)

    query = """
        INSERT INTO student_correction (test_id, student_id, score, corrected_test)
        VALUES (?, ?, ?, ?)
    """

    db.execute(query, (id, student, score, "uploads/" + test_filename))
    db.commit()

    os.remove("temp" + test.filename)

    return redirect(url_for('test.index', id=id))

@bp.route("/dashboard/<int:id>")
@login_required
def dashboard(id):
    db = get_db()

    query = """
        SELECT
            s.username AS username,
            sc.score AS score,
            sc.corrected_test AS corrected_test
        FROM
            student_correction sc
        JOIN
            student s ON sc.student_id = s.id
        JOIN
            test t ON sc.test_id = t.id
        JOIN
            grade g ON t.grade_id = g.id
        WHERE
            t.id = ?
    """

    students = db.execute(query, (id,)).fetchall()

    return render_template("test/dashboard.html", students=students)
