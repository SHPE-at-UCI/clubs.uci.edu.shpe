import os
from flask import Flask, render_template, redirect, url_for, g, request, flash
from werkzeug import secure_filename
from app.routes.auth import login_required
from app.extensions import db
# from flask_login import current_user
from flask_recaptcha import ReCaptcha

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.config["PDF_UPLOADS"] = "./app/utils/temp" # Path to save resumes
    PATH_TO_UPLOAD = app.config["PDF_UPLOADS"] #constant term 

    # Configure and Start Google recaptcha
    app.config.update(
        RECAPTCHA_ENABLED= True,
        RECAPTCHA_SITE_KEY= os.getenv("GOOGLE_SITE_KEY"),
        RECAPTCHA_SECRET_KEY= os.getenv("GOOGLE_SECRET_KEY")
    )
    recaptcha = ReCaptcha(app=app)

    @app.after_request
    def add_header(r):
        """
        Add headers to:
            - force latest IE rendering engine or Chrome Frame,
            - to cache the rendered page for 10 minutes.
            
        This prevents browser to cache *.css files
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    from app.utils.google_drive_api import google_drive_auth # google drive api functions
    from app.routes import auth, settings
    from app.routes.search import get_all_users, get_user
    from app.routes import dashboard
    from app.routes.dashboard import allowed_file, delete_file
    from app.routes import faq
    # Register routes
    app.register_blueprint(auth.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(faq.bp)

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


    #new admin route.
    @app.route('/admin')
    @login_required
    def admin():
        users = get_all_users()
        user = db.child(
            'users').child(g.user['localId']).get().val()
        budget = db.child('budget').get().val()
        return render_template('admin.html',users=users, uid = g.user['localId'], user = user, budget=budget)

    @app.route('/checkout')
    @login_required
    def checkout():
        return render_template('checkout.html')


    @app.route('/points')
    @login_required
    def points():
        user = db.child(
            'users').child(g.user['localId']).get().val()
        userPoints = userPoints = db.child(
            'points').child(g.user['localId']).get().val()
        return render_template('points.html', points=userPoints, user=user)

    @app.route('/dashboard', methods=["GET","POST"])
    @login_required
    def dashboard():
        user = db.child(
            'users').child(g.user['localId']).get().val()
        print(user)
        if request.method == "POST":
            user_file = request.files['pdf_uploader']
            if not allowed_file(user_file): #checks if file is pdf
                return redirect(request.url)
            else:
                secure_file = secure_filename(user_file.filename) # holds pdf file from form
                user_file.save(os.path.join(PATH_TO_UPLOAD, secure_file)) # create variable here path to new pdf
                myfilepath = os.path.join(PATH_TO_UPLOAD, secure_file) #hold file path for google drive
                google_drive_auth(myfilepath)
                delete_file(myfilepath)

            return redirect(request.url) #returns url and looks for request object
        # if method is GET then render template
        return render_template("dashboard.html", user=user)

    @app.route('/team')
    def team():
        return render_template('/team.html')

    @app.route('/settings')
    @login_required
    def settings():
        user = db.child(
            'users').child(g.user['localId']).get().val()
        return render_template('settings.html',user=user)

    @app.route('/portfolio/<ucinet>')
    @login_required
    def portfolio(ucinet):
        #print(f"Retrieving Data for {ucinet}")
        userInfo = get_user(ucinet)
        user = db.child(
            'users').child(g.user['localId']).get().val()
        #print(userInfo)
        if userInfo == None:
            return page_not_found("User not found")
        return render_template('portfolio.html', userdata=userInfo, user = user)

    @app.route('/meetteam')
    def meet_team():
        return 'MeetTeam'

    @app.route('/search')
    def search():
        users = get_all_users()
        user = db.child(
            'users').child(g.user['localId']).get().val()
        #for user in users:
        #     print(user)
        print(user)
        return render_template('search.html', users=users, user = user)


    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('/error/404.html', title='404'), 404

    return app
