from flask import render_template


def check_conn(conn):
    if conn is None:
        return False
    else:
        return True
