#Necessary header files
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import MessageToJson
import requests
import json
import pandas as pd
from collections import OrderedDict
import datetime
import time

sleepTime = 1	      #Time to wait for next iteration
fileName = 'dummy.csv'             #Name of the filename to save as csv
key='noeXTjzoym4GbxYjEXWdYM8Z0ij7lOYq'          #Key fortransit website

def entityCheck(feed):
    if(feed.entity):
        return True
    return False

def getResponse():
    response = ''
    while response == '':
        try:
            response = requests.get('https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key='+key)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    return response

def getFeed():
    feed = gtfs_realtime_pb2.FeedMessage()
    response=getResponse()
    feed.ParseFromString(response.content)
    return feed

def getDataFrame(dict_obj):
    collector = []
    counter=0
    for block in dict_obj['entity']:
        counter += 1
        row = OrderedDict()
        row['vehicle_id'] = block['id']
        row['trip_id'] = block['vehicle']['trip'].get('tripId','')
        row['route_id'] = block['vehicle']['trip'].get('routeId','')
        row['latitude'] = block['vehicle']['position'].get('latitude','')
        row['longitude'] = block['vehicle']['position'].get('longitude','')
        row['speed'] = block['vehicle']['position'].get('speed','')
        row['timestamp'] = block['vehicle'].get('timestamp','')
        #row['vehicle_id'] = block['vehicle']['vehicle'].get('id','')
        #row['label'] = block['vehicle']['vehicle'].get('label','')
        collector.append(row)
    df = pd.DataFrame(collector)
    return df

def getFrame():
    entityFlag=False
    while entityFlag!=True:
        feed=getFeed()
        entityFlag=entityCheck(feed)
        print("Entity Present : ",entityFlag)

    dict_obj = MessageToDict(feed)
    frame=getDataFrame(dict_obj)
    frame['humantime'] = frame.apply( lambda row: datetime.datetime.fromtimestamp(int(row['timestamp'])),axis=1 )
    feedtime = int(dict_obj['header']['timestamp'])
    frame['feed time'] = datetime.datetime.fromtimestamp(feedtime)
    return frame

def main():
    iteration=0
    frame=getFrame()
    with open(fileName,'w') as f:
        frame.to_csv(f, index=False)
    print("Iter : {0}, Shape : {1}".format(iteration,frame.shape))
    while(True):
        time.sleep(sleepTime)
        newFrame=getFrame()
        with open(fileName,'a') as f:
             newFrame.to_csv(f,index=False,header=False)
        iteration+=1
        print("Iter : {0}, Shape : {1}".format(iteration,newFrame.shape))
    
if __name__=="__main__":
    main()
