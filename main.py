import Lib.API as api

botwGameId = 110758

def checkStreams(pagination, maxLen):
    streams = api.getStreams(botwGameId, maxLen=maxLength, pagination=pagination)

def main():
    streamList = []
    maxLength = 100

    streamList.append(initialStreams['data'])
    if len(initialStreams['data'] == maxLength):