import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

from app.extensions import db
from app.routes.auth import login_required

import requests.exceptions
import json 


bp = Blueprint('settings', __name__, url_prefix='/settings')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def settings():
    if request.method == 'POST':
        data = {
            "first_name":request.form['first_name'],
            "last_name":request.form['last_name'],
            "email":request.form['email'],
            "major":request.form['major'],
            "year":request.form['year']
        }
        db.child("users").child(g.user['localId']).update(data)
        
    user_data = db.child("users").child(g.user['localId']).get().val()
    data = requests.get('https://us-central1-shpe-uci-tech.cloudfunctions.net/majors').text
    return render_template('/settings.html', user=user_data, data=data)