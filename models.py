"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/user-login-icon-14.png"


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    def __repr__(self):
        user = self
        return f"User id={user.id} user_name={user.user_name} first_name={user.first_name} last_name={user.last_name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)
