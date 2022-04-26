import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from matplotlib.pyplot import colorbar

# Setup of app
external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)
# This variable is what Procfile points to with gunicorn:
#   web: ... app:server
server = app.server

# Reading locations and counts for locations of sensors
world_df = pd.read_csv("data/pcc_energy_joined_country_codes.csv")

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

            """,
            className="section__container",
        ),
        # --------  -------- #
        html.Div(
            [
                dcc.Dropdown(
                    sorted(['Coal per capita (kWh)',
                    'Fossil Fuels per capita (kWh)', 
                    'Energy per capita (kWh)',
                    'Low-carbon energy per capita (kWh)', 
                    'Gas per capita (kWh)',
                    'Nuclear per capita (kWh)', 
                    'Oil per capita (kWh)',
                    'Renewables per capita (kWh)', 
                    'Wind per capita (kWh)',
                    'Solar per capita (kWh)', 
                    'Hydro per capita (kWh)']),
                    "Coal per capita (kWh)",
                    id="world_energy_type_selection"
                ),
                html.Div([
                    dcc.Loading(dcc.Graph(id="world_map_energy_animation"), type="graph"),
                    dcc.Loading(dcc.Graph(id="world_bar_energy_animation"), type="graph")
                ], id="worldmap_graph__section")
            ],
            className="section__container",
            id="worldmap__section"
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


@app.callback(
    Output("world_map_energy_animation", "figure"),
    Input("world_energy_type_selection", "value")
    )
def display_animated_worldmap(energy_type):
    df = world_df
    # Worldmap Figure
    world_animation = px.choropleth(
        df,
        locations="country_code",
        color=energy_type,
        animation_frame="Year",
        hover_name="Entity",
        color_continuous_scale=["#aaa", "green"],
        range_color=[df[energy_type].min(), df[energy_type].max()]
    )

    world_animation.update_layout(
        margin={"t": 0, "l": 0, "r": 0, "b": 0},
        coloraxis_showscale=False,  # Removes colorbar
    )

    return world_animation


if __name__ == "__main__":
    app.run_server(debug=True)
