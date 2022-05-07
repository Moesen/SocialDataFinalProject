import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

# Setup of app
external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)
# This variable is what Procfile points to with gunicorn:
#   web: ... app:server
server = app.server

# Reading locations and counts for locations of sensors
world_df = pd.read_csv("data/pcc_energy_joined_country_codes.csv", index_col=0)


###### SECOND SECTION DATA ######
data_pcc_country = pd.read_csv(
    "data/pcc_energy_extrapolated_5_country.csv", index_col=0
)
data_socio_country = pd.read_csv("data/socio_extrapolated_5_country.csv", index_col=0)

data_pcc_country = data_pcc_country.set_index(["Entity", "Continent", "Year"])
data_socio_country = data_socio_country.set_index(["Entity", "Continent", "Year"])

df_social_energy = data_pcc_country.join(data_socio_country, how="outer").reset_index()
df_social_energy = (
    df_social_energy.sort_values(["Year", "Entity"]).reset_index().drop(columns="index")
)
df_social_energy["Fraction of Low-carbon energy per capita"] = (
    df_social_energy["Low-carbon energy per capita (kWh)"]
    / df_social_energy["Energy per capita (kWh)"]
)
col_int = [
    "GDP per capita ($)",
    "Child mortality rate (under 5 years - %)",
    "HDI",
    "Life expectancy (years)",
    "Population",
    "Tertiary education (%)",
    "Internet users (%)",
    "Tax revenue of total GDP (%)",
]
df_social_energy = (
    df_social_energy.sort_values(["Year", "Continent", "Entity"])
    .reset_index()
    .drop(columns="index")
)



