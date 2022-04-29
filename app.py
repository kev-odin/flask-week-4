from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange

from yelp import find_coffee


class loginForm(FlaskForm):
    email = StringField(label="Enter email", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="Enter password", validators=[DataRequired(), Length(min=6, max=16)]
    )
    submit = SubmitField(label="Login")


class birthdayForm(FlaskForm):
    date = DateField(label="Enter valid date")
    entries = IntegerField(
        label="Number of entries (1 - 10)", validators=[NumberRange(min=0, max=10)]
    )
    submit = SubmitField(label="Search")


passwords = {"kchung@fake.com": "asdfgh"}

app = Flask(__name__)
app.secret_key = "a secret"


@app.route("/home")
def helloworld():
    return render_template("home.html", myData=find_coffee())


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
