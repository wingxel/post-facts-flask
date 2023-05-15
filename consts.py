#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
"""

import os
from datetime import datetime


class Consts:
    # Relative path to the folder where users profile images are saved
    SAVE_PROFILE_REL_PATH = os.path.join("static", "img", "profiles")
    # Absolute path to the folder where users profile images are saved
    SAVE_PROFILE_LOCATION = os.path.join(os.getcwd(), SAVE_PROFILE_REL_PATH)
    # User profile image name
    W219_29032 = f"wi{datetime.today().minute}ng{datetime.today().hour}xel{datetime.today().year}"
    # Database file name
    MY_DB = "wingxel.db"
    # General error
    ERR_TXT = "Please try again later!"
