import os

from flask import Flask, render_template, redirect, url_for, g, Blueprint, request, jsonify
from app.routes.auth import login_required #possibly don't need
from app.extensions import db
import app.__init__
import requests # methods
# from flask_login import current_user

bp = Blueprint('faq', __name__, url_prefix='/faq')

# This is the main page for the FAQ page
# Returns a page with a search bar, filtering 
# the questions in the database
@bp.route('/', methods=['GET'])
def faq():
    user = db.child(
            'users').child(g.user['localId']).get().val()
    if request.method == 'GET':
        questions = getAllQuestions()
        return render_template('faq/faq.html', questions=questions,user = user)


@bp.route('/post', methods=['GET', 'POST'])
def postQuestion():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        pass


@bp.route('/api/questions', methods=['GET'])
def getAllQuestions():
    if request.method == 'GET':
        return db.child('questions').get().val()

