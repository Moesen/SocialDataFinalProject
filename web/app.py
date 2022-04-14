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



if __name__ == "__main__":
    app.run_server(debug=True)
