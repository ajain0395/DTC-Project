import psycopg2
from typing import Iterator, Optional,Any,Dict

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
from django.contrib.gis.geos import Point, WKBWriter,WKBReader
import io


sleepTime = 7	      #Time to wait for next iteration
fileName = 'dummy.csv'             #Name of the filename to save as csv
key='6uwbqTNiek5jYJKFAev0DZgH5LdeqXAR'          #Key fortransit website
apiurl = 'https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key='

class StringIteratorIO(io.TextIOBase):

    def __init__(self, iter: Iterator[str]):
        self._iter = iter
        self._buff = ''

    def readable(self) -> bool:
        return True

    def _read1(self, n: Optional[int] = None) -> str:
        while not self._buff:
            try:
                self._buff = next(self._iter)
            except StopIteration:
                break
        ret = self._buff[:n]
        self._buff = self._buff[len(ret):]
        return ret

    def read(self, n: Optional[int] = None) -> str:
        line = []
        if n is None or n < 0:
            while True:
                m = self._read1()
                if not m:
                    break
                line.append(m)
        else:
            while n > 0:
                m = self._read1(n)
                if not m:
                    break
                n -= len(m)
                line.append(m)
        return ''.join(line)

def clean_csv_value(value: Optional[Any]) -> str:
    if value is None:
        return r'\N'
    return str(value).replace('\n', '\\n')

def create_staging_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS staging_buses;
        CREATE UNLOGGED TABLE staging_buses (
        
        trip_id character varying(100) NOT NULL,
        route_id integer NOT NULL,
        geometry public.geometry(Point,4326) NOT NULL,
        latitude double precision NOT NULL,
        longitude double precision NOT NULL,
        speed double precision NOT NULL,
        vehicle_id character varying(100) NOT NULL,
        "timestamp" timestamp with time zone NOT NULL
        );
    """)

def insert_to_buses( alldata: Iterator[Dict[str, Any]],connection, size: int = 8192) -> None:
    try:
        with connection.cursor() as cursor:
            create_staging_table(cursor)

            buses_string_iterator = StringIteratorIO((
                '|'.join(map(clean_csv_value, (
                    row['vehicle_id'],
                    row['trip_id'],
                    row['route_id'],
                    row['latitude'],
                    row['longitude'],
                    row['geometry'],
                    row['speed'],
                    row['congestion'],
                    row['timestamp']
                ))) + '\n'
                for row in alldata
            ))
            cursor.copy_from(buses_string_iterator, 'stops_buses', sep='|', size=size,columns=('vehicle_id','trip_id','route_id','latitude','longitude','geometry','speed','congestion','timestamp'))
    except(Exception):
        print (str(Exception))
        return False
    return True

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
def getcongestion(block):
    return 1

def threadFunc(arr,connection):
    #  wkb_w = WKBWriter()
     counter=0
     alldata = []
     for block in arr['entity']:
        counter += 1
        row = {}
        row['vehicle_id'] = block['id']
        row['trip_id'] = block['vehicle']['trip'].get('tripId','')
        row['route_id'] = block['vehicle']['trip'].get('routeId','')
        row['latitude'] = block['vehicle']['position'].get('latitude','')
        row['longitude'] = block['vehicle']['position'].get('longitude','')
        row['speed'] = block['vehicle']['position'].get('speed','')
        row['timestamp'] = str(datetime.datetime.fromtimestamp(int(block['vehicle'].get('timestamp',''))))
 #       row['trip_start_time'] = str(datetime.datetime.fromtimestamp(int(block['vehicle'].get('timestamp',''))))
        row['geometry'] = Point( block['vehicle']['position'].get('longitude',''),block['vehicle']['position'].get('latitude',''),srid=4326)
        row['congestion'] = getcongestion(block)
        #row['vehicle_id'] = block['vehicle']['vehicle'].get('id','')
        #row['label'] = block['vehicle']['vehicle'].get('label','')
        #t1=time.time()
        alldata.append(row)
     writing_success = insert_to_buses(iter(alldata),connection)
     print ("Entries written ",len(alldata),"Success: ", writing_success)



# def getDataFrame(dict_obj,connection):
#     #collector = []
#     counter=0
#     for block in dict_obj['entity']:
#         counter += 1
#         row = {}
#         #OrderedDict()
#         row['vehicle_id'] = block['id']
#         row['trip_id'] = block['vehicle']['trip'].get('tripId','')
#         row['route_id'] = block['vehicle']['trip'].get('routeId','')
#         row['latitude'] = block['vehicle']['position'].get('latitude','')
#         row['longitude'] = block['vehicle']['position'].get('longitude','')
#         row['speed'] = block['vehicle']['position'].get('speed','')
#         row['timestamp'] = block['vehicle'].get('timestamp','')
#         #row['vehicle_id'] = block['vehicle']['vehicle'].get('id','')
#         #row['label'] = block['vehicle']['vehicle'].get('label','')
#         insert_to_buses(row,connection)
#         #collector.append(row)
#     #df = pd.DataFrame(collector)
#     #return df

def getFrame(connection):
    temp1 = time.time()
    entityFlag=False
    while entityFlag!=True:
        feed=getFeed()
        entityFlag=entityCheck(feed)
        print("Entity Present : ",entityFlag)

    dict_obj = MessageToDict(feed)
    temp2 = time.time()
    print ("Data Fetching Time ",(temp2-temp1))
    print ("Writing to DB...")
    temp1 = time.time()
    #frame=getDataFrame(dict_obj,connection)
    frame=threadFunc(dict_obj,connection)
    temp2=time.time()
    totalTime =  temp2-temp1
    print("DB Time ",totalTime)
    print ("Writing to DB completed...")
    # frame['humantime'] = frame.apply( lambda row: datetime.datetime.fromtimestamp(int(row['timestamp'])),axis=1 )
    # feedtime = int(dict_obj['header']['timestamp'])
    # frame['feed time'] = datetime.datetime.fromtimestamp(feedtime)
    return frame

#def main():
    
if __name__=="__main__":
    iteration=0
    while(True):
        while(True):
            try:
                mainconnection = psycopg2.connect(host='192.168.18.221', dbname='dtcdb',   user='dtc', password='dtc')
                mainconnection.autocommit = False
                break
            except:
                print ("Connection Error")
                pass
        t1=time.time()
        newFrame=getFrame(mainconnection)
        mainconnection.commit()
        iteration+=1
        #print("Iter : {0}, Shape : {1}".format(iteration,newFrame.shape))
        t2=time.time()
        totalTime =  t2-t1
        print("Total Time ",totalTime)
        if(totalTime<9):
            time.sleep(9 - totalTime)
   #main()
