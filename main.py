import Lib.API as api
import json
import asyncio

botwGameId = 110758
async def checkStreams(pagination=None, maxLength=50, resultList=[]):
    print('maxLength ', maxLength)
    streams = api.getStreams(botwGameId, maxLen=maxLength, pagination=pagination)
    resultList.extend(streams['data'])
    if len(streams['data']) == maxLength or len(streams['data']) == maxLength:
        print('if')
        resultList.extend(await checkStreams(pagination=streams['pagination']['cursor'], maxLength=maxLength, resultList=resultList))
    else:
        print('else')
        pass
    return(resultList)

async def main():
    maxLength = 100
    relicsStreams = []
    streams = await checkStreams(maxLength=maxLength)
    
    for stream in streams:
      if isinstance(stream, dict):
        title = stream['title'].lower().split(' ')
        #print(' '.join(title))
        if 'relics' in title and stream['type'] == 'live':
          print(title)
          relicsStreams.append(stream)


    with open('response.json', 'wt') as writeData:
      status = streams
      print(len(status))
      writeData.write(json.dumps(relicsStreams, indent=2))
      
asyncio.run(main())