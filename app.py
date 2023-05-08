"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "bloglysecretkey"
app.config[" = UPLOAD_FOLDERSQLALCHEMY_RECORD_QUERIES"] = True
app.debug = True

debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home_page():
    """show home page"""

    return render_template("home.html")


@app.route("/users", methods=["GET"])
def show_users():
    """show all users"""

    users = User.query.all()

    if len(users) == 0:
        flash("No users")
        return redirect("/")

    return render_template("users.html", users=users)


@app.route("/new-user", methods=["GET"])
def new_user():
    """show new user form"""

    return render_template("new-user.html")


@app.route("/new-user", methods=["POST"])
def add_user():
    """handle adding new user to database"""

    name = User.full_name_dict(request.form["name"].title())

    if name == "Too many names":
        flash(
            "First, middle, and last name only. Please hyphenate multiple last or middle names."
        )
        return redirect("/new-user")

    elif name == "Only one name":
        flash("Please include your last name.")
        return redirect("/new-user")

    new_user = User(
        user_name=request.form["user_name"],
        first_name=name["first_name"],
        middle_name=name["middle_name"],
        last_name=name["last_name"],
        image_url=request.form["image_url"] or None,
    )

    db.session.add(new_user)
    db.session.commit()

    flash("User added!")
    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """show specific user"""

    user = User.query.get_or_404(user_id)
    full_name = User.get_full_name(user)
    return render_template("user.html", user=user, full_name=full_name)


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user_form(user_id):
    """show edit user form"""

    user = User.query.get_or_404(user_id)
    full_name = User.get_full_name(user)
    image_url = User.check_image_url(user.image_url, ["GET"])

    if image_url == None:
        return render_template("edit-user.html", full_name=full_name)

    return render_template("edit-user.html", full_name=full_name, image_url=image_url)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def save_user_changes(user_id):
    """handle updating user in database"""

    user = User.query.get_or_404(user_id)
    name = User.full_name_dict(request.form["name"].title())
    image_url = User.check_image_url(request.form["image_url"] or None, ["POST"])

    if name == "Too many names":
        flash(
            """First, middle, and last name only. 
            Please hyphenate multiple last or middle names."""
        )
        return redirect(f"/users/{user_id}/edit")

    elif name == "Only one name":
        flash("Please include your last name.")
        return redirect(f"/users/{user_id}/edit")

    user.first_name = name["first_name"]
    user.middle_name = name["middle_name"]
    user.last_name = name["last_name"]
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()
    flash("Profile updated!")
    return redirect(f"/users/{user_id}")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """handle deleting user from database"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    flash("Profile deleted!")
    return redirect("/users")
