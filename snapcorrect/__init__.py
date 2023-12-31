import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        UPLOAD_FOLDER="/snapcorrect/static/uploads",
        DATABASE=os.path.join(app.instance_path, "snapcorrect.sqlite"),
        ALLOWED_EXTENSIONS={"png", "jpg"}
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    from . import auth
    from . import professor
    from . import grade
    from . import test
    from . import student

    app.register_blueprint(auth.bp)
    app.register_blueprint(professor.bp)
    app.register_blueprint(grade.bp)
    app.register_blueprint(test.bp)
    app.register_blueprint(student.bp)

    app.add_url_rule("/", endpoint="index")

    return app
