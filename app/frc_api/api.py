import requests

from flask import current_app

API_KEY = current_app.config.get("", None)

def make_request(headers):
    pass