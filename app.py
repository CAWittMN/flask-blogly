"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Post, db, connect_db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "bloglysecretkey"
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
app.debug = True

debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home_page():
    """show home page"""
    posts = Post.query.order_by(Post.created_datetime.desc()).limit(5).all()

    return render_template("home.html", posts=posts)


####################### User routes #########################################


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


######################## Post routes ######################################


@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def new_post(user_id):
    """show new post form"""

    return render_template("new-post.html")


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def save_new_post(user_id):
    """handle saving post to database"""
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form["title"],
        content=request.form["content"],
        user=user,
    )

    db.session.add(new_post)
    db.session.commit()

    flash("Post added!")
    return redirect(f"/users/{user_id}/posts/{new_post.id}")


@app.route("/users/<int:user_id>/posts/<int:post_id>")
def show_post(user_id, post_id):
    """show specific post"""
    post = Post.query.get_or_404(post_id)

    return render_template("post.html", post=post)


@app.route("/users/<int:user_id>/posts/<int:post_id>/edit", methods=["GET"])
def edit_post(user_id, post_id):
    """edit post"""

    post = Post.query.get_or_404(post_id)

    return render_template("edit-post.html", post=post)


@app.route("/users/<int:user_id>/posts/<int:post_id>/edit", methods=["POST"])
def save_post_changes(user_id, post_id):
    post = Post.query.get_or_404(post_id)

    print(request.form["title"])
    print(request.form["content"])
    post.title = request.form["title"]
    post.content = request.form["content"]

    print(post)

    db.session.add(post)
    db.session.commit

    flash("Post updated!")
    return redirect(f"/users/{user_id}/posts/{post_id}")


@app.route("/users/<int:user_id>/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(user_id, post_id):
    """handle post delete"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit

    flash("Post deleted!")
    return redirect(f"/users/{user_id}")
