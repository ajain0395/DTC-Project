import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import geopandas as gpd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
mapbox_access_token = 'pk.eyJ1IjoiYWphaW4wMzk1IiwiYSI6ImNqeDczMWNkczAwcngzeHAzaDc2aGptaHIifQ.PrZuFAsV8w5ghhUhe8AF3w'

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')
#xd = pd.read_csv("./")


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

#app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            ############################################################################
            'data' : [
                    go.Scattermapbox(
                            lat=['38.91427','38.91538','38.91458',
                                 '38.92239','38.93222','38.90842',
                                 '38.91931','38.93260','38.91368',
                                 '38.88516','38.921894','38.93206',
                                 '38.91275'],
                            lon=['-77.02827','-77.02013','-77.03155',
                                 '-77.04227','-77.02854','-77.02419',
                                 '-77.02518','-77.03304','-77.04509',
                                 '-76.99656','-77.042438','-77.02821',
                                 '-77.01239'],
                            mode='markers',
                            marker=go.scattermapbox.Marker(size=9),
                            text=["The coffee bar","Bistro Bohem","Black Cat",
                                  "Snap","Columbia Heights Coffee","Azi's Cafe",
                                  "Blind Dog Cafe","Le Caprice","Filter",
                                  "Peregrine","Tryst","The Coupe",
                                  "Big Bear Cafe"])],
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
                        lat=38.92,
                        lon=-77.07
                    ),
                    pitch=0,
                    zoom=10
                ),
            )
            #############################################################################
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)