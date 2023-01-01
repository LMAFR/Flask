from flask import Flask
from markupsafe import escape
from flask import url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/<name>')
def hello_world(name):
    return f"Hello {escape(name)}!"

@app.route('/user/<username>')
def show_user_profile(username):
    # Show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Show the id of the current post
    return f'Post {escape(post_id)}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # Show the subpath after /path/
    return f'Subpath: {escape(subpath)}'

# The next way to write a route makes the website redirect you to the version with slash at the end in case you write the path without that slash
@app.route('/projects/')
def projects():
    return 'The project page'

# And the format below makes the website raise a 404 error if you write the path with an additional slash at the end of the route
@app.route('/about')
def about():
    return 'The about page'

@app.route('/login')
def login():
    return 'login'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('show_user_profile', username='John Doe'))