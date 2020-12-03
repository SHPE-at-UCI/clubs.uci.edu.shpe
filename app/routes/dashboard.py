import os


from flask import Flask, render_template, redirect, url_for, g, Blueprint, request
from app.routes.auth import login_required #possibly don't need
from app.extensions import db
import app.__init__
# from flask_login import current_user
from flask_recaptcha import ReCaptcha

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
ALLOWED_EXTENSIONS_FOR_FILE_UPLOAD = ["PDF"] #helps check file extension

@bp.route('/')
def login():
    # fetch user information from database
    user = db.child('users').child(g.user['localId']).get().val()
    users = db.child('users').get().val()
    # fetch user points from database
    userPoints = db.child('points').child(g.user['localId']).get().val()
    # load the dashboard with the user information
    return render_template('/dashboard.html', user=user, points=userPoints)


# checks to see if a file is a pdf
def allowed_file(filename):
    if not "." in filename.filename:
        return False
    extension = filename.filename.rsplit(".", 1)[1]
    if extension.upper() in ALLOWED_EXTENSIONS_FOR_FILE_UPLOAD:
        return True
    else:
        return False

def delete_file(filename):
    os.remove(filename)