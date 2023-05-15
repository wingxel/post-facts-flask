#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
SQL Queries for each action
"""

class Queries:
    # SQL query to create users table if one does not exist
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
    # SQL query to create insert a user into the users table
    INSERT_USER_QUERY = """ INSERT INTO users (firstName, lastName, username, email, fileN, pswd)
        VALUES (?, ?, ?, ?, ?, ?)
        """
    # SQL query to check if an email is already registered
    CHECK_EMAIL_USER_QUERY = """SELECT email FROM users WHERE email=?"""
    # SQL query to check if an username is already registered
    CHECK_USER_USERNAME_QUERY = """SELECT username FROM users WHERE username=?"""
    # SQL query to get user info when login
    LOGIN_QUERY = """SELECT firstName, lastName, username, email, fileN, pswd FROM users WHERE username=?"""
    
    # SQL query to create facts table if one does not exist
    CREATE_FACTS_TABLE = """CREATE TABLE IF NOT EXISTS facts (
        id INTEGER NOT NULL PRIMARY KEY,
        factId VARCHAR NOT NULL UNIQUE,
        fact VARCHAR NOT NULL,
        username VARCHAR NOT NULL,
        likes INTEGER NOT NULL,
        posted_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(username) REFERENCES users(username))
        """
    # SQL query to insert a fact into the facts table
    SAVE_FACT_QUERY = """INSERT INTO facts (factId, fact, username, likes)
        VALUES (?, ?, ?, ?)
        """
    # SQL query to get facts and associated information (who posted the fact - 
    # profile image)
    GET_FACTS_QUERY = """SELECT factId, fact, username, 
        likes, posted_on, fileN FROM facts INNER JOIN
        users USING(username) ORDER BY posted_on DESC
        """
    # SQL query to mark given fact as liked by given user
    LIKE_FACT_QUERY = """UPDATE facts SET likes=likes + 1 WHERE factId=?"""
    # SQL query to remove like from given fact for given user
    UNLIKE_FACT_QUERY = """UPDATE facts SET likes=likes - 1 
        WHERE factId=? AND likes >= 1
        """
    # SQL query to get all the likes for a given fact
    GET_LIKES = """SELECT likes FROM facts WHERE factId=?"""
    
    # SQL query to create history table if one does not exist
    CREATE_HISTORY_TABLE = """CREATE TABLE IF NOT EXISTS history (
        id INTEGER NOT NULL PRIMARY KEY,
        factId VARCHAR NOT NULL,
        username VARCHAR NOT NULL,
        liked_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        toggle INTEGER NOT NULL,
        FOREIGN KEY(factId) REFERENCES facts(factId),
        FOREIGN KEY(username) REFERENCES users(username))
        """
    # SQL query to like history for a given fact and username
    CHECK_HISTORY_QUERY = """SELECT toggle FROM history WHERE factId=? AND username=?"""
    # SQL query to add history for given fact and username
    ADD_HISTORY_QUERY = """INSERT INTO history(factId, username, toggle) VALUES (?, ?, ?)"""
    # SQL query to update like for a given fact and username accordingly
    TOGGLE_HISTORY_QUERY = """UPDATE history SET toggle=? WHERE factId=? AND username=?"""
