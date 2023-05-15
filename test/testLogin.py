#!/usr/bin/python3

"""
https://wingxel.github.io/website
-----------------------------------
Test login
"""

import requests
from bs4 import BeautifulSoup


headers = {
	"User-Agent": "Mozilla/200",
}

sessionv = requests.Session()
index = sessionv.get("http://localhost:8000/login-pg")

# Get the csrf_token
soup = BeautifulSoup(index.text, "html.parser")
token =  soup.find("input", {"name": "csrf_token"})["value"]

payload = {
	"uName": "testacc",
	"pwd": "Random1#",
    "csrf_token": token
}

resp = sessionv.post("http://localhost:8000/login", headers=headers, data=payload, timeout=3)
print(resp.text)