###### THIRD SECTION DATA ######
y_loadings = pd.read_csv("data/y_loadings_v.csv", index_col=0)
loadings_v = pd.read_csv("data/loadings_v.csv", index_col=0)
test_data = pd.read_csv("data/test_data.csv", index_col=0)


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
                #### **Past, present and future of energy**
                As the epitome of insightfulness Elon Musk once said: *"If you don't have sustainable energy, you have unsustainable energy."*(source: https://blog.ted.com/what-will-the-future-look-like-elon-musk-speaks-at-ted2017/)
                Now, more than ever, the need to strive for a green future is essential, but the path is not at all simple or clear.
                Fortunately, green energy sources are on the rise globally (source: https://www.iea.org/news/renewable-electricity-growth-is-accelerating-faster-than-ever-worldwide-supporting-the-emergence-of-the-new-global-energy-economy), but things are seldom as simple as they might seem. 
                In the following figure, we see the relationship between the proportion of energy coming from renewable sources against time.
                The data is from (source: https://ourworldindata.org/) and consists of yearly readings.
                We see the continental trends, and the average of these, called global. 

                INSERT STATIC GRAPH

                As one might suspect, the trends vary greatly from continent to continent. We see that Europe is steadily increasing their fraction of reenewable energy. 
                On the other hand, we see that Africa has in fact declined, which is a point is worth lingering on. 
                For many countries (and especially those of Africa) recordings do not date back as far as, say, those of Europe. 
                Thus, as new countries enter the data, we might see sudden changes in the continental averages. 
                From the graph, we also see that South America is doing a good job as measured by fraction of renewable energy. 
                However, of the 6 populated continents, South Africa is second to last. 
                As the name global warming suggests, the problem should, at the end of the day, be considered at a global level, which means that at the end of the day, the values for e.g. Asia are more important than those of South America. 
                Asia is more populous than the remaining continents combined, and from the figure we see that their fraction has steadied of at somewhere between 0.05-0.06. 
                In fact, Africa and Asia consists of roughly 76.74% of the world population and are far below the global fraction.
                This is essentially the same argument as "Why should we, the small country of Denmark, bother with climate change when our net contribution is negligible".
                We will refrain from diving into this moral debate. 
                In order to investigate the issue at an even deeper level, we can look at the patterns at a country level across time. 

                INSERT MOESMAND FIGURE 


                At the end of the day, what we see is that there is quite large variety between countries when we measure their fraction of renewable energy. 
                One posssible part of the explanation is differences in social and economic measures between countries. 
                For the remainder of this article, we will delve deeper into this relationship between energy consumption and social/economic measures.   
                
                #### **Exploring relationship between energy and social/economic measures**
                Our hypothesis is that energy consumption is linked with measures of social and enomic aspects at several levels. 
                Additionally, we hypothesize that the causality of this relationship can be hard to determine, but our guess is that higher social/economic measures eventually will lead to a more green energy profile for a country.
                Thus, when a country gets richer (both economically and socially), it will transition to haaving a larger fraction of renewable energy.
                In order to investigate this hypothesis, we graph the fraction of renewable energy against a specific social/economic measure, and then let the data flow with time.
                Each point corresponds to a country. 

                INSERT WEIS FIGURE 

                For most measures, we irst and foremost observe that said measure improves over time. 
                Taking HDI as an example, we very clearly see that almost all countries get a higher HDI over time, which in itself is a very positive and hopeful observation.
                We do, however, not see as significant an improvement in the fraction of renewable energy.
                We really only do see the trend of higher fraction following higher measure for the green dots, which is Europe. 
                In order to investigate the relationship in a slightly more robust and precise manner, we can try to model the problem. 


                #### **Modelling relationship between energy and social/economic measures**
                In order to model the relationship, we will make use of a model called partial least squares. 
                In terms of specific variables, we will limit those representing energy to the fraction of reenewable energy, which was also mentioned earlier. 
                We will then investigate how social and economic measures relate to this variable. 
                It is important to note that the model works by making projections, thus creating a latent space. 
                This means that we have to be careful with how we interpret the results of the model.
                See e.g. (source: ) for further details. 

                


            """,
            className="section__container",
        ),
        # --------  -------- #
        html.Div(
            [
                dcc.Dropdown(
                    sorted(
                        [
                            "Coal per capita (kWh)",
                            "Fossil Fuels per capita (kWh)",
                            "Energy per capita (kWh)",
                            "Low-carbon energy per capita (kWh)",
                            "Gas per capita (kWh)",
                            "Nuclear per capita (kWh)",
                            "Oil per capita (kWh)",
                            "Renewables per capita (kWh)",
                            "Wind per capita (kWh)",
                            "Solar per capita (kWh)",
                            "Hydro per capita (kWh)",
                        ]
                    ),
                    "Coal per capita (kWh)",
                    id="world_energy_type_selection",
                ),
                html.Div(
                    [
                        dcc.Loading(
                            dcc.Graph(id="world_map_energy_animation"), type="graph"
                        ),
                        # dcc.Loading(dcc.Graph(id="world_bar_energy_animation"), type="graph")
                    ],
                    id="worldmap_graph__section",
                ),
            ],
            className="section__container",
            id="worldmap__section",
        ),
        # -------- Social data and energy type relationship -------- #
        html.Br(),
        dcc.Markdown(
            """
            #### **Tester graph**
            here is the most something something graph
            """
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    "Choose social measure to compare with fraction of low-carbon energy use",
                                    className="heading",
                                )
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    dcc.Dropdown(
                                        id="dropdown",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in sorted(col_int)
                                        ],
                                        value="HDI",
                                    )
                                ],
                                className="dropdown",
                                id="social_data_type_selection",
                            )
                        )
                    ]
                ),
                dcc.Checklist(
                    ["  Scatter", "  Trendline", "  Continent"],
                    ["  Continent", "  Scatter"],
                    inline=False,
                    id="checklist_social_energy_compare",
                    labelStyle={"display": "block"},
                ),
                html.Div([dcc.Loading(dcc.Graph(id="graph_scatter"), type="graph")]),
            ],
            className="section__container",
        ),
        dcc.Markdown(
            """
        hehehehehehehehehehehehehehe
        """,
            className="section__container",
        ),
        html.Br(),
        dcc.Markdown(
            """
            #### **Results**
            Look at these PLS components my friends
            """
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    "",
                                    className="heading",
                                )
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    dcc.Dropdown(
                                        id="dropdown2",
                                        options=[
                                            {
                                                "label": str(f'PLS Component {i+1}'), 
                                                "value": i+1
                                            }
                                            for i in range(3)
                                        ],
                                        value=1,
                                    )
                                ],
                                className="dropdown",
                                id="pls_component_type_selection",
                            )
                        )
                    ]
                ),
                html.Div([dcc.Loading(dcc.Graph(id="pls_components"), type="graph")]),
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


###-------------- FIRST SECTION PLOTS --------------###
world_df = pd.read_csv("data/pcc_energy_joined_country_codes.csv", index_col=0)
world_bar_df = world_df.groupby("Year").sum().unstack().reset_index()
world_bar_df.columns = ["x", "Year", "y"]


@app.callback(
    Output("world_map_energy_animation", "figure"),
    Input("world_energy_type_selection", "value"),
)
def display_animated_worldmap(energy_type):
    # Worldmap Figure
    world_animation = px.choropleth(
        world_df,
        locations="country_code",
        color=energy_type,
        animation_frame="Year",
        hover_name="Entity",
        color_continuous_scale=["#aaa", "green"],
        range_color=[world_df[energy_type].min(), world_df[energy_type].max()],
    )

    bar_animation = px.bar(
        world_bar_df,
        x="y",
        y="x",
        animation_frame="Year",
        orientation="h",
    )

    bar_animation.update_layout(
        margin={"t": 0, "l": 0, "r": 0, "b": 0},
    )

    world_animation.update_layout(
        margin={"t": 0, "l": 0, "r": 0, "b": 0},
        coloraxis_showscale=False,  # Removes colorbar
    )

    world_animation.add_trace(bar_animation.data[0])
    for i, frame in enumerate(world_animation.frames):
        world_animation.frames[i].data += (bar_animation.frames[i].data[0],)

    return world_animation


###-------------- SECOND SECTION PLOTS --------------###
@app.callback(
    Output("graph_scatter", "figure"),
    [Input("dropdown", "value"), Input("checklist_social_energy_compare", "value")],
)
def update_graph(dropdown, values):
    x = dropdown
    y = "Fraction of Low-carbon energy per capita"
    df_int = (
        df_social_energy.iloc[
            np.sum(np.array(df_social_energy[[x, y]].isnull()) * 1.0, axis=1) == 0
        ]
        .reset_index()
        .drop(columns="index")
    )

    if dropdown == 'Population':
        log_axis = True
    else:
        log_axis = False

    for i in np.sort(df_int["Year"].unique()):
        if len(df_int["Continent"][df_int["Year"] == i].unique()) != 6:
            df_int = df_int[df_int["Year"] != i].reset_index().drop(columns="index")
        else:
            break

    if "  Continent" in values:
        color = "Continent"
        trendline_color = None
    else:
        color = None
        trendline_color = "Black"

    if "  Scatter" in values:
        df_int['size'] = df_int["Population"] ** (1 / 2)  # "Energy per capita (kWh)"
        size_max = 40
    else:
        df_int['size'] = df_int[x] * 0 + 0.001
        size_max = 0.001

    if "  Trendline" in values:
        scope = "trace"
        type = "lowess"
        frac = 0.75
    else:
        scope = None
        type = None
        frac = None

    fig1 = px.scatter(
        df_int,
        x=x,
        y=y,
        size="size",
        color=color,
        animation_frame="Year",
        animation_group="Entity",
        log_x=log_axis,
        size_max=size_max,
        range_x=[np.min(df_int[x]), np.max(df_int[x]) * 1.1],
        range_y=[-0.2, 1.2],
        labels={y: "Fraction of Renewable Energy ", x: x},
        trendline_scope=scope,
        trendline=type,
        trendline_options=dict(frac=frac),
        trendline_color_override=trendline_color,
        hover_name="Entity",
        hover_data={"Continent": True,
                    "Year": False,
                    x: True,
                    y: True,
                    "size": False}
    )

    fig1.update_layout(margin={"t": 0, "l": 0, "r": 0, "b": 0})
    fig1.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
    fig1.add_hline(y=1, line_width=1, line_dash="dash", line_color="gray")
    fig1.add_hline(y=0, line_width=1, line_dash="dash", line_color="gray")
    if ("  Trendline" not in values) & ("  Scatter" not in values):
        fig1.add_annotation(
            x=1 / 2 * (np.max(df_int[x]) * 1.1 - np.min(df_int[x])),
            y=0.5,
            text="Choose either Scatter or Trendline to show data",
            font=dict(family="Courier New, monospace", size=16, color="Black"),
            align="center",
            bordercolor="Black",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ADD8E6",
            showarrow=False,
            opacity=0.8,
        )

    return fig1



###-------------- THIRD SECTION PLOTS --------------###
@app.callback(
    Output("pls_components", "figure"),
    Input("dropdown2", "value"),
)
def update_graph(dropdown2):
    comp = dropdown2
    social_feats = pd.Series(loadings_v['Feature'][loadings_v['Continent'] == False]).unique()
    continents =  pd.Series(loadings_v['Feature'][loadings_v['Continent'] == True]).unique()

    colormap = {}
    for indx,i in enumerate(social_feats):
        colormap[i] = px.colors.qualitative.Pastel[indx]
    for indx,i in enumerate(continents):
        colormap[i] = px.colors.qualitative.Antique[indx]


    fig = px.bar(loadings_v[loadings_v['PLS Component'] == comp], x="x", y="Loading", color="Feature", barmode='group',
                facet_col='Continent', facet_col_wrap=1, color_discrete_map=colormap,
                category_orders={'Continent':[False, True]},
                labels={'x':''},
                width=1200, height=400,
                facet_row_spacing = 0.125,
                hover_name="Feature",hover_data={"Loading": True,
                                                "Feature": False,
                                                "Continent": False,
                                                "x":False,
                                                "PLS Component":False})

    fig.update_yaxes(tickvals=[-1.0,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1.0])
    fig.update_layout(
        xaxis = dict(
            showticklabels=False
        ),
        xaxis2 = dict(
            showticklabels=False
        ),
        xaxis3 = dict(
            showticklabels=False
        )
    )

    fig.update_layout(
        margin=dict(l=40, r=750, t=40, b=40)
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.05
    ))

    if comp == 1:
        anno_text = str(f'         <b>PLS Component 1</b><br><br>'+
                        f'The correlation coefficient <br>with the target variable is: <b>{y_loadings.iloc[0,0]:.3f}' + 
                        '</b><br><br>This PLS component seems to capture<br>'+
                        'the highly developed <b>European</b><br>'+ 
                        'countries... Etc.<br>'+
                        'Example: Iceland')
    elif comp == 2:
        anno_text = str(f'         <b>PLS Component 2</b><br><br>'+
                        f'The correlation coefficient <br>with the target variable is: <b>{y_loadings.iloc[1,0]:.3f}' + 
                        '</b><br><br>This PLS component seems to capture<br>'+
                        'the poorly developed <b>South</b><br>'+ 
                        '<b>American</b> countries. (weird).. Etc.<br>'+
                        'Example: Brazil')
    else:
        anno_text = str(f'         <b>PLS Component 3</b><br><br>'+
                        f'The correlation coefficient <br>with the target variable is: <b>{y_loadings.iloc[2,0]:.3f}' + 
                        '</b><br><br>This PLS component seems to capture<br>'+
                        'the larger <b>Asian</b> countries. Etc<br>'+ 
                        'Example: China')

    fig.add_annotation(
        yanchor="top",
        xanchor="left",
        yref = 'paper',
        xref = 'paper',
        x=1.95,
        y=1,
        text=anno_text,
        font=dict(family="Courier New, monospace", size=16, color="Black"),
        align="left",
        bordercolor="Black",
        borderwidth=1,
        borderpad=4,
        bgcolor="#EBECF0",
        showarrow=False,
        opacity=0.8,
    )

    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("Continent=True", "<b>Continents</b>")))
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("Continent=False", "<b>Social metrics</b>")))
        
    return fig




if __name__ == "__main__":
    app.run_server(debug=True, port=8050, host="127.0.0.1")
