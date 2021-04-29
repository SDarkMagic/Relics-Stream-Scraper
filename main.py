import Lib.API as api
import json
import ftplib

botwGameId = 110758

def checkStreams(pagination=None, maxLength=50, resultList=[]):
    print('maxLength ', maxLength)
    streams = api.getStreams(botwGameId, maxLen=maxLength, pagination=pagination)
    resultList.extend(streams['data'])
    if len(streams['data']) == maxLength or len(streams['data']) == maxLength:
        print('if')
        resultList.extend(checkStreams(pagination=streams['pagination']['cursor'], maxLength=maxLength, resultList=resultList))
    else:
        print('else')
        pass
    return(resultList)

def uploadFile(file, fileName, destHost):
    user = os.getenv('FTP_USERNAME')
    password = os.getenv('FTP_PASSWORD')
    ftp = ftplib.FTP(destHost)
    ftp.login(user=user, passwd=password)
    ftp.storbinary(f'STOR {fileName}', open(file, 'rb'))
    try:
        ftp.quit()
    except:
        ftp.close()

def main():
    streamList = []
    maxLength = 100

    streamList.append(initialStreams['data'])
    if len(initialStreams['data'] == maxLength):
        pass

with open('response.json', 'wt') as writeData:
    status = checkStreams(maxLength=100)
    print(len(status))
    writeData.write(json.dumps(status, indent=2))