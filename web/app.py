import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
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
world_df = pd.read_csv("data/pcc_energy_joined_country_codes.csv", index_col=0)





###### SKRIV BESKRIVELSE ############# SKRIV BESKRIVELSE #######
data_pcc_country = pd.read_csv("data/pcc_energy_extrapolated_5_country.csv",index_col=0)
data_socio_country = pd.read_csv("data/socio_extrapolated_5_country.csv",index_col=0)

data_pcc_country = data_pcc_country.set_index(['Entity','Continent','Year'])
data_socio_country = data_socio_country.set_index(['Entity','Continent','Year'])

df_social_energy = data_pcc_country.join(data_socio_country,how='outer').reset_index()
df_social_energy = df_social_energy.sort_values(['Year','Entity']).reset_index().drop(columns='index')
df_social_energy['Fraction of Low-carbon energy per capita'] = df_social_energy['Low-carbon energy per capita (kWh)']/df_social_energy['Energy per capita (kWh)']
col_int = ['GDP per capita ($)','Child mortality rate (under 5 years - %)','HDI','Life expectancy (years)',
           'Tertiary education (%)','Internet users (%)','Tax revenue of total GDP (%)']
df_social_energy = df_social_energy.sort_values(['Year','Continent','Entity'])

###### SKRIV BESKRIVELSE ############# SKRIV BESKRIVELSE #######




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

         # -------- Social data and energy type relationship -------- #
        html.Br(),
        dcc.Markdown(
            """
            #### **Tester graph**
            here is the most something something graph
            """
        ),
        html.Div([
            dbc.Row([dbc.Col([html.Div("Relationship between energy types and social data", className="heading")])]),
            dbc.Row([dbc.Col(html.Div([dcc.Dropdown(id='dropdown',
                                options=[{'label': i, 'value': i} for i in sorted(col_int)],
                                value="GDP per capita ($)")],
                                className="dropdown",
                                id="social_data_type_selection")
            )]),
            dcc.Checklist(
                ['Continent', 'Trendline', 'Scatter'],
                ['Continent', 'Scatter'],
                inline=False,
                id = "checklist_social_energy_compare"
            ),
            dcc.Tabs(id="tabs-selector",
                        value="tab-1",
                        className="custom-tabs-container",
                        children=[
                                dcc.Tab(label="ScatterPlot",
                                        value="tab-1",
                                        className="custom-tab",
                                        children=[html.Div([dcc.Graph(id="graph_scatter")]),
                                                    ]),
                                dcc.Tab(label="ScatterPlot_OverallTrend",
                                        value="tab-2",
                                        className="custom-tab",
                                        children=[html.Div([dcc.Graph(id="graph_scatter_overall_trend")]),
                                                    ]),
                                dcc.Tab(label="Continent_trend",
                                        value="tab-3",
                                        className="custom-tab",
                                        children=[html.Div([dcc.Graph(id="graph_continent_trend")]),
                                                    ]),
                        ]),
            ],
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


@app.callback([Output('graph_scatter', 'figure'),
               Output('graph_scatter_overall_trend', 'figure'),
               Output("graph_continent_trend", "figure")],
              [Input('dropdown', 'value'),
               Input('tabs-selector', 'value')])
def update_graph(dropdown, tab):
    fig1 = px.scatter()
    fig2 = px.scatter()
    fig3 = px.scatter()

    x = dropdown
    y = "Fraction of Low-carbon energy per capita"
    df_int = (df_social_energy.iloc[np.sum(np.array(df_social_energy[[x,y]].isnull())*1.0,axis=1) == 0]
                .reset_index()
                .drop(columns='index'))
    fig1 = px.scatter(df_int, 
                          x=x, y=y,
                          size="Energy per capita (kWh)",
                          color="Continent",
                          animation_frame="Year", animation_group="Entity",
                          hover_name="Entity", log_x=False, size_max=60,
                          range_x=[np.min(df_int[x]),np.max(df_int[x])*1.1], 
                          range_y=[-0.2,1.2])
                          #trendline_scope='trace',
                          #trendline="lowess", 
                          #trendline_options=dict(frac=0.33))#,trendline_color_override='black')
    if tab == 'tab-1':
        fig1 = px.scatter(df_int, 
                          x=x, y=y,
                          size="Energy per capita (kWh)",
                          color="Continent",
                          animation_frame="Year", animation_group="Entity",
                          hover_name="Entity", log_x=False, size_max=60,
                          range_x=[np.min(df_int[x]),np.max(df_int[x])*1.1], 
                          range_y=[-0.2,1.2])
                          #trendline_scope='trace',
                          #trendline="lowess", 
                          #trendline_options=dict(frac=0.33))#,trendline_color_override='black')
    elif tab == 'tab-2':
        fig2 = px.scatter(df_int, 
                          x=x, y=y,
                          size="Energy per capita (kWh)",
                          color="Continent",
                          animation_frame="Year", animation_group="Entity",
                          hover_name="Entity", log_x=False, size_max=60,
                          range_x=[np.min(df_int[x]),np.max(df_int[x])*1.1], 
                          range_y=[-0.2,1.2])
                          #trendline_scope='trace',
                          #trendline="lowess", 
                          #trendline_options=dict(frac=0.33))#,trendline_color_override='black')
    elif tab == 'tab-3':
        fig3 = px.scatter(df_int, 
                          x=x, y=y,
                          size="Energy per capita (kWh)",
                          color="Continent",
                          animation_frame="Year", animation_group="Entity",
                          hover_name="Entity", log_x=False, size_max=60,
                          range_x=[np.min(df_int[x]),np.max(df_int[x])*1.1], 
                          range_y=[-0.2,1.2])
                          #trendline_scope='trace',
                          #trendline="lowess", 
                          #trendline_options=dict(frac=0.33))#,trendline_color_override='black')

    fig1.update_layout(
        margin={"t": 0, "l": 0, "r": 0, "b": 0}
    )
    return fig1,fig2,fig3







if __name__ == "__main__":
    app.run_server(debug=True)
