import requests
import os
import json
import util


def getStreams(gameId, maxLen=50, pagination=None):
    token, regenTimer = util.regenAccessToken()
    API_HEADERS = {
    'Client-ID' : os.getenv('CLIENT_ID'),
    'Authorization' : f'Bearer {token}'
    }
    if pagination != None:
            status = requests.get(f'https://api.twitch.tv/helix/streams?game_id={gameId}&first={maxLen}&after={pagination}', headers=API_HEADERS)
    else:
        status = requests.get(f'https://api.twitch.tv/helix/streams?game_id={gameId}&first={maxLen}', headers=API_HEADERS)
    return(status.json())

getStreams(botwGameId)