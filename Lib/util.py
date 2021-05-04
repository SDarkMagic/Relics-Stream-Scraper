import os
import sys
import requests

def genAccessToken():
    OAUTH_REQUEST_ENDPOINT = 'https://id.twitch.tv/oauth2/token'
    REQUEST_HEADERS = {
        'client_id' : os.getenv('CLIENT_ID'),
        'client_secret' : os.getenv('CLIENT_SECRET'),
        'grant_type' : 'client_credentials'
    }
    oauth = requests.post(url=OAUTH_REQUEST_ENDPOINT, params=REQUEST_HEADERS)
    oauthData = oauth.json()
    return(oauthData['access_token'], oauthData['expires_in'])