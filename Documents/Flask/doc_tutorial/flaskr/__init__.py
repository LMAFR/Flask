# This file will be treated as a package (due to its name)
import os
from flask import Flask
from config import secret_key

# Our application factory function will be "create_app"
def create_app(test_config=None):
    # create and configure the app (Flask instance)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=secret_key,
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
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    # The line below makes equivalent url_for('index') and url_for('blog.index').
    # Anyway, is main function is show the index template in the '/' URL.
    app.add_url_rule('/', endpoint='index')

    return app
