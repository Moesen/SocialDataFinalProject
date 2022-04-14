import os

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


# Setup of app
external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)
# This variable is what Procfile points to with gunicorn:
#   web: ... app:server
server = app.server

# Reading locations and counts for locations of sensors
df_sens_locations = pd.read_csv("data/locations.csv")
df_sens_activity = pd.read_csv("data/monthly_sensor_data.csv")

fig = px.scatter_mapbox(
    df_sens_locations,
    lat="latitude_sensor",
    lon="longitude_sensor",
    hover_data={
        "latitude_sensor": False,
        "longitude_sensor": False,
        "count": ":100.0f",
        "site_id": True
    },
    color_discrete_sequence=["darkgreen"],
    size="count",
    size_max=20,
    zoom=13,
)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 10, "l": 10, "b": 0}, width=500, height=500)

app.layout = html.Div(
    [
        # -------- HEADER -------- #
        html.Header(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("melborn_icon.png"),
                            className="melbourne_icon",
                        ),
                        html.H1("Pedestrians in Melbourne AU"),
                        html.Button("Notebook", className="notebook_button")
                    ],
                    className="header__container",
                )
            ]
        ),
        # -------- DATASET Introduction -------- #
        dcc.Markdown(
            """
                ---------------------------------
                #### **Introduction to our datasets**
                We have chosen to work with the lovely city of melbourne.
                Here we are focusing on ...\n
                From the [City of melbourne - Open data](https://data.melbourne.vic.gov.au/) website we found these datasets particularely interesting
                * [Link to first dataset](/): Small description of dataset
                * [Link to second dataset](/): Small description of dataset
                * [Link to third dataset](/): Small description of dataset
                * [Link to fourth dataset](/): Small description of dataset
            """
        ),
        # --------  -------- #
        dcc.Markdown(
            """
                ----------
                #### **Sensor locations**
                This is a map of the different pedestrian sensors, and the activity they have tracked throughout the period
            """
        ),
        html.Div([
            dcc.Graph(figure=fig, id="sensor-map", hoverData={"points": [{"customdata": [1001]}]}),
            dcc.Graph(id="timeseries-sensor-activity")
        ], id="sensor-location-graphs__container"
        ),
        dcc.Markdown(
            """
                ------------
                #### **References**
                For the curious person, these are these sources helped
                us better understand what we wer working with. We 
                have tried to show when we use them,
                so if you found anything especially interesting
                these are a great way to continue the journey.
                
                1. [First reference](/): Small description
                1. [Second reference](/): Small description
                1. [Second reference](/): Small description
                1. [Second reference](/): Small description
                * [ ] : test
                * [x] : other test   
            """
        ),
    ],
    className="content__container",
)

@app.callback(
    Output("timeseries-sensor-activity", "figure"),
    Input("sensor-map", "hoverData")
)
def update_sensor_activity_timeseries(hoverData):
    site_id = hoverData['points'][0]['customdata'][-1]
    site_df = df_sens_activity[df_sens_activity.site_id == site_id]
    
    fig = px.scatter(site_df, x="month_name", y="count")
    fig.update_traces(mode="lines+markers")
    fig.update_yaxes(showgrid=False)
    fig.add_annotation(x=.80, y=.90, xanchor="left", yanchor="bottom", xref="paper", yref="paper", showarrow=False, align="right", text=f"Site ID: {site_id}")
    fig.update_yaxes(range=[0, site_df["count"].max()])
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
