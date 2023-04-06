#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
Flask sign-up, login and logout demo.
Clone from github:
    https://github.com/
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
    allF = dbmanager.getAllFacts(session)
    return render_template("index.html", title="Home", \
        loggedIn=libs.checkIfLoggedIn(session), facts=allF)


@app.route("/sign-pg")
def signPg():
    if libs.checkIfLoggedIn(session):
        return redirect("/")
    return render_template("sign_up.html", title="Sign-Up")


@app.route('/sign-up', methods=["POST"])
def signUp():
    if not libs.checkIfLoggedIn(session) and libs.checkSignUp(request):
        return dbmanager.signUp(request)
    else:
        try:
            request.files["profile"].close()
        except Exception:
            pass
    return Consts.ERR_TXT


@app.route('/login-pg')
def loginPg():
    if libs.checkIfLoggedIn(session):
        return redirect("/")
    return render_template("login.html", title="Login", fromSignUp=libs.checkIfFromSignUp(request.args))


@app.route('/login', methods=["POST"])
def login():
    if not libs.checkIfLoggedIn(session) and libs.checkLogin(request.form):
        result = dbmanager.login(request.form)
        if result[1] is not None:
            for k, v in result[1].items():
                session[k] = v
        return result[0]
    return Consts.ERR_TXT


@app.route('/favicon.ico')
def favicon():
    return send_file("static/img/ven/favicon.ico", "favicon.ico")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/index")


@app.route("/postFact", methods=["POST"])
def postFact():
    if libs.checkIfLoggedIn(session) and libs.checkIfFact(request.form):
        if dbmanager.postFact(request.form, session):
            return "success"
    return Consts.ERR_TXT


@app.route("/post-pg")
def postFactPg():
    if libs.checkIfLoggedIn(session):
        return render_template("postFact.html", title="Post Fact", loggedIn=True)
    return redirect("/login-pg")


@app.route("/like", methods=["POST"])
def like():
    if libs.checkIfLoggedIn(session) and libs.checkIfLikeFormOk(request.form):
        return f"{dbmanager.likeFact(request.form, session)}"
    else:
        return "failed"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
