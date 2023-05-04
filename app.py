"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "bloglysecretkey"

debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def root():
    return render_template("home.html")


@app.route("/users")
def show_users():
    users = User.query.all()
    if len(users) == 0:
        flash("No users")
        return redirect("/")
    return render_template("users.html", users=users)


@app.route("/new-user", methods=["GET"])
def new_user():
    return render_template("new-user.html")


@app.route("/new-user", methods=["POST"])
def add_user():
    new_user = User(
        user_name=request.form["user_name"],
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        image_url=request.form["image_url"] or None,
    )

    db.session.add(new_user)
    db.session.commit()

    flash("User added!")
    return redirect("/new-user")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)


@app.route("/users//<int:user_id>/edit", methods=["POST"])
def save_user_changes(user_id):
    user = User.query.get_or_404(user_id)
    user.user_name = request.form["user_name"]
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/users')