from flask import (Flask,
                   render_template,
                   redirect
                   )
import psycopg2

app = Flask(__name__)

app.secret_key = 'bezhan200910203040'


def manually_connect(_db_name, _user, _password):
    if not _db_name:
        _db_name = "postgres"
    elif not _user:
        _user = "postgres"
    elif not _user and not _db_name:
        _user = "postgres"
        _db_name = "postgres"

    db_name = _db_name
    user = _user
    password = _password
    port = "5432"
    host = "127.0.0.1"

    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
    except psycopg2.Error as e:
        print(e)
        return False

    return conn


def redirect_to_connect():
    with app.app_context():
        return render_template("error_connection.html")


def redirect_to_index():
    info = {
        'is_success': True,
        'is_logout': True
    }

    with app.app_context():
        return render_template("login.html", info=info)
