import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import auth, db
import requests.exceptions
import json

from time import time
from sys import platform

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Below should go all our routes dealing with Registration / Login / Session / Logout


@bp.route('/register', methods=('GET', 'POST'))
def register():
    data = requests.get('https://us-central1-shpe-uci-tech.cloudfunctions.net/majors').text
    print(data)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        try:
            user = auth.create_user_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as e:
            error = json.loads(e.args[1])['error']['message']
            if error == "EMAIL_EXISTS":
                flash("Email already in use. Please Sign In.")
            else:
                flash("An error has occurred.")


        if error is None:
            points = {
                "fall":0,
                "winter":0,
                "spring":0
            }

            data = {
                "first_name":request.form['first_name'],
                "last_name":request.form['last_name'],
                "email":email,
                "major":request.form['major'],
                "year":request.form['year']
            }

            user = auth.sign_in_with_email_and_password(email, password)

            results = db.child("users").child(user["localId"]).set(data)

            pointsRes = db.child("points").child(user["localId"]).set(points)

            session.clear()
            session['user'] = user
            return redirect(url_for('dashboard'))
    return render_template('/auth/register.html', data=data)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        try:
            user = auth.sign_in_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as e:
            error = json.loads(e.args[1])['error']['message']
            print(error)
            flash("Invalid Credentials")

        if error is None:
            session.clear()
            session['user'] = user
            return redirect(url_for('dashboard'))

    return render_template('/auth/login.html')


@bp.before_app_request
# this gets executed before ANY request.
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user = session.get("user")

    # print(user)
    if user is None:
        g.user = None
    else:
        g.user = user
    pass


def login_required(view):
    # Wrapper function to check if user is logged in.
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    auth.current_user = None #https://github.com/thisbejim/Pyrebase/issues/284
    return redirect(url_for('auth.login'))
