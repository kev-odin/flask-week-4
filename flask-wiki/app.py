import datetime as dt
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, login_required, logout_user
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from models import db, login, UserModel
from wiki import find_birthdays


class LoginForm(FlaskForm):
    email = StringField(label="Enter email", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="Enter password", validators=[DataRequired(), Length(min=6, max=16)]
    )
    submit = SubmitField(label="Login")


class RegisterForm(FlaskForm):
    email = StringField(label="Enter email", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="Enter password", validators=[DataRequired(), Length(min=6, max=16)]
    )
    submit = SubmitField(label="Register")


class SearchBirthday(FlaskForm):
    birthday = DateField(label="Enter birthday", validators=[DataRequired()])
    results = IntegerField(
        label="Number of results",
        validators=[DataRequired(), NumberRange(min=1, max=20)],
    )
    submit = SubmitField(label="Search!")


app = Flask(__name__)
app.secret_key = "a secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/login.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login.init_app(app)


def add_user(email, password):
    # check if email or username exits
    user = UserModel()
    user.set_password(password)
    user.email = email
    db.session.add(user)
    db.session.commit()


def current_date(info: str):
    if info == "today":
        month = dt.datetime.now().strftime("%m")
        day = dt.datetime.now().strftime("%d")
        return f"{month}/{day}"
    elif info == "year":
        return dt.datetime.now().strftime("%Y")


@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email="lhhung@uw.edu").first()
    if user is None:
        add_user("lhhung@uw.edu", "qwerty")


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    title = "Home App"
    form = SearchBirthday()
    myData = find_birthdays(current_date("today"), current_date("year"))

    if form.validate_on_submit():
        if request.method == "POST":
            entry = request.form["birthday"]
            results = request.form["results"]
            month = f"{entry[5:7]}/{entry[8:10]}"
            year = entry[0:4]
            return render_template(
                "home.html",
                title=title,
                form=form,
                myData=find_birthdays(month, year, results),
            )
    return render_template("home.html", title=title, form=form, myData=myData)


@app.route("/")
def redirectToLogin():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    title = "Login Page"
    form = LoginForm()

    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            pw = request.form["password"]
            user = UserModel.query.filter_by(email=email).first()
            if user is not None and user.check_password(pw):
                login_user(user)
                return redirect("/home")
            elif user is not None and not user.check_password(pw):
                flash(f"Incorrect email or password. Please try again.")
    return render_template("login.html", title=title, form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    title = "Registration Page"
    form = RegisterForm()

    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            user = UserModel.query.filter_by(email=email).first()
            if user is None:
                add_user(email, password)
                flash("Registration Completed!")
                return redirect("/login")
            elif user is not None and user.check_password(password):
                login_user(user)
                return redirect("/home")
            else:
                flash("Email has already been taken. Please try another email.")
    return render_template("register.html", title=title, form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
