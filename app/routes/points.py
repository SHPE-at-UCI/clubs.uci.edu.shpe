import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

from app.extensions import db  #auth
import requests.exceptions
import json

from time import time
from sys import platform

bp = Blueprint('points', __name__, url_prefix='/points')




@bp.route('/editPoints', methods=('GET', 'POST'))
def editPoints():
    if request.method == 'POST':
        points = {                                      # create new points object with the new values
            'fall' : request.form['fallPoints'],
            'winter' : request.form['winterPoints'],
            'spring' : request.form['springPoints']
        }
        user = session.get("user");                    #  get the current user
        pointsRes = db.child("points").child(user["localId"]).set(points)  # set the current user's points in the database
        return redirect(url_for('dashboard'))  # return to dashboard
    return redirect(url_for('points'))
