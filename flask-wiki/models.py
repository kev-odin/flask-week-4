from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login = LoginManager()


class UserModel(UserMixin, db.Model):
    """
    Base ORM table to be used with SQLAlchemy
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        """
        Security measure to ensure no passwords are hard coded within the application.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Security measuer to validate passwords within a database.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.id} | {self.email}"


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
