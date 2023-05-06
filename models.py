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
        return f"""User id={user.id} 
        user_name={user.user_name} 
        first_name={user.first_name}
        middle_name={user.middle_name} 
        last_name={user.last_name}"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    middle_name = db.Column(db.Text)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    @classmethod
    def get_full_name(cls, user):
        """Return a string built from user data"""

        if user.middle_name == None:
            return f"""{user.first_name} {user.last_name}"""
        return f"{user.first_name} {user.middle_name} {user.last_name}"

    @classmethod
    def full_name_dict(cls, name):
        """create a name dictionary from a string name"""

        split_name = name.split()

        if len(split_name) == 1:
            result = "Only one name"
            return result
        elif len(split_name) > 3:
            result = "Too many names"
            return result
        elif len(split_name) == 2:
            split_name.insert(1, None)

        name_dict = dict(
            first_name=split_name[0], middle_name=split_name[1], last_name=split_name[2]
        )

        return name_dict

    @classmethod
    def check_image_url(cls, url, method):
        """check if image url is the default url and retrun appropriate based on method"""

        if url == None and method == ["POST"]:
            return DEFAULT_IMAGE_URL
        elif url == DEFAULT_IMAGE_URL and method == ["GET"]:
            return None
        return url
