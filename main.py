import Lib.API as api
import Lib.util as util
import json
import ftplib
import os
import threading
import queue
import time
#import sys
#import signal

oauthToken = None
botwGameId = 110758

"""
def killHandler(signal_received, frame):
    dataQueue.put('kill')
    refreshThread.join()
    mainThread.join()
    sys.exit(0)
"""
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
    except:
        ftp.close()

def main(queue):
    global oauthToken
    maxLength = 100
    print('started main')
    while True:
        queueData = queue.get()
        #print(queueData)
        oauthToken = queueData
        relicsStreams = []
        streams = checkStreams(maxLength=maxLength)
        #print(f'streams length {len(streams)}')
        for stream in streams:
            if isinstance(stream, dict):
                title = stream['title'].lower().split(' ')
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
        time.sleep(30)

def refreshOauth(queue):
    while True:
        print('called Oauth refresh')
        oauthToken, regenTimer = util.genAccessToken()
        queue.put(oauthToken)
        print(regenTimer)
        time.sleep(30)

dataQueue = queue.Queue()

refreshThread = threading.Thread(target=refreshOauth, args=(dataQueue, ))
mainThread = threading.Thread(target=main, args=(dataQueue, ))

if __name__ == '__main__':
    refreshThread.start()
    mainThread.start()
    #dataQueue.put('kill')