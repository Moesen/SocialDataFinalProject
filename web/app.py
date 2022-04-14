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
                        dcc.Markdown(
                            """
                            # Energy Consumption and 
                            # Social/Economic Development
                            ##### by Kelvin Foster, Nicolai Weisbjerg and Gustav Lang Moesmand
                            """
                        ),
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
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Adipiscing elit duis tristique sollicitudin nibh sit amet commodo nulla. Magna fermentum iaculis eu non diam phasellus vestibulum lorem sed. Blandit libero volutpat sed cras ornare arcu dui vivamus. Phasellus vestibulum lorem sed risus ultricies tristique. Aliquam faucibus purus in massa tempor nec feugiat. Libero volutpat sed cras ornare. Diam vulputate ut pharetra sit amet. Interdum consectetur libero id faucibus nisl tincidunt eget nullam. Lectus nulla at volutpat diam ut venenatis tellus in metus. Diam vel quam elementum pulvinar etiam non quam lacus. Volutpat sed cras ornare arcu dui vivamus arcu felis. Porttitor massa id neque aliquam vestibulum morbi blandit cursus. Platea dictumst quisque sagittis purus.

                Ac turpis egestas maecenas pharetra convallis posuere morbi. Leo urna molestie at elementum. At imperdiet dui accumsan sit amet. Orci nulla pellentesque dignissim enim sit amet. Imperdiet sed euismod nisi porta lorem mollis aliquam. Aliquet lectus proin nibh nisl. Id aliquet risus feugiat in ante metus dictum at. In tellus integer feugiat scelerisque. Egestas integer eget aliquet nibh. Semper viverra nam libero justo laoreet sit amet cursus sit. Urna nec tincidunt praesent semper feugiat nibh sed. Varius quam quisque id diam vel quam elementum pulvinar etiam. In tellus integer feugiat scelerisque varius. Netus et malesuada fames ac. Praesent semper feugiat nibh sed pulvinar proin gravida hendrerit lectus. Tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada. Fames ac turpis egestas sed tempus urna et pharetra. Sed turpis tincidunt id aliquet. Neque viverra justo nec ultrices dui.

                In hendrerit gravida rutrum quisque non. In arcu cursus euismod quis viverra. Sed tempus urna et pharetra. Fermentum dui faucibus in ornare. Purus ut faucibus pulvinar elementum integer enim neque. Adipiscing diam donec adipiscing tristique. Sed risus ultricies tristique nulla aliquet. Convallis convallis tellus id interdum velit laoreet id donec. Non arcu risus quis varius quam quisque id. Suscipit adipiscing bibendum est ultricies integer. Cras sed felis eget velit aliquet sagittis id consectetur.

                Purus in mollis nunc sed id semper risus. Nisi quis eleifend quam adipiscing vitae proin. Sagittis purus sit amet volutpat consequat. Velit scelerisque in dictum non consectetur a. Vel orci porta non pulvinar. Auctor neque vitae tempus quam pellentesque. Magna fringilla urna porttitor rhoncus dolor. Fringilla phasellus faucibus scelerisque eleifend donec pretium vulputate sapien nec. Lorem mollis aliquam ut porttitor leo a diam sollicitudin tempor. Morbi enim nunc faucibus a pellentesque. Ac turpis egestas sed tempus urna et pharetra. Mus mauris vitae ultricies leo integer. Sed elementum tempus egestas sed sed risus pretium quam. A arcu cursus vitae congue mauris rhoncus. Morbi quis commodo odio aenean sed adipiscing diam. Varius vel pharetra vel turpis nunc eget lorem dolor sed. Habitant morbi tristique senectus et netus et.

                Turpis massa sed elementum tempus egestas. Felis eget velit aliquet sagittis id consectetur purus ut faucibus. Enim diam vulputate ut pharetra sit. Placerat orci nulla pellentesque dignissim enim sit amet. Sed euismod nisi porta lorem mollis aliquam ut porttitor. Vel orci porta non pulvinar neque. Rhoncus urna neque viverra justo nec. Donec et odio pellentesque diam volutpat commodo. Et magnis dis parturient montes nascetur ridiculus mus. Facilisis magna etiam tempor orci eu lobortis elementum nibh tellus. Molestie ac feugiat sed lectus vestibulum.
                
                From the [City of melbourne - Open data](https://data.melbourne.vic.gov.au/) website we found these datasets particularely interesting
            """,
            className="section__container",
        ),
        # --------  -------- #
        dcc.Markdown(
            """
                ----------
                #### **Sensor locations**
                This is a map of the different pedestrian sensors, and the activity they have tracked throughout the period
            """,
            className="section__container",
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
            """,
            className="section__container",
        ),
    ],
    className="content__container",
)

if __name__ == "__main__":
    app.run_server(debug=True)
