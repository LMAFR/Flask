import sqlite3
import pytest
from flaskr.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    
    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False
    
    def fake_inib_db():
        Recorder.called = True

    # monkeypatch replaces init_db by a function (fake_init_db) that records that it has been called.
    monkeypatch.setattr('flaskr.db.init_db', fake_inib_db)
    # result is the result of calling init_db by using command line.
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called