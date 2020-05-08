from flask import (Blueprint, redirect, request,
                   session, url_for)

from app.extensions import db


bp = Blueprint('points', __name__, url_prefix='/points')
@bp.route('/editPoints', methods=('GET', 'POST'))
def editPoints():
    if request.method == 'POST':
        # create new points object with the new values
        points = {
            'fall': request.form['fallPoints'],
            'winter': request.form['winterPoints'],
            'spring': request.form['springPoints']
        }
        #  get the current user
        user = session.get("user")
        # set the current user's points in the database
        db.child("points").child(user["localId"]).set(points)
        return redirect(url_for('dashboard'))  # return to dashboard
    return redirect(url_for('points'))
