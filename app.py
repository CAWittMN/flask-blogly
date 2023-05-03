"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = 'bloglysecretkey'

toolbar = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/users')
def show_users():
    users = User.query.all()
    if len(users) == 0:
        flash('No users')
        return redirect('/')
    return render_template('users.html', users=users)

@app.route('/new-user' )
def new_user():
    return render_template('new-user')
