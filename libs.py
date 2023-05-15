#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
"""

import os
import re
from PIL import Image
from imghdr import what
from consts import Consts


class Validator:
    
    @staticmethod
    def __hasWhiteSpace(pasTxt: str) -> bool:
        """
        Check if provided password contains white space characters i.e newline, tab, space e.t.c
        :param passTxt
        """
        frm = re.compile(r"\s")
        return len(frm.findall(pasTxt)) > 0
    
    @staticmethod
    def __hasNoneChar(passTxt: str) -> bool:
        """
        Check provided password has none letter character i.e $, @, # e.t.c
        :param passTxt
        """
        frm = re.compile(r"\W")
        return len(frm.findall(passTxt)) > 0
    
    @staticmethod
    def isPasswordValid(passTxt: str) -> bool:
        """
        Check if the password is valid
        :param passTxt
        """
        return not Validator.__hasWhiteSpace(passTxt) and Validator.__hasNoneChar(passTxt) and \
            len(passTxt) >= 8
    
    @staticmethod
    def isEmailValid(emailTxt: str) -> bool:
        """
        Check if the email has standard email format email@dmn.com 
        (The regex used is not full email validating regex)
        :param emailTxt
        """
        f = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
        return f.match(emailTxt) is not None
    
    @staticmethod
    def __checkIfImage(img: str) -> bool:
        """
        Checks if the profile image is valid image and the size is below 3 MB
        :param img
        """
        check = what(img) is not None and img.seek(0, os.SEEK_END) < (3 *1024 * 1024)
        img.seek(0)
        return check
    
    @staticmethod
    def checkIfValidImage(img: str) -> bool:
        """
        Check if the profile image is valid
        :param img: String file path
        """
        return img.filename != "" and Validator.__checkIfImage(img)


def checkSignUp(request: dict) -> bool:
    """
    Check if all the input fields of sign-up form are filled (not empty)
    Also checks if the profile image is valid
    :param request
    """
    form = request.form
    params = ["fName", "lName", "uName", "email", "pwd", "csrf_token"]
    return all(key in form for key in params) and \
        Validator.isPasswordValid(form["pwd"]) and Validator.isEmailValid(form["email"]) and \
        len(form["fName"].strip()) > 0 and len(form["lName"].strip()) > 0 and \
        len(form["uName"].strip()) > 0 and Validator.checkIfValidImage(request.files["profile"])


def checkLogin(form: dict) -> bool:
    """
    Check if all the input fields of login form are filled
    :param form
    """
    params = ["uName", "pwd", "csrf_token"]
    return all(key in form for key in params) and len(form["pwd"]) > 0 and len(form["uName"]) > 0


def checkIfFromSignUp(form: dict) -> bool:
    """
    Check if user was redirected from sign-up page
    :param form
    """
    return "signup" in form


def checkIfLoggedIn(session: dict) -> bool:
    """
    Check if the user is logged in
    :param session
    """
    params = ["firstName", "lastName", "username", "email"]
    return all(key in session for key in params)


def checkIfFact(form: dict) -> bool:
    """
    Check if all the input fields of post fact form are filled
    :param form
    """
    params = ["csrf_token", "fact"]
    return all(key in form for key in params)


def checkIfLikeFormOk(form: dict) -> bool:
    """
    Check if all the input fields of like form are filled
    :param form
    """
    params = ["csrf_token", "factId"]
    return all(key in form for key in params)


def getRandS(length=8) -> str:
    """
    Generate a random hex string
    :param length
    """
    return os.urandom(length).hex()


def clearInfo(fileName) -> None:
    """
    Clear image metadata
    :param fileName
    """
    try:
        src = os.path.join(Consts.SAVE_PROFILE_LOCATION, fileName)
        with Image.open(src) as img:
            mBytes = list(img.getdata())
            nImg = Image.new(img.mode, img.size)
            nImg.putdata(mBytes)
            nImg.save(src)
            nImg.close()
    except Exception:
        pass
