import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
import os

img_dir = os.getcwd() + "/img/"

# Setup of app
external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)
# This variable is what Procfile points to with gunicorn:
#   web: ... app:server
server = app.server

# Reading locations and counts for locations
df_locations = pd.read_csv("data/locations.csv")
fig = px.scatter_mapbox(
    df_locations,
    lat="latitude_sensor",
    lon="longitude_sensor",
    hover_data={
        "latitude_sensor": False,
        "longitude_sensor": False,
        "count": ":100.0f",
    },
    color_discrete_sequence=["darkgreen"],
    size="count",
    size_max=20,
    zoom=13,
)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


app.layout = html.Div(
    [
        html.Header([
            html.Div([
                html.Img(src=app.get_asset_url("melborn_icon.png"), style={"width": "3rem"}),
                html.H1("Pedestrians in Melbourne AU", style={"margin": "0", "padding": "0"})
            ], style={"display": "flex", "alignItems": "flex-end", "justifyContent": "space-around"})
            ], style={"marginTop": "1.5rem", "width": "100%"}
        ),
        dcc.Markdown(
            [
                "---------------------------------",
                "#### **Introduction to our datasets**",
                "We have chosen to work with the lovely city of melbourne.",
                "Here we are focusing on ...\n",
                "From the [City of melbourne - Open data](https://data.melbourne.vic.gov.au/) website we found these datasets particularely interesting"
            ]
        ),
        dcc.Markdown(
            [
                "----------",
                "#### **Sensor locations**",
                "This is a map of the different pedestrian sensors, and the activity they have tracked throughout the period",
            ]
        ),
        dcc.Graph(figure=fig, style={"width": "100%"}),
    ],
    style={
        "display": "flex",
        "alignItems": "center",
        "flexDirection": "column",
        "maxWidth": "45vw",
        "margin": "0 auto",
    },
)


if __name__ == "__main__":
    app.run_server(debug=True)
