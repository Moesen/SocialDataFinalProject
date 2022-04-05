import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
import plotly.express as px
import pandas as pd

# Setup of app
external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)
# This variable is what Procfile points to with gunicorn:
#   web: ... app:server
server = app.server

# Reading locations and counts for locations
df_locations = pd.read_csv("data/locations.csv")
fig = px.scatter_mapbox(df_locations,
                     lat="latitude_sensor",
                     lon="longitude_sensor",
                     hover_data={'latitude_sensor': False,
                                 "longitude_sensor": False,
                                 "count": ":100.0f"},
                     color_discrete_sequence=["darkgreen"],
                     size="count",
                     size_max=20,
                     zoom=13)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


app.layout = html.Div([
    html.Header([
        html.H1("Pedestrians in Melbourne AU")
        ], style = {"margin-top": "1.5rem"}
    ),
    dcc.Markdown(["---------------------------------",
                  "#### **Overview of the data**",
                  "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                  ]),
    dcc.Markdown(["----------",
                  "#### **Sensor locations**",
                  "This is a map of the different pedestrian sensors, and the activity they have tracked throughout the period"
                  ]),
    dcc.Graph(figure=fig, style={"width": "100%"})
    ], style={"display": "flex", "align-items": "center", "flex-direction": "column", "max-width": "45vw", "margin": "0 auto"}
)


if __name__ == "__main__":
    app.run_server(debug=True)
