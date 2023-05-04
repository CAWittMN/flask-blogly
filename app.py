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

@app.route('/new-user', methods=['GET'])
def new_user():
    return render_template('new-user.html')

@app.route('/new-user', methods=['POST'])
def add_user():
    new_user = User(
        user_name=request.form['user_name'], 
        first_name=request.form['first_name'], 
        last_name=request.form['last_name'], 
        image_url=request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    flash('User added!')
    return redirect('/new-user')