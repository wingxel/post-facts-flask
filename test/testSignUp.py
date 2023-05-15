#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
Test signup
"""

import os
import sys
import requests
from sys import argv, exit
from bs4 import BeautifulSoup


if len(argv[1::]) == 0:
    exit("Usage: python textSignUp.py /path/to/profile/image")

absPath = sys.argv[1]

# Check if the provided profile image path is valid
if not os.path.exists(absPath):
    exit(f"Invalid profile image: {absPath}")

headers = {
	"User-Agent": "Mozilla/200",
}

sessionv = requests.Session()
index = sessionv.get("http://localhost:8000/sign-pg")

# Get the csrf_token since the form are protected
soup = BeautifulSoup(index.text, "html.parser")
token =  soup.find("input", {"name": "csrf_token"})["value"]

profile = {
	"profile": (absPath.split("/")[-1], open(absPath, "rb"))
}

# Test Info
payload = {
	"fName": "Test",
	"lName": "Acc",
	"uName": "testacc",
	"email": "test-run-@test.cim",
	"pwd": "Random1#",
    "csrf_token": token
}

resp = sessionv.post("http://localhost:8000/sign-up", headers=headers, data=payload, 
    files=profile, timeout=3)
print(resp.text)
