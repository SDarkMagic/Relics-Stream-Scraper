import requests
import os
import json
import Lib.util as util


def getStreams(oauth, gameId, maxLen=50, pagination=None):
    token = oauth
    API_HEADERS = {
    'Client-ID' : os.getenv('CLIENT_ID'),
    'Authorization' : f'Bearer {token}'
    }
    if pagination != None:
            status = requests.get(f'https://api.twitch.tv/helix/streams?game_id={gameId}&first={maxLen}&after={pagination}', headers=API_HEADERS)
    else:
        status = requests.get(f'https://api.twitch.tv/helix/streams?game_id={gameId}&first={maxLen}', headers=API_HEADERS)
    return(status.json())

#getStreams(110758)