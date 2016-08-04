"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
# from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    return render_template("user_list.html", users=users)


@app.route('/login_form')
def login_form():
    """Show login form"""

    return render_template("login_form.html")


@app.route('/login', methods=["POST"])
def login():
    """Login"""

    email = request.form.get("email")
    password = request.form.get("password")

    emails = User.query.filter(User.email==email, User.password==password).all()

    if session["current_user"]:
        flash("You are already logged in.")
        if emails:
            session["current_user"] = email
            flash("Logged in as %s" % email)
            print session
            return redirect("/")
        else:
            flash("That email and password combination is not in the system.")
            return redirect("/login_form")


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop("current_user", None)
   print "****Popped session*******"
   print session
   print "*******************"
   flash("Logged out.")
   return redirect("/")


@app.route('/register')
def show_register_form():
    """Shows registration form."""

    return render_template("register_form.html")


@app.route('/user_id_check')
def check_user_id():

    new_email = request.args.get("email")
    emails = User.query.filter(User.email==new_email).all()
    #check password too

    if emails:
        return "True"
    else:
        return "False"


@app.route('/register-confirmation', methods=["POST"])
def show_register_confirmation():
    """Shows registration confirmation."""
    print "!!!!!!!!!!!!!!!!!!!!HERE!!!!!!!!!!!!!!!!!!!!!"
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    new_user = User(email=email,password=password,age=age,zipcode=zipcode)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
