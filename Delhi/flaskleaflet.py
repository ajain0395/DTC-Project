#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 00:24:16 2019

@author: ashish
"""
import folium
import pandas as pd
stops = pd.read_csv("data/GTFS/stops.txt")

mapp = folium.Map(location=[28.613939, 77.209023],zoom_start=12)
delhi_edge='./data/delhi2.geojson'
tooltip = 'Click for more info'


folium.GeoJson(
    delhi_edge,
    name='geojson'
).add_to(mapp)

for x in range(len(stops)):
#    print(stops.iloc[x]['stop_lat'])
    folium.Marker([stops.iloc[x]['stop_lat'],stops.iloc[x]['stop_lon']],
           popup='<strong>'+stops.iloc[x]['stop_name']+'</strong>',
           tooltip='<strong>'+stops.iloc[x]['stop_name']+'</strong>',).add_to(mapp),
           
#folium.Marker([stops['stop_lat'][10],stops['stop_lon'][10]],
#           popup='<strong>'+stops['stop_name'][10]+'</strong>',
#           tooltip=tooltip,
#           icon=folium.Icon(icon='cloud')).add_to(mapp),
#text = 'your text here'

#iframe = folium.IFrame(text, width=700, height=450)
#popup = folium.Popup(iframe, max_width=3000)
#Text = folium.Marker(location=[28.613939, 77.209023], popup=popup,
#                     icon=folium.Icon(icon_color='green'))
#mapp.add_child(Text)
folium.LayerControl().add_to(mapp)

mapp.save("flaskleaflet.html")