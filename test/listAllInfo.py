#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
List All Info
"""

import sqlite3


conn = sqlite3.connect("../wingxel.db")
cur = conn.cursor()

# List all info
try:
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.execute("SELECT * FROM facts")
    facts = cur.fetchall()
    cur.execute("SELECT * FROM history")
    hist = cur.fetchall()
    print("Users:\n")
    for user in users:
        print(user)
    print("\n\nFacts\n")
    for fact in facts:
        print(fact)
    print("\n\nHistory")
    for h in hist:
        print(h)
except Exception as err:
    print(f"Error : {str(err)}")
finally:
    cur.close()
    conn.close()