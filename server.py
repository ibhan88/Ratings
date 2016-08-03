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

@app.route('/register')
def show_register_form():
    """Shows registration form."""

    existing_users = User.query.filter(User.email!=None).all()
    emails = []   
    for user in existing_users:
        emails.append(user.email)

    return render_template("register_form.html", emails=emails)
    # if methods == "GET":
    #     return render_template("register_form.html")
    # else:
    #     #Some CODE
    #     return redirect("/")

@app.route('/user_id_check')
def check_user_id():

    new_email = request.args.get("email")
    print "**********new_email******************************"
    print new_email
    print "****************************************"
    emails = User.query.filter(User.email==new_email).all()
    print "************emails****************************"
    print emails
    print "****************************************"
    #check password too

    if emails:
        print "TRUE"
        return "True"
    else:
        return "False"


@app.route('/register-confirmation', methods=["POST"])
def show_register_confirmation():
    """Shows registration confirmation."""

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
