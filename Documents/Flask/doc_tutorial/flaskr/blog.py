from flask import (
    Blueprint, g, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u WHERE p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    
    # In the line below I think posts is an optional argument, being the argument variable the one we will use in the HTML template.
    return render_template('blog/index.html', posts=posts)
