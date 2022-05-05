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
df_social_energy = df_social_energy.sort_values(['Year','Continent','Entity']).reset_index().drop(columns='index')

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
            dbc.Row([dbc.Col([html.Div("Choose social measure to compare with fraction of low-carbon energy use", className="heading")])]),
            dbc.Row([dbc.Col(html.Div([dcc.Dropdown(id='dropdown',
                                options=[{'label': i, 'value': i} for i in sorted(col_int)],
                                value="GDP per capita ($)")],
                                className="dropdown",
                                id="social_data_type_selection")
            )]),
            dcc.Checklist(
                ['Scatter', 'Trendline', 'Continent'],
                ['Continent', 'Scatter'],
                inline=False,
                id = "checklist_social_energy_compare",
                labelStyle={'display': 'block'}
            ),
            html.Div([
                dcc.Loading(dcc.Graph(id="graph_scatter"), type="graph")])
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


@app.callback(Output('graph_scatter', 'figure'),
             [Input('dropdown', 'value'),
              Input('checklist_social_energy_compare','value')])
def update_graph(dropdown, values):
    x = dropdown
    y = "Fraction of Low-carbon energy per capita"
    df_int = (df_social_energy.iloc[np.sum(np.array(df_social_energy[[x,y]].isnull())*1.0,axis=1) == 0]
                .reset_index()
                .drop(columns='index'))

    for i in np.sort(df_int['Year'].unique()):
        if len(df_int['Continent'][df_int['Year']==i].unique()) != 6:
            df_int = df_int[df_int['Year'] != i].reset_index().drop(columns='index')
        else:
            break;

    if "Continent" in values:
        color = 'Continent'
    else:
        color = None

    if "Scatter" in values:
        size = "Energy per capita (kWh)"
        size_max = 40
    else:
        size = df_int[x]*0+0.001
        size_max = 0.001

    if "Trendline" in values:
        scope = 'trace'
        type = 'lowess'
        frac = 0.6
    else:
        scope = None
        type = None
        frac = None
        
    fig1 = px.scatter(df_int, 
                      x=x, y=y,
                      size=size,
                      color=color,
                      animation_frame="Year", animation_group="Entity",
                      hover_name="Entity", log_x=False, size_max=size_max,
                      range_x=[np.min(df_int[x]),np.max(df_int[x])*1.1], 
                      range_y=[-0.2,1.2],
                      labels={y:'Fraction: Low-carbon energy', x:x},
                      trendline_scope=scope,
                      trendline=type,
                      trendline_options=dict(frac=frac))

    fig1.update_layout(
        margin={"t": 0, "l": 0, "r": 0, "b": 0}
    )

    if ('Trendline' not in values) & ('Scatter' not in values):
        fig1.add_annotation(
            x=1/2*(np.max(df_int[x])*1.1-np.min(df_int[x])),
            y=0.5,
            text="Choose either Scatter or Trendline to show data",
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="Black"
                ),
            align="center",
            bordercolor="Black",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ADD8E6",
            showarrow=False,
            opacity=0.8
            )

    return fig1







if __name__ == "__main__":
    app.run_server(debug=True)
