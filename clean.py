#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
Start a new slate
"""

import os
from consts import Consts


def clean():
    try:
        # remove profile pictures
        for picStr in os.listdir(Consts.SAVE_PROFILE_LOCATION):
            profilePic = os.path.join(Consts.SAVE_PROFILE_LOCATION, picStr)
            if os.path.isfile(profilePic):
                os.remove(profilePic)
        
        # remove db
        db = os.path.join(os.getcwd(), Consts.MY_DB)
        if os.path.isfile(db):
            os.remove(db)
    except Exception:
        pass


if __name__ == "__main__":
    clean()
