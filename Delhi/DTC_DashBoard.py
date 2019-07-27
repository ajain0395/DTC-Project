#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 11:30:57 2019

@author: ashish
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.tools as tls
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
#import geopandas as gpd
import os
import time

#import MapParseFinal as map
import MapParseFinal as mapparser

flag = True
#import threading
lata = []
longa = []
bus_name = []


#class Thread_A(threading.Thread):
#    def __init__(self, name):
#        threading.Thread.__init__(self)
#        self.name = name
#
#    def run(self):
#        global lata
#        global longa
#        global bus_name
#       
#        df = mapparser.getFrame()
#        lata = df.latitude.tolist()
#        longa = df.longitude.tolist()
#        bus_name = df.vehicle_id.tolist()
#
#class Thread_B(threading.Thread):
#    def __init__(self, name):
#        threading.Thread.__init__(self)
#        self.name = name
#
#    def run(self):
#        global app
#        app.run_server(debug=True,port=8078)


#import plotly 
#plotly.tools.set_credentials_file(username='ajain0395', api_key='JXb0W7CDDS7rbdFOP0c4')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
mapbox_access_token = 'pk.eyJ1IjoiYWphaW4wMzk1IiwiYSI6ImNqeDczMWNkczAwcngzeHAzaDc2aGptaHIifQ.PrZuFAsV8w5ghhUhe8AF3w'


stream_ids = tls.get_credentials_file()['stream_ids']

stream_id = stream_ids[0]
df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')
stops = pd.read_csv("./stops.csv")                      
#      stream = stream_bus,

stream_bus = go.Stream(
    token=stream_id,  # link stream id to 'token' key
    maxpoints=500      # keep a max of 80 pts on screen
)
livelocation = go.Scattermapbox(
                            lat=[],
                            lon=[],
                            stream = stream_bus,
                            mode='markers',
                            marker=go.scattermapbox.Marker(size=9),
                            text=[])

stops.stop_lat = stops.stop_lat.astype(float)
stops.stop_lon = stops.stop_lon.astype(float)
app.layout = html.Div(children=[
    html.H1(children='DTC Project'),

    html.Div(children='''
        Displaying Stops and live bus location
    '''),
    dcc.Graph(
        id='dtc_stops',
        figure={
            ########################livelocation####################################################
            'data' : [
                    go.Scattermapbox(
                            lat=stops.stop_lat.tolist(),
                            lon=stops.stop_lon.tolist(),
                            mode='markers',
                            marker=go.scattermapbox.Marker(size=9),
                            text=stops.stop_name.tolist()),
                            go.Scattermapbox(
                            lat=lata,
                            lon=longa,
#                            stream = stream_bus,
                            mode='markers',
                            marker=go.scattermapbox.Marker(size=9),
                            text=bus_name)
                            ,
                            livelocation,
                            ],
            ############################################################################
#            'data': [
#                go.Scatter(
#                    x=df[df['continent'] == i]['gdp per capita'],
#                    y=df[df['continent'] == i]['life expectancy'],
#                    text=df[df['continent'] == i]['country'],
#                    mode='markers',
#                    opacity=0.7,
#                    marker={
#                        'size': 15,
#                        'line': {'width': 0.5, 'color': 'white'}
#                    },
#                    name=i
#                ) for i in df.continent.unique()
#            ],
            ############################################################################
#            'layout': go.Layout(
#                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
#                yaxis={'title': 'Life Expectancy'},
#                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#                legend={'x': 0, 'y': 1},
#                hovermode='closest'
#            )
            #############################################################################
            'layout' : go.Layout(
                autosize=True,
                hovermode='closest',
                mapbox=go.layout.Mapbox(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=go.layout.mapbox.Center(
                        lat=28.6304,
                        lon=77.2177
                    ),
                    pitch=2,
                    zoom=12
                ),
            )
            #############################################################################
        }
    )
],style={'width': '100%','height':'200%'})



from threading import Thread
def thread1(threadname):
    global lata
    global longa
    global bus_name
    global app
    global livelocation
    while(flag):
        df = mapparser.getFrame()
        lata.extend( df.latitude.tolist())
        longa.extend(df.longitude.tolist())
        bus_name.extend(df.vehicle_id.tolist())
        time.sleep(10)
        livelocation.lat = df.latitude.tolist()
        livelocation.lon = df.longitude.tolist()
        app.callback()


if __name__ == '__main__':
#    b = Thread_B("appserver")
#    b.start()
    
#    count  = 20
#    while(count > 0):
#        a = Thread_A("myThread_name_A")
#        a.start()
#        a.join()
#        count-=1
#    b.join()
    threadx = Thread( target=thread1, args=("Thread-1", ) )
    threadx.start()
    app.run_server(debug=True,port=8078)
    flag = False
    threadx.join()