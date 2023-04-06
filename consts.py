#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
"""

import os
from datetime import datetime


class Consts:
    SAVE_PROFILE_REL_PATH = os.path.join("static", "img", "profiles")
    SAVE_PROFILE_LOCATION = os.path.join(os.getcwd(), SAVE_PROFILE_REL_PATH)
    W219_29032 = f"wi{datetime.today().minute}ng{datetime.today().hour}xel{datetime.today().year}"
    MY_DB = "wingxel.db"
    ERR_TXT = "Please try again later!"
