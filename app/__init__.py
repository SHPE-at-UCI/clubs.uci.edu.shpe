import os

from flask import Flask, render_template, redirect, url_for, g
from app.routes.auth import login_required
from app.extensions import db
# from flask_login import current_user
from flask_recaptcha import ReCaptcha

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    # Configure and Start Google recaptcha
    app.config.update(
        RECAPTCHA_ENABLED= True,
        RECAPTCHA_SITE_KEY= os.getenv("GOOGLE_SITE_KEY"),
        RECAPTCHA_SECRET_KEY= os.getenv("GOOGLE_SECRET_KEY")
    )
    recaptcha = ReCaptcha(app=app)

    from app.routes import auth, settings
    from app.routes.search import get_all_users, get_user

    # Register routes
    app.register_blueprint(auth.bp)
    app.register_blueprint(settings.bp)

    from app.routes import points
    app.register_blueprint(points.bp)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    # There is no need for a homepage.
    def index():
        return redirect(url_for('auth.login'))

    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        # fetch user information from database
        user = db.child('users').child(g.user['localId']).get().val()
        # fetch user points from database
        userPoints = db.child('points').child(g.user['localId']).get().val()
        # load the dashboard with the user information
        return render_template('dashboard.html', user=user, points=userPoints)

    @app.route('/points')
    @login_required
    def points():
        userPoints = userPoints = db.child(
            'points').child(g.user['localId']).get().val()
        return render_template('points.html', points=userPoints)

    @app.route('/team')
    def team():
        return render_template('/team.html')


    @app.route('/settings')
    @login_required
    def settings():
        return render_template('settings.html')

    @app.route('/portfolio/<ucinet>')
    @login_required
    def portfolio(ucinet):
        #print(f"Retrieving Data for {ucinet}")
        userInfo = get_user(ucinet)
        if userInfo == None:
            return page_not_found("User not found")
        return render_template('portfolio.html', userdata=userInfo)

    @app.route('/meetteam')
    def meet_team():
        return 'MeetTeam'

    @app.route('/search')
    def search():
        users = get_all_users()
        # for user in users:
        #     user.print()
        return render_template('search.html', users=users)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('/error/404.html', title='404'), 404

    return app
