import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for, current_app)

from app.extensions import auth, db
import requests.exceptions
import json
import requests

bp = Blueprint('auth', __name__, url_prefix='/auth')

def verify_recaptcha_token(user_token = None):
    google_recaptcha_uri = 'https://www.google.com/recaptcha/api/siteverify'
    if user_token:
        data = {'secret': current_app.config['RECAPTCHA_SECRET_KEY'], \
                'response': user_token}
        post_response = requests.post(google_recaptcha_uri, data)
        #print(post_response.status_code)
        #print(post_response)
        #print(post_response.text)
        if post_response.status_code == 200:
            # Convert the response to a dict and return the dict["success"]
            response_dict = json.loads(post_response.text)
            #print(response_dict)
            return response_dict["success"]
    return False

@bp.route('/register', methods=('GET', 'POST'))
def register():
    data = requests.get('https://us-central1-shpe-uci-tech.cloudfunctions.net/majors').text
    #print(data)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        recaptcha_response = request.form['g-recaptcha-response']

        error = None

        if verify_recaptcha_token(recaptcha_response):
            print("valid recaptcha")
        else:
            error = "Invalid Recaptcha"
            print("invalid recaptcha")

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try:
                user = auth.create_user_with_email_and_password(email, password)
            except requests.exceptions.HTTPError as e:
                error = json.loads(e.args[1])['error']['message']
                if error == "EMAIL_EXISTS":
                    flash("Email already in use. Please Sign In.")
                else:
                    flash(error)

        if error is None:
            points = {
                "fall": 0,
                "winter": 0,
                "spring": 0
            }
            data = {
                "first_name": request.form['first_name'],
                "last_name": request.form['last_name'],
                "email": email,
                "major": request.form['major'],
                "year": request.form['year'],
                "resume_id": "",
                "is_admin": "False",
                "paid_status": "general"
            }


            user = auth.sign_in_with_email_and_password(email, password)

            db.child("users").child(user["localId"]).set(data)

            db.child("points").child(user["localId"]).set(points)

            session.clear()
            session['user'] = user
            session['name'] = db.child('users').child(user['localId']).get().val()
            return redirect(url_for('dashboard')) 
        else:
            flash(error)

    if g.user is not None:
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
            session['name'] = db.child('users').child(user['localId']).get().val()
            return redirect(url_for('dashboard'))
    if request.method == 'GET':
        if g.user is not None:
            return redirect(url_for('dashboard'))

    return render_template('/auth/login.html')


@bp.before_app_request
# this gets executed before ANY request.
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user = session.get("user")

    try:
        name = session.get('name')['first_name']
    except:
        name = None

    if user is None:
        g.user = None
        g.name = None
    else:
        g.user = user
        g.name = name


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
    # https://github.com/thisbejim/Pyrebase/issues/284
    auth.current_user = None
    return redirect(url_for('auth.login'))


# need to add none default value for file_id