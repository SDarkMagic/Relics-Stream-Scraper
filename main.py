import Lib.API as api
import Lib.util as util
import json
import ftplib
import os
import threading
import queue
import time
import asyncio


oauthToken = None
botwGameId = 110758

def checkStreams(pagination=None, maxLength=50, resultList=None):
    if resultList != None:
        pass
    else:
        resultList = []
    print('maxLength ', maxLength)
    streams = api.getStreams(oauthToken, botwGameId, maxLen=maxLength, pagination=pagination)
    resultList.extend(streams['data'])
    if len(streams['data']) == maxLength or len(streams['data']) == maxLength:
        #print('if')
        resultList.extend(checkStreams(pagination=streams['pagination']['cursor'], maxLength=maxLength, resultList=resultList))
    else:
        #print('else')
        pass
    print('finished checkStreams')
    return(resultList)

def uploadFile(file, fileName, destHost):
    user = os.getenv('FTP_USERNAME')
    password = os.getenv('FTP_PASSWORD')
    ftp = ftplib.FTP(destHost)
    ftp.login(user=user, passwd=password)
    ftp.storbinary(f'STOR {fileName}', open(file, 'rb'))
    print(f'{fileName} uploaded successfully!')
    try:
        ftp.quit()
        print('FTP connection quit')
    except:
        ftp.close()
        print('FTP function Closed')
    return

def main(queue):
    global oauthToken
    maxLength = 100
    queueData = None
    sleepDelay = 30
    sleptTime = 0
    print('started main')
    while True:
        if queueData != None:
            if (queueData[1] - sleptTime <= sleepDelay):
                time.sleep((queueData[1] - sleptTime) + 1)
                queueData = queue.get()
            else:
                pass
        else:
            queueData = queue.get()
        # print(f'QueueData: {queueData}')
        oauthToken = queueData[0]
        relicsStreams = []
        try:
          streams = checkStreams(maxLength=maxLength)
        except:
          time.sleep(60)
          continue
        #print(f'streams length {len(streams)}')
        for stream in streams:
            if isinstance(stream, dict):
                title = stream['title'].lower().split(' ')
                for word in title:
                    wordIdx = title.index(word)
                    title[wordIdx] = util.puncStrip(word)
                if 'relics' in title and stream['type'] == 'live':
                    #print(title)
                    relicsStreams.append(stream)
                else:
                    continue
            else:
                continue
        with open('response.json', 'wt') as writeData:
            status = streams
            # print(len(status))
            writeData.write(json.dumps(relicsStreams, indent=2))
        print(len(relicsStreams))
        uploadFile('response.json', 'LiveStreams.json', "ftp.relicsofthepast.dev")
        relicsStreams.clear()
        time.sleep(sleepDelay)
        sleptTime += sleepDelay

def refreshOauth(queue):
    while True:
        print('called Oauth refresh')
        oauthToken, regenTimer = util.genAccessToken()
        queue.put([oauthToken, regenTimer])
        print(regenTimer)
        sleptTime = 0
        while sleptTime < regenTimer:
            time.sleep(5)
            sleptTime += 5

dataQueue = queue.Queue()

refreshThread = threading.Thread(target=refreshOauth, args=(dataQueue, ))
mainThread = threading.Thread(target=main, args=(dataQueue, ))

if __name__ == '__main__':
    refreshThread.start()
    mainThread.start()
    #dataQueue.put('kill')