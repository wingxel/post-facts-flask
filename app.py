#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
Flask sign-up, login and logout demo.
Clone from github:
    https://github.com/wingxel/post-facts-flask.git
--------------------------------------------
Rate/Share: https://play.google.com/store/apps/details?id=com.wingxel.python
"""

import libs
import dbmanager
from consts import Consts
from flask_wtf.csrf import CSRFProtect
from flask import render_template, Flask, send_file, request, session, redirect


app = Flask(__name__)
app.config["SECRET_KEY"] = libs.getRandS(32)
csrf = CSRFProtect(app)
csrf.init_app(app)


@app.route("/index")
@app.route("/home")
@app.route("/")
def index():
    """
    Load home page
    """
    # Get all the facts from the database to display on home page
    allF = dbmanager.getAllFacts(session)
    return render_template("index.html", title="Home", \
        loggedIn=libs.checkIfLoggedIn(session), facts=allF)


@app.route("/sign-pg")
def signPg():
    """
    Load sign-up page
    """
    # If user is already logged in redirect to home page
    if libs.checkIfLoggedIn(session):
        return redirect("/")
    return render_template("sign_up.html", title="Sign-Up")


@app.route('/sign-up', methods=["POST"])
def signUp():
    """
    Process sign-up form
    """
    # Check if user is not logged in and if sign-up form data was entered correctly
    # Before the form is submitted to the backend, it's checked by client side js
    # but it's a good idea to also check in the backend (The form could not
    # have been submitted from the browser i.e the script in test/testSignUp.py)
    if not libs.checkIfLoggedIn(session) and libs.checkSignUp(request):
        return dbmanager.signup(request)
    else:
        try:
            request.files["profile"].close()
        except Exception:
            pass
    return Consts.ERR_TXT


@app.route('/login-pg')
def loginPg():
    """
    Load login page
    """
    # If user is already logged in redirect to home page
    if libs.checkIfLoggedIn(session):
        return redirect("/")
    return render_template("login.html", title="Login", fromSignUp=libs.checkIfFromSignUp(request.args))


@app.route('/login', methods=["POST"])
def login():
    """
    Process login form
    """
    # Check if the user is not logged in and if the login form was filled correctly
    if not libs.checkIfLoggedIn(session) and libs.checkLogin(request.form):
        # Authenticate user and get basic info (names, email and profile image)
        result = dbmanager.login(request.form)
        # Add basic info to the session
        if result[1] is not None:
            for k, v in result[1].items():
                session[k] = v
        return result[0]
    return Consts.ERR_TXT


@app.route('/favicon.ico')
def favicon():
    """
    Load the website icon
    """
    return send_file("static/img/ven/favicon.ico", "favicon.ico")


@app.route("/logout")
def logout():
    """
    Logout by clearing session data
    """
    session.clear()
    return redirect("/index")


@app.route("/postFact", methods=["POST"])
def postFact():
    """
    Store a fact in database
    """
    # Check if user is logged in and if the fact form is not empty
    if libs.checkIfLoggedIn(session) and libs.checkIfFact(request.form):
        if dbmanager.postFact(request.form, session):
            return "success"
    return Consts.ERR_TXT


@app.route("/post-pg")
def postFactPg():
    """
    Load the post fact page
    """
    # Only logged in users can post facts. If user is not logged in
    # redirect to login page
    if libs.checkIfLoggedIn(session):
        return render_template("postFact.html", title="Post Fact", loggedIn=True)
    return redirect("/login-pg")


@app.route("/like", methods=["POST"])
def like():
    """
    Process like form
    """
    # Check if the user is logged in and if the like form contains required info
    if libs.checkIfLoggedIn(session) and libs.checkIfLikeFormOk(request.form):
        return f"{dbmanager.likeFact(request.form, session)}"
    else:
        return "failed"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
