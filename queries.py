#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
SQL Queries for each action
"""

class Queries:
    CREATE_TABLE_USERS = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER NOT NULL PRIMARY KEY,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL,
        username VARCHAR NOT NULL UNIQUE,
        email VARCHAR NOT NULL UNIQUE,
        fileN VARCHAR NOT NULL,
        pswd VARCHAR NOT NULL,
        registered_on DATETIME DEFAULT CURRENT_TIMESTAMP)
        """
    INSERT_USER_QUERY = """ INSERT INTO users (firstName, lastName, username, email, fileN, pswd)
        VALUES (?, ?, ?, ?, ?, ?)
        """
    CHECK_EMAIL_USER_QUERY = """SELECT email FROM users WHERE email=?"""
    CHECK_USER_USERNAME_QUERY = """SELECT username FROM users WHERE username=?"""
    LOGIN_QUERY = """SELECT firstName, lastName, username, email, fileN, pswd FROM users WHERE username=?"""
    
    CREATE_FACTS_TABLE = """CREATE TABLE IF NOT EXISTS facts (
        id INTEGER NOT NULL PRIMARY KEY,
        factId VARCHAR NOT NULL UNIQUE,
        fact VARCHAR NOT NULL,
        username VARCHAR NOT NULL,
        likes INTEGER NOT NULL,
        posted_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(username) REFERENCES users(username))
        """
    SAVE_FACT_QUERY = """INSERT INTO facts (factId, fact, username, likes)
        VALUES (?, ?, ?, ?)
        """
    GET_FACTS_QUERY = """SELECT factId, fact, username, 
        likes, posted_on, fileN FROM facts INNER JOIN
        users USING(username) ORDER BY posted_on DESC
        """
    LIKE_FACT_QUERY = """UPDATE facts SET likes=likes + 1 WHERE factId=?"""
    UNLIKE_FACT_QUERY = """UPDATE facts SET likes=likes - 1 
        WHERE factId=? AND likes >= 1
        """
    GET_LIKES = """SELECT likes FROM facts WHERE factId=?"""
    
    CREATE_HISTORY_TABLE = """CREATE TABLE IF NOT EXISTS history (
        id INTEGER NOT NULL PRIMARY KEY,
        factId VARCHAR NOT NULL,
        username VARCHAR NOT NULL,
        liked_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        toggle INTEGER NOT NULL,
        FOREIGN KEY(factId) REFERENCES facts(factId),
        FOREIGN KEY(username) REFERENCES users(username))
        """
    CHECK_HISTORY_QUERY = """SELECT toggle FROM history WHERE factId=? AND username=?"""
    ADD_HISTORY_QUERY = """INSERT INTO history(factId, username, toggle) VALUES (?, ?, ?)"""
    TOGGLE_HISTORY_QUERY = """UPDATE history SET toggle=? WHERE factId=? AND username=?"""
