from flask import Blueprint, render_template
from snapcorrect.auth import login_required

bp = Blueprint("professor", __name__)


@bp.route("/")
@login_required
def index():
    return render_template("professor/index.html")
