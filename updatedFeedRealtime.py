import psycopg2
# from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import *
import pandas as pd
#import geopandas as gpd
from sqlalchemy import *
from geoalchemy2 import Geometry
#Necessary header files
from google.transit import gtfs_realtime_pb2
from threading import Thread
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import MessageToJson
import requests
import json
import pandas as pd
from collections import OrderedDict
import datetime
import time


sleepTime = 7	      #Time to wait for next iteration
fileName = 'dummy.csv'             #Name of the filename to save as csv
key='6uwbqTNiek5jYJKFAev0DZgH5LdeqXAR'          #Key fortransit website
apiurl = 'https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key='

def insert_to_buses(X):
    try:
        connection = psycopg2.connect(host='localhost', dbname='dtcdb',   user='dtc', password='dtc')
        connection.autocommit=False
        sql = "INSERT INTO stops_buses (vehicle_id, trip_id, route_id, latitude, longitude, speed,timestamp, geometry)         VALUES (%s,%s,%s,%s,%s,%s,to_timestamp(%s,'yyyy-mm-dd hh24:mi:ss'), ST_SetSRID(ST_MakePoint(%s, %s), 4326))"
        with connection.cursor() as cur:
            cur.execute(sql, ((X['vehicle_id']),
                              (X['trip_id']),
                              (X['route_id']),
                              (X['latitude']),
                              (X['longitude']),
                              (X['speed']),
                              (str(datetime.datetime.fromtimestamp(int(X['timestamp'])))),
                              (X['longitude']),
                              (X['latitude']),                         
                             ))
        connection.commit()
        # print("Transaction completed successfully ")
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error in transction Reverting all other operations of a transction ", error)
        connection.rollback()
    finally:
        #closing database connection.
        if(connection):
            connection.close()
            # print("PostgreSQL connection is closed")

def entityCheck(feed):
    if(feed.entity):
        return True
    return False

def getResponse():
    response = ''
    while True:
        try:
            response = requests.get(apiurl+key)
            if(response.ok):
                return response
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            # time.sleep(2)
            print("Was a nice sleep, now let me continue...")
            continue
    return response

def getFeed():
    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        response=getResponse()
        feed.ParseFromString(response.content)
        return feed
    except:
        return getFeed()


def threadFunc(arr):
     counter=0
     for block in arr:
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
        #t1=time.time()
        insert_to_buses(row)    



def getDataFrame(dict_obj):
    div = len(dict_obj['entity'])//4
    print("Number of Entries ",len(dict_obj['entity']))
    i=1
    arr1 = [dict_obj['entity'][i] for i in range(0,i*div)];  i+=1
    arr2 = [dict_obj['entity'][i] for i in range((i-1)*div,i*div)]; i+=1
    arr3 = [dict_obj['entity'][i] for i in range((i-1)*div,i*div)]; i+=1
    arr4 = [dict_obj['entity'][i] for i in range((i-1)*div,len(dict_obj['entity']))]; 
    
    t1 = Thread(target=threadFunc, args=(arr1,)) 
    t2 = Thread(target=threadFunc, args=(arr2,)) 
    t3 = Thread(target=threadFunc, args=(arr3,)) 
    t4 = Thread(target=threadFunc, args=(arr4,))
    t1.start();t2.start();t3.start();t4.start();
    t1.join();t2.join();t3.join();t4.join(); 

def getFrame():
    entityFlag=False
    while entityFlag!=True:
        feed=getFeed()
        entityFlag=entityCheck(feed)
        print("Entity Present : ",entityFlag)

    dict_obj = MessageToDict(feed)
    frame=getDataFrame(dict_obj)
    # frame['humantime'] = frame.apply( lambda row: datetime.datetime.fromtimestamp(int(row['timestamp'])),axis=1 )
    # feedtime = int(dict_obj['header']['timestamp'])
    # frame['feed time'] = datetime.datetime.fromtimestamp(feedtime)
    return frame

def main():
    iteration=0
    while(True):
        t1=time.time()
        newFrame=getFrame()
        iteration+=1
        #print("Iter : {0}, Shape : {1}".format(iteration,newFrame.shape))
        t2=time.time()
        totalTime =  t2-t1
        print(totalTime)
        if(totalTime<10):
            time.sleep((10-totalTime)-1)
    
if __name__=="__main__":
   main()