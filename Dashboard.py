import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.io as pio
from selenium import webdriver
from selenium import webdriver
import time

con = sqlite3.connect('cosmos23-testdata.db', check_same_thread=False) #create the SQLite connection with the database file
#cur = con.cursor() #create the local cursor for the connection

#SQL code to access columns from the db file
sql = '''
SELECT water.id, timestamp, science.name AS Bouy, lat, lon, tds, temperature, ph, do, orp, depth
FROM water
LEFT JOIN science
ON water.science_id = science.id
ORDER BY water.id DESC;
'''


#use the connection with the database to read the SQL code and create a dataframe in the format the SQL code describes
df_1 = pd.read_sql(sql, con)
#print(df_1.head()) debugging code

fig = px.scatter_mapbox(
    df_1, 
    lat="lat", 
    lon="lon", 
    hover_data=["id", "ph", "temperature", "tds", "do", "orp"], 
    height=470, 
    color="Bouy", 
    mapbox_style="open-street-map"  # use open-street-map style
)

fig.update_layout(
    autosize=True,
    hovermode='closest',
    showlegend=True,
    mapbox=dict(
        accesstoken=None,  # no token is needed for open-street-map
        bearing=0,
        center=dict(
            lat=32.916558,
            lon=-117.097651
        ),
        pitch=0,
        zoom=14,
        style='open-street-map'  # this can also be set in the mapbox dict
    ),
)






app = Dash(__name__)

#layout of dashboard
app.layout = html.Div([

    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),  # 1 second interval
    html.Div(id='live-update-text'),
    html.H1("COSMOS Cluster 7: Hacking for Ocean Dashboard", style={'text-align': 'center', 'color': '#46A9FC'}),
    html.Div(style={'display': 'flex','flex-direction': 'row', 'align-items': 'center' },children=[
    html.Div(style={'display': 'grid', 	'grid-template-rows': '250px 230px',
	'grid-template-columns': '250px 250px 250px', 'width':'50vw'}, children=[
    
        #ph graph
        dcc.Graph(
            id="phgraph", style={ 'width': '100%'},
            figure={
                "data": [
                    {
                        "x": df_1["timestamp"], #x-axis is timestamp
                        "y": df_1["ph"], #y-axis is ph
                        "name" : "pH",
                        "type": "line",
                        "marker": {"color": "#f3f57f"}, #color of graph
                    },
                ],
                "layout": {
                    "showlegend": True,

                    "xaxis": {
                        "automargin": True,
                        "title": {"text": "Timestamp"}
                    },
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": "pH"}
                        },
                    "height": 300,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            }
        ),
        #depth graph
        dcc.Graph(
            id="depthgraph", style={'display': 'inline-block', 'width': '100%'},
            figure={
                "data": [
                    {
                        "x": df_1["timestamp"], #x-axis is timestamp
                        "y": df_1["depth"], #y-axis is ph
                        "name" : "depth",
                        "type": "line",
                        "marker": {"color": "#29CF8D"}, #color of graph
                    },
                ],
                "layout": {
                    "showlegend": True,

                    "xaxis": {
                        "automargin": True,
                        "title": {"text": "Timestamp"}
                    },
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": "depth"}
                        },
                    "height": 300,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            }
        ),

        #do graph
        dcc.Graph(
            id="dograph", style={'display': 'inline-block', 'width': '100%'},
            figure={
                "data": [
                    {
                        "x": df_1["timestamp"], #x-axis is timestamp
                        "y": df_1["do"], #y-axis is ph
                        "name" : "do",
                        "type": "line",
                        "marker": {"color": "#FC04E5"}, #color of graph
                    },
                ],
                "layout": {
                    "showlegend": True,

                    "xaxis": {
                        "automargin": True,
                        "title": {"text": "Timestamp"}
                    },
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": "do"}
                        },
                    "height": 200,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            }
        ),

        #orp graph
        dcc.Graph(
            id="orpgraph", style={'display': 'inline-block', 'width': '100%'},
            figure={
                "data": [
                    {
                        "x": df_1["timestamp"], #x-axis is timestamp
                        "y": df_1["orp"], #y-axis is ph
                        "name" : "orp",
                        "type": "line",
                        "marker": {"color": "#0448FC"}, #color of graph
                    },
                ],
                "layout": {
                    "showlegend": True,

                    "xaxis": {
                        "automargin": True,
                        "title": {"text": "Timestamp"}
                    },
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": "orp"}
                        },
                    "height": 200,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            }
        ),

        #temperature graph
        dcc.Graph(
            id="temperaturegraph", style={'display': 'inline-block', 'width': '30%'},
            figure={
                "data": [
                    {
                    "x": df_1["timestamp"], #x-axis is timestamp
                    "y": df_1["temperature"], #y-axis is temp
                    "name" : "temperature",
                    "type": "line",
                    "marker": {"color": "#e0553d"}, #color of graph
                    },
                ],
                "layout": {
                    "showlegend": True,

                    "xaxis": {
                        "automargin": True,
                        "title": {"text": "Timestamp"}
                    },
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": "Temp (°C)"}
                        },
                    "height": 200,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            }
        ),
        #tds graph
        dcc.Graph(
            id="tdsgraph", style={'display': 'inline-block', 'width': '80%'},
            figure={
                "data": [
                    {
                    "x": df_1["timestamp"], #x-axis is timestamp
                    "y": df_1["tds"], #y-axis is tds
                    "name" : "tds",
                    "type": "line",
                    "marker": {"color": "#7ff5e3"}, #color of graph
                    },
                ],
                "layout": {
                    "showlegend": True,

                    "xaxis": {
                        "automargin": True,
                        "title": {"text": "Timestamp"}
                    },
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": "tds"}
                        },
                    "height": 200,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            }

        ), 
    ]),


    #map
    # create map using the figure created earlier
    dcc.Graph(id='map',figure=fig), 
    # create datatable to display the dataframe
    
    ]),
    dash_table.DataTable(df_1.to_dict('records'),
        id='data_table',
        columns=[{'id':c, 'name':c} for c in df_1.columns],
        fixed_rows={'headers': True},
        page_size=5
    ),
    html.Div(id='output_div') #cell selected from the datatable
    

]) 

