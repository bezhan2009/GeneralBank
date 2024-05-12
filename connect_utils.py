from flask import render_template


def check_conn(conn):
    if conn is None:
        return False
    else:
        return True

"""
def get_manually_connect():
    db_name = request.form['db_name']
    user = request.form['user']
    password = request.form['password']
    conn = manually_connect_p(db_name, user, password)
    session['conn'] = conn

    if conn is None:
        return redirect_to_connect()
    return redirect_to_index()
    
"""