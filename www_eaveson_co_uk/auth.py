import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from dotenv import load_dotenv
import os

load_dotenv()

bp = Blueprint('auth', __name__, url_prefix='/auth')

LOGIN_USERNAME = os.getenv('LOGIN_USERNAME')
LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD')
LOGIN_ID = os.getenv('LOGIN_ID')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if username != LOGIN_USERNAME:
            error = 'Incorrect username.'
        elif password != LOGIN_PASSWORD:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = LOGIN_ID
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = LOGIN_USERNAME

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view