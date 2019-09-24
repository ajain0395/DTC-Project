#!/usr/bin/env python
import psycopg2
# from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import *
import pandas as pd
from sqlalchemy import *
from geoalchemy2 import Geometry
def insert_to_buses(X):
    try:
        connection = psycopg2.connect(host='192.168.18.221', dbname='dtcdb',   user='dtc', password='dtc')
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
        print("Transaction completed successfully ")
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error in transction Reverting all other operations of a transction ", error)
        connection.rollback()
    finally:
        #closing database connection.
        if(connection):
            connection.close()
            print("PostgreSQL connection is closed")
def insert_to_stops(X):
    try:
        connection = psycopg2.connect(host='localhost', dbname='dtcdb',   user='dtc', password='dtc')
        connection.autocommit=False
        sql = "INSERT INTO stops_stops (stop_id, stop_name,stop_code,longitude, latitude, geometry)         VALUES (%s,%s,%s,%s,%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))"
        with connection.cursor() as cur:
            cur.execute(sql, ((X['stop_id']),
                              (X['stop_name']),
                              (X['stop_code']),
                              (X['longitude']),
                              (X['latitude']),
                              (X['longitude']),
                              (X['latitude']),                         
                             ))
        connection.commit()
#print("Transaction completed successfully ")
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error in transction Reverting all other operations of a transction ", error)
        connection.rollback()
    finally:
        #closing database connection.
        if(connection):
            connection.close()
#print("PostgreSQL connection is closed")


# In[ ]:


# gdf = pd.read_csv('./Delhi/data/DTC_dataset/demo.csv')
stops_data = pd.read_csv('./Delhi/data/newjsdata/stops_lat_lon.csv')


stops_dict = stops_data.T.to_dict()
print("Data Migration Running....")
for i in range(len(stops_data)):
    insert_to_stops(stops_dict[i])
print("Completed....")
