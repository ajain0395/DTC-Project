#####################################################################################################################

##This Program is used to create a Grid object of desired size and storing latitude and longitude in it accoordingly

#####################################################################################################################
import csv
import pandas as pd
import math
from math import sin, cos, sqrt, atan2, radians
import numpy as np 
import pickle
import time

class locat:
    def __init__(self,lat,long):
        self.lat = lat
        self.long = long
    def getLatitude(self):
        return self.lat
    def getLongitude(self):
        return self.long
    def getPrint(self):
        print("Latitde:",self.getLatitude(),", Longitude:",self.getLongitude())

class cell:
    def __init__(self,cell_id):
        self.cell_id = cell_id 
        self.posting = {}
        self.busEntries = {}
        self.averageSpeeds={}
    
class GridMaker:
    def __init__(self,min_latitude,min_longitude,max_latitude,max_longitude,split):
        self.min_lat = min_latitude
        self.min_long = min_longitude
        self.max_lat = max_latitude
        self.max_long = max_longitude
        self.split = split
        self.gridSize = split*split
        self.GRID = None
        
    def loadGrid(self,grid):
        self.GRID=grid
    
    def getMinBoundary(self):
        return [self.min_lat,self.min_long]
    
    def getMaxBoundary(self):
        return [self.max_lat,self.max_long]
    
    def updateSplit(self,new_split):
        self.split=new_split
    
    def getLatStepSize(self):
        diff = self.max_lat-self.min_lat
        return diff/self.split
    
    def getLongStepSize(self):
        diff = self.max_long-self.min_long
        return diff/self.split
    
    def hash(self,point):
        latStep = self.getLatStepSize()
        longStep= self.getLongStepSize()
        latDiff = point.getLatitude()-self.min_lat
        longDiff = point.getLongitude()-self.min_long
        row = math.floor(latDiff/latStep)
        col = math.floor(longDiff/longStep)
        cell_id = row*self.split + col
        return cell_id
    
    def getCordinatesOfCell(self,cell_id):
        latStep = self.getLatStepSize()
        longStep= self.getLongStepSize()
        col = cell_id%self.split
        row = (cell_id-col)/self.split
        latitude1 = self.min_lat+ row *latStep
        longitude1= self.min_long + col * longStep
        return latitude1,longitude1
    
    def getFourCordinatesOfCell(self,cell_id):
        lat,long = self.getCordinatesOfCell(cell_id)
        latStep = self.getLatStepSize()
        longStep= self.getLongStepSize()
        loc1 = locat(lat,long)
        loc2 = locat(lat+latStep,long)
        loc3 = locat(lat,long+longStep)
        loc4 = locat(lat+latStep,long+longStep)
        return [loc1,loc2,loc3,loc4]
    
    def validateLocation(self,loc):
        lat = loc.getLatitude()
        lon = loc.getLongitude()
        if (lat<self.min_lat or lat>self.max_lat) or (lon<self.min_long or lon>self.max_long):
            return False
        return True
        
    def getAddressOfCell(self,cell_id):
        pass
        #body of this fucntion is to return address
        
        
    def create_CSV(self,filename):
        data = {}
        data['cell_id']=[]
        data['latitude']=[]
        data['longitude']=[]
        for i in range(self.gridSize):
            data['cell_id'].append(i)
            lat,long = self.getCordinatesOfCell(i)
            data['latitude'].append(lat)
            data['longitude'].append(long)
        df = pd.DataFrame(data)
        df.to_csv(filename,index=False)
        print('data writed to :',filename)
        
    def createPostingList(self,file): #### with the use of csvreader
        cellList={}
        start = time.time()
        for i in range(self.gridSize):
            cellList[i]=cell(i)
        with open(file,'r') as csvFile:
            reader = csv.reader(csvFile)
            col = next(reader)
            #print(col)
            for row in reader:
                #print(row)
                #print(row[2],row[3])
                loc = locat(float(row[2]),float(row[3]))
                road_id = str(row[1])
                cell_id = self.hash(loc)
                if self.validateLocation(loc)==True:
                    if cellList[cell_id].posting.get(road_id)==None:
                        cellList[cell_id].posting[road_id]=[]
                    cellList[cell_id].posting[road_id].append(loc)
        self.GRID =cellList
        csvFile.close()
        end = time.time()
        print("Done with Postings in ",end-start)
        
    def createPostingListOld(self,file): ### With the use of dataframe reading
        print("creating Postings for Cells")
        dataFrame = pd.read_csv(file)
        cellList={}
        for i in range(self.gridSize):
            cellList[i]=cell(i)
        for i in range(len(dataFrame)):
            lat = dataFrame['Latitude'][i]
            long= dataFrame['Longitude'][i]
            road_id = dataFrame['Road_id'][i]
            loc = locat(lat,long)
            cell_id = self.hash(loc)
            if self.validateLocation(loc)==True:
                if cellList[cell_id].posting.get(road_id)==None:
                    cellList[cell_id].posting[road_id]=[]
                cellList[cell_id].posting[road_id].append(loc)
        self.GRID = cellList
        print("Done with Postings")
        
    def createPostingListForRoad(self,file):
        print("creating Postings for Cells")
        dataFrame = pd.read_csv(file)
        cellList={}
        for i in range(self.gridSize):
            cellList[i]=cell(i)
        for i in range(len(dataFrame)):
            lat = dataFrame['stop_lat'][i]
            long= dataFrame['stop_lon'][i]
            road_id = dataFrame['road_id'][i]
            loc = locat(lat,long)
            cell_id = self.hash(loc)
            if self.validateLocation(loc)==True:
                if cellList[cell_id].posting.get(road_id)==None:
                    cellList[cell_id].posting[road_id]=[]
                cellList[cell_id].posting[road_id].append(loc)
        self.GRID = cellList
        print("Done with Postings")
        
def createPickle(newGrid,size):
    with open("SharedMemory/gridWithPosting"+str(size)+".pickle", 'wb') as handle:
            pickle.dump(newGrid, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
    #sizes = [190,230,280,370]
    sizes =600#[600]
    t1 =time.time()
    #for size in sizes:
    newGrid=GridMaker(28.4011,76.8631,28.8783,77.4481,sizes)
    
    #    list1=newGrid.getFourCordinatesOfCell(21070)
    #    for coord in list1:
    #        print(coord.getLatitude())
    #        print(coord.getLongitude())
    #    list2=newGrid.getFourCordinatesOfCell(20615)
    #    for coord in list2:
    #        print(coord.getLatitude())
    #        print(coord.getLongitude())
    
#        newGrid.create_CSV("SharedMemory/grid_"+str(size)+".csv")
#        newGrid.createPostingList('GridReq/combinedRoadInfo.csv')
#        createPickle(newGrid,size)
    t2 =time.time()
    print("Process terminated in :: ",t2-t1)