from flask import Blueprint
from snapcorrect.auth import login_required

bp = Blueprint("test", __name__)


@bp.route("/<int:id>/index")
@login_required
def index(id):
    pass


@bp.route("/create")
@login_required
def create():
    pass
