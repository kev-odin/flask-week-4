from datetime import date
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from wiki import find_births


class loginForm(FlaskForm):
    email = StringField(label="Enter email", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="Enter password", validators=[DataRequired(), Length(min=6, max=16)]
    )
    submit = SubmitField(label="Login")


class searchForm(FlaskForm):
    min_entry = 1
    max_entry = 20
    date = StringField(validators=[DataRequired()])
    entries = IntegerField(
        validators=[
            DataRequired(),
            NumberRange(
                min=min_entry,
                max=max_entry,
                message=f"Values are only valid between {min_entry}-{max_entry}",
            ),
        ]
    )
    submit = SubmitField(label="Search")


passwords = {}
passwords["lhhung@uw.edu"] = "qwerty"

app = Flask(__name__)
app.secret_key = "a secret"


@app.route("/home", methods=["GET", "POST"])
def index():
    form = searchForm()
    return render_template("home.html", myData=find_births())


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    form = loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            user = request.form["email"]
            pw = request.form["password"]
            if user is not None and user in passwords and passwords[user] == pw:
                return redirect("/home")
    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
