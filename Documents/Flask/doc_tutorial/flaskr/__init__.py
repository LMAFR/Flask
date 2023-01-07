# This file will be treated as a package (due to its name)
import os
from flask import Flask

# Our application factory function will be "create_app"
def create_app(test_config=None):
    # create and configure the app (Flask instance)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config == 'None':
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # A simple page that says hello

    @app.route('/hello/')
    def hello():
        return 'Hello world!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register.blueprint(auth.bp)

    return app
