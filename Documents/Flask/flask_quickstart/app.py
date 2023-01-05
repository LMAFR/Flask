from flask import Flask
from markupsafe import escape
from flask import url_for, redirect, abort
from flask import render_template, request, make_response
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    resp.set_cookie('username', 'aflorido')
    username = request.cookies.get('username')
    return resp

@app.route('/hello/')
@app.route('/hello/<name>')
def hello_world(name=None):
    return render_template('hello.html', name=name)

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
    return redirect(url_for('about'))

# And the format below makes the website raise a 404 error if you write the path with an additional slash at the end of the route
@app.route('/about')
def about():
    abort(401)
    this_is_never_executed()
    return 'The about page'

@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-something'] = 'A value'
    return resp

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     # By default, the method is POST
#     else:
#         return show_the_login_form()

# request object
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
           return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error = error)

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('show_user_profile', username='John Doe'))
    # Create a URL to look at the static file:
    url_for('static', filename='style.css')
    # url_for('', filename='favicon.ico')

# With assert, a message is raised in case the condition is not met )no messages for the two asserts below)
with app.test_request_context('/hello', method = 'POST'):
    assert request.path == '/hello'
    assert request.method == 'POST'

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = method.files['test.txt']
        f.save(f'/var/www/uploads/{secure_filename(f.filename)}')




