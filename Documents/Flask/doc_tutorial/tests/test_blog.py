import pytest
from flaskr.db import get_db

def test_index(auth, client):
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Register' in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test \nbody' in response.data
    assert b'href="/1/update/"' in response.data

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == '/auth/login'

def test_author_required(client, app, auth):
    # Change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute(
            "UPDATE post SET author_id = 2 WHERE id = 1"
        )
        db.commit()

    auth.login()
    # If the user is not the author of the post, he should not be able to update/delete it
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # If the user is not the author of the post, he should not be able to see the edit button.
    assert b'href="/1/update"' not in client.get('/').data

@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(auth, client):
    auth.login()
    assert client.post(path).status_code == 404
