from flask import Blueprint, render_template, g, session
from snapcorrect.auth import login_required
from snapcorrect.db import get_db

bp = Blueprint("professor", __name__)

@bp.route("/")
@login_required
def index():
    db = get_db()

    tests = db.execute("SELECT * FROM test WHERE professor_id = ?", (session.get("professor_id"),)).fetchall()
    grades = db.execute("SELECT * FROM grade WHERE professor_id = ?", (session.get("professor_id"),)).fetchall()

    return render_template("professor/index.html", tests=tests, grades=grades)
