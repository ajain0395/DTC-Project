#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 15:44:34 2019

@author: ashish
"""

import datetime
import time
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import MapParseFinal as mapparse
stream_id = "xjqhj2b04z"

s = py.Stream(stream_id)

# We then open a connection
s.open()
i = 0    # a counter
k = 5    # some shape parameter

# Delay start of stream by 5 sec (time to switch tabs)
#time.sleep(5)

while True:
    # Current time on x-axis, random numbers on y-axis
    df = mapparse.getFrame()
    lat = df.latitude.tolist()
    lon = df.longitude.tolist()
    text = df.vehicle_id.tolist()
    # Send data to your plot
    s.write(dict(lat=lat[0],lon=lon[0],text=text[0]))

    #     Write numbers to stream to append current data on plot,
    #     write lists to overwrite existing data on plot

    #time.sleep(5)  # plot a point every second    
# Close the stream when done plotting
s.close()