#callback for the user clicks on the dataframe cells
@app.callback(
    Output('output_div', 'children'),
    Input('data_table', 'active_cell'),
    State('data_table', 'data')
)
def getActiveCell(active_cell, data):
    if active_cell:
        col = active_cell['column_id']
        row = active_cell['row']
        cellData = data[row][col]
        return html.P(f'row: {row}, col: {col}, value: {cellData}')
    return html.P('')

# callback to update graphs and table every 5 seconds
@app.callback(
    [Output('phgraph', 'figure'),
     Output('depthgraph', 'figure'),
     Output('dograph', 'figure'),
     Output('orpgraph', 'figure'),
     Output('temperaturegraph', 'figure'),
     Output('tdsgraph', 'figure'),
     Output('map', 'figure'),
     Output('data_table', 'data'),
     Output('data_table', 'columns')],
    Input('interval-component', 'n_intervals')
)

def update(n):
    # use the connection with the database to read the SQL code and create a dataframe in the format the SQL code describes
    df_1 = pd.read_sql(sql, con)
    

    #intializing and create figure for live update
    fig_ph = go.Figure(
    data=[
        go.Scatter(
            x=df_1["timestamp"], 
            y=df_1["ph"], 
            name="pH",
            mode='lines',
            marker=dict(color="#7ff5e3")
        ),
    ],
    layout=go.Layout(
        autosize=True, 
        showlegend=True,
        xaxis=dict(title="Timestamp", automargin=True),
        yaxis=dict(title="ph", automargin=True),
        height=200,
        width=250,
        margin=dict(t=10, l=10, r=10),
    )
)
    
    
    fig_depth = go.Figure(
    data=[
        go.Scatter(
            x=df_1["timestamp"], 
            y=df_1["depth"], 
            name="depth",
            mode='lines',
            line=dict(color="#29CF8D"),
        ),
    ],
    layout=go.Layout(
        autosize=True, 
        showlegend=True,
        xaxis=dict(title="Timestamp", automargin=True),
        yaxis=dict(title="tds", automargin=True),
        height=220,
        width=260,
        margin=dict(t=10, l=10, r=10),
    )
)

    fig_do = go.Figure(
    data=[
        go.Scatter(
            x=df_1["timestamp"], 
            y=df_1["do"], 
            name="do",
            mode='lines',
            line=dict(color="#FC04E5"),
        ),
    ],
    layout=go.Layout(
        autosize=True, 
        showlegend=True,
        xaxis=dict(title="Timestamp", automargin=True),
        yaxis=dict(title="do", automargin=True),
        height=200,
        width=250,
        margin=dict(t=10, l=10, r=10),
    )
)

    fig_orp = go.Figure(
    data=[
        go.Scatter(
            x=df_1["timestamp"], 
            y=df_1["orp"], 
            name="orp",
            mode='lines',
            line=dict(color="#0448FC"),
        ),
    ],
    layout=go.Layout(
        autosize=True, 
        showlegend=True,
        xaxis=dict(title="Timestamp", automargin=True),
        yaxis=dict(title="orp", automargin=True),
        height=220,
        width=260,
        margin=dict(t=10, l=10, r=10),
    )
)
    fig_temp = go.Figure(
    data=[
        go.Scatter(
            x=df_1["timestamp"], 
            y=df_1["temperature"], 
            name="temp",
            mode='lines',
            line=dict(color="#e0553d"),
        ),
    ],
    layout=go.Layout(
        autosize=True, 
        showlegend=True,
        xaxis=dict(title="Timestamp", automargin=True),
        yaxis=dict(title="temp", automargin=True),
        height=230,
        width=260,
        margin=dict(t=10, l=10, r=10),
    )
)

    fig_tds= go.Figure(
    data=[
        go.Scatter(
            x=df_1["timestamp"], 
            y=df_1["tds"], 
            name="tds",
            mode='lines',
            line=dict(color="#F8B902"),
        ),
    ],
    layout=go.Layout(
        autosize=True, 
        showlegend=True,
        xaxis=dict(title="Timestamp", automargin=True),
        yaxis=dict(title="tds", automargin=True),
        height=240,
        width=240,
        margin=dict(t=10, l=10, r=10),
    )
)

    return fig_ph, fig_depth, fig_do, fig_orp, fig_temp, fig_tds,fig, df_1.to_dict('records'), [{'id': c, 'name': c} for c in df_1.columns]

if __name__ == '__main__':
    app.run_server(debug=True)


