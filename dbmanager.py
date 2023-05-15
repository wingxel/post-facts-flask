#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
"""

import os
import time

from flask import Request
from flask.sessions import SessionMixin

import libs
import sqlite3
import hashlib
from consts import Consts
from queries import Queries
from threading import Thread
from werkzeug.utils import secure_filename


def get_hash(data: str) -> str:
    """
    Get hashed password
    :param data
    """
    return hashlib.sha512(data.encode("utf-8")).hexdigest()


def save_profile(img: str) -> str:
    """
    Save the provided profile image in static/img/profiles
    :param img
    """
    output_file= secure_filename(img.filename)
    # Get the filename extension
    ext = output_file.split('.')[-1]
    # Create a unique filename
    new_filename = f"{time.time_ns()}_{Consts.W219_29032}_{libs.getRandS()}.{ext}"
    try:
        if not os.path.exists(Consts.SAVE_PROFILE_LOCATION):
            os.makedirs(Consts.SAVE_PROFILE_LOCATION)
        img.save(os.path.join(Consts.SAVE_PROFILE_LOCATION, new_filename))
    except Exception as err:
        print(f"An error occurred while saving profile : {str(err)}")
        return ""
    finally:
        img.close()
    return new_filename


def undoSaveProfile(filename: str) -> None:
    """
    Delete saved profile image
    :param filename
    """
    fl = os.path.join(Consts.SAVE_PROFILE_LOCATION, filename)
    try:
        os.remove(fl)
    except Exception as err:
        print(f"Failed to remove file {fl}\nError : {str(err)}")


def signup(request: Request) -> str:
    """
    Save the sign-up info into the database
    :param request
    """
    form = request.form
    conn = sqlite3.connect(Consts.MY_DB)
    cur = conn.cursor()
    try:
        cur.execute(Queries.CREATE_TABLE_USERS)
        data = {
            "fName": form["fName"],
            "lName": form["lName"], 
            "uName": form["uName"], 
            "email": form["email"],
            "fileN": save_profile(request.files["profile"]),
            "pswd": get_hash(form["pwd"])
        }
        # Check if the email already registered
        cur.execute(Queries.CHECK_EMAIL_USER_QUERY, (data["email"],))
        if len(cur.fetchall()) > 0:
            undoSaveProfile(data["fileN"])
            return "Email is already registered"
        
        # Check if the username already registered
        cur.execute(Queries.CHECK_USER_USERNAME_QUERY, (data["uName"],))
        if len(cur.fetchall()) > 0:
            undoSaveProfile(data["fileN"])
            return "Username is already registered"
        
        cur.execute(Queries.INSERT_USER_QUERY, tuple(data.values()))
        # Clear image metadata
        t = Thread(target=libs.clearInfo, args=(data["fileN"],), daemon=True)
        t.start()
    except Exception as err:
        print(f"An error occurred while inserting : {str(err)}")
        return "Please try again later!"
    finally:
        conn.commit()
        cur.close()
        conn.close()
    return "success"


def login(form: dict) -> tuple:
    """
    Authenticate user
    :param form
    """
    conn = sqlite3.connect(Consts.MY_DB)
    cur = conn.cursor()
    ses_data = {
        "firstName": "",
        "lastName": "",
        "username": "",
        "email": "",
        "fileName": ""
    }
    try:
        cur.execute(Queries.CREATE_TABLE_USERS)
        
        data = {
            "uName": form["uName"],
            "pswd": get_hash(form["pwd"])
        }
        
        # Check if the username exists in the database
        cur.execute(Queries.LOGIN_QUERY, (data["uName"],))
        result = cur.fetchall()
        if len(result) == 0:
            return ("Invalid username or password", None,)
        
        # Check if the provided password hash matches the account associated with
        # the provided username
        result = result[0]
        if result[5] != data["pswd"]:
            return ("Invalid username or password", None,)
        # Session data
        ses_data["firstName"] = result[0]
        ses_data["lastName"] = result[1]
        ses_data["username"] = result[2]
        ses_data["email"] = result[3]
        ses_data["fileName"] = os.path.join(Consts.SAVE_PROFILE_REL_PATH, result[4])
        
    except Exception as err:
        print(f"An error occurred while login : {str(err)}")
        return ("Please try again later!", None,)
    finally:
        conn.commit()
        cur.close()
        conn.close()
    return ("success", ses_data)


def postFact(form: dict, session: dict) -> bool:
    """
    Store the posted fact in the database
    :param form
    :param session
    """
    conn = sqlite3.connect(Consts.MY_DB)
    cur = conn.cursor()
    try:
        cur.execute(Queries.CREATE_FACTS_TABLE)
        factId = f"{time.time_ns()}_{Consts.W219_29032}"
        cur.execute(Queries.SAVE_FACT_QUERY, (factId, form["fact"], session["username"], 0,))
        return True
    except Exception as err:
        print(f"An error occurred while saving post : {str(err)}")
    finally:
        conn.commit()
        cur.close()
        conn.close()
    return False


def getAllFacts(session: SessionMixin) -> list:
    """
    Get all the facts
    """
    conn = sqlite3.connect(Consts.MY_DB)
    cur = conn.cursor()
    try:
        cur.execute(Queries.GET_FACTS_QUERY)
        allItems = cur.fetchall()
        repackedItems = []
        # repack all the facts to include user who posted profile image
        # with relative path that is static/img/profiles/image21.png
        for item in allItems:
            imgPath = os.path.join(Consts.SAVE_PROFILE_REL_PATH, item[5])
            repackedItems.append((item[0], item[1], item[2], item[3], item[4], imgPath,
                                  checkIfCurrentUserLikedFact(session, item[0])))
        return repackedItems
    except Exception as err:
        print(f"An error occurred while getting facts : {str(err)}")
    finally:
        cur.close()
        conn.close()
    return []


def likeFact(form: dict, session: dict) -> int:
    """
    Process like form (when the like button is clicked)
    :param form
    :param session
    """
    conn = sqlite3.connect(Consts.MY_DB)
    curr = conn.cursor()
    try:
        curr.execute(Queries.CREATE_HISTORY_TABLE)
        curr.execute(Queries.CHECK_HISTORY_QUERY, (form["factId"], session["username"],))
        toggle = curr.fetchall()
        if len(toggle) == 0:
            # If the user had not previously liked fact, add user info (username)
            # to the history then toggle like to 1 for that user
            curr.execute(Queries.LIKE_FACT_QUERY, (form["factId"],))
            curr.execute(Queries.ADD_HISTORY_QUERY, (form["factId"], session["username"], 0,))
            curr.execute(Queries.TOGGLE_HISTORY_QUERY, (1, form["factId"], session["username"]))
        elif toggle[0][0] == 1:
            # If the user had previously liked the fact, toggle the like to 0 for 
            # that user (the user clicked the undo button)
            curr.execute(Queries.UNLIKE_FACT_QUERY, (form["factId"],))
            curr.execute(Queries.TOGGLE_HISTORY_QUERY, (0, form["factId"], session["username"],))
        else:
            # If the user had previously undone the like (clicked the undo button), toggle
            # the like back to 1 for that user
            curr.execute(Queries.LIKE_FACT_QUERY, (form["factId"],))
            curr.execute(Queries.TOGGLE_HISTORY_QUERY, (1, form["factId"], session["username"],))
        curr.execute(Queries.GET_LIKES, (form["factId"],))
        l = curr.fetchone()
        return l[0] if len(l) >= 1 else 0
    except Exception as err:
        print(f"An error occurred while liking fact : {str(err)}")
    finally:
        conn.commit()
        curr.close()
        conn.close()
    return 0


def checkIfCurrentUserLikedFact(session: dict, factId: str) -> bool:
    """
    Check if the user has liked given fact
    :param session
    :param factId
    """
    if not libs.checkIfLoggedIn(session):
        return False
    conn = sqlite3.connect(Consts.MY_DB)
    cur = conn.cursor()
    try:
        cur.execute(Queries.CHECK_HISTORY_QUERY, (factId, session["username"],))
        toggle = cur.fetchall()
        return len(toggle) >= 1 and toggle[0][0] == 1
    except Exception as err:
        print(f"An error occurred while checking if current user liked fact : {str(err)}")
    finally:
        cur.close()
        conn.close()
    return False
