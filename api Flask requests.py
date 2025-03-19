
from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# Spotify API credentials (replace with your actual values)
CLIENT_ID = "340ebe283d9f462489c995e108401871"
CLIENT_SECRET = "a84f4bc0ce67494c969e7a9b818ce574"
TOKEN_URL = "https://accounts.spotify.com/api/token"


def get_access_token():
    """Fetches a new access token from Spotify API"""
    auth_response = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        auth=(CLIENT_ID, CLIENT_SECRET),
    )

    if auth_response.status_code == 200:
        return auth_response.json().get("access_token")
    else:
        return None


@app.route("/new-releases", methods=["GET"])
def get_new_releases():
    """Fetches new releases from Spotify"""
    token = get_access_token()
    if not token:
        return jsonify({"error": "Failed to get access token"}), 500

    response = requests.get(
        "https://api.spotify.com/v1/browse/new-releases",
        headers={"Authorization": f"Bearer {token}"},
    )

    return jsonify(response.json())


if __name__ == "__main__":
    app.run(debug=True)

    
