import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
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

# intro section data
frac_global = df_social_energy.groupby("Year").mean()
frac_global["Continent"] = "Global"
df_group_by_year_and_continent = df_social_energy.groupby(["Year", "Continent"]).mean()
df_group_by_year_and_continent = df_group_by_year_and_continent.reset_index().append(
    frac_global.reset_index()
)
plot_data = df_group_by_year_and_continent.reset_index()
plot_data = plot_data.drop("index", axis=1)

intro_plot = px.line(
    plot_data,
    x="Year",
    y="Fraction of Low-carbon energy per capita",
    color="Continent",
    width=800,
    height=500,
    title="Fraction of renewable energy across time",
    labels={
        "Year": "Year",
        "Fraction of Low-carbon energy per capita": "Fraction of renewable energy",
    },
)

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
                As the epitome of insightfulness Elon Musk once said: *"If you don't have sustainable energy, you have unsustainable energy."*[[1]]
                Now, more than ever, the need to strive for a green future is essential, but the path is not at all simple or clear.
                Fortunately, green energy sources are on the rise globally[[2]], but things are seldom as simple as they might seem. 
                In the following figure, we see the relationship between the proportion of energy coming from renewable sources against time.
                The data is from Our World in Data from Oxford [[3]] and consists of yearly readings.
                We see the continental trends, and the average of these, called global.
                """,
            className="section__container",
        ),
        dcc.Graph(figure=intro_plot),
        dcc.Markdown(
            """
                As one might suspect, the trends vary greatly from continent to continent. We see that Europe is steadily increasing their fraction of reenewable energy. 
                On the other hand, we see that Africa has in fact declined, which is a point is worth lingering on. 
                For many countries (and especially those of Africa) recordings do not date back as far as, say, those of Europe. 
                Thus, as new countries enter the data, we might see sudden changes in the continental averages. 
                From the graph, we also see that South America is doing a good job as measured by fraction of renewable energy. 
                However, of the 6 populated continents, South America is second to last. 
                As the name global warming suggests, the problem should, at the end of the day, be considered at a global level, which means that at the end of the day, the values for e.g. Asia are more important than those of South America. 
                Asia is more populous than the remaining continents combined, and from the figure we see that their fraction has steadied of at somewhere between 0.05-0.06. 
                In fact, Africa and Asia consists of roughly 76.74% of the world population and are far below the global fraction.
                This is essentially the same argument as "Why should we, the small country of Denmark, bother with climate change when our net contribution is negligible".
                We will refrain from diving into this moral debate. 
                In order to investigate the issue at an even deeper level, we can look at the patterns at a country level across time. 
            """,
            className="section__container",
        ),
        html.Div(
            [
                dcc.Dropdown(
                    sorted(['Coal',
                    'Fossil Fuels', 
                    'Fraction of renewables',
                    'Energy',
                    'Low-carbon energy', 
                    'Gas',
                    'Nuclear', 
                    'Oil',
                    'Renewables', 
                    'Wind',
                    'Solar', 
                    'Hydro']),
                    "Fraction of renewables",
                    id="world_energy_type_selection"
                ),
                html.Div([
                    dcc.Loading(dcc.Graph(id="world_map_energy_animation"), type="graph"),
                ], id="worldmap_graph__section")
            ],
            className="section__container",
            id="worldmap__section",
        ),
        dcc.Markdown(
            """
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
                For most measures, we first and foremost observe that said measure improves over time. 
                Taking HDI as an example, we very clearly see that almost all countries get a higher HDI over time, which in itself is a very positive and hopeful observation.
                We do, however, not see as significant an improvement in the fraction of renewable energy.
                We really only do see the trend of higher fraction following higher measure for the green dots, which is Europe. 
                In order to investigate the relationship in a slightly more robust and precise manner, we can try to model the problem. 


                #### **Modelling relationship between energy and social/economic measures**
                In order to model the relationship, we will make use of a model called partial least squares. 
                In terms of specific variables, we will limit those representing energy to the fraction of reenewable energy, which was also mentioned earlier. 
                We will then investigate how social/economic measures relate to this variable, along with geographic information, here represented by continents. 
                It is important to note that the model works by making projections, and it is therefore not directly interpretable in a strict sense. 
                See e.g. [[4]] for further details on interpretability of the model.
                In terms of the mathematical details, we will not delve in to them here in the article and instead focus on the results of the model.
                Please refer to [[5]] for the mathematical details.  

                When fitting the model, one can extract the so-called PLS components, which spans a latent/hidden representation of the data.
                The components will tell us something about the underlying structure of the data, and will be a way to get some additional insight into the data that is not based purely on plotting.
                We will look at the first 3 components as they tell us the most about the data. 
                For each component, we have the loadings, which basically tell us how strongly the given feature correlates with our response, i.e. the fraction of renewable energy. 
                We have split the features into social/economic measures and geographic information (continents), since we are interested in seeing if certain components might represent certain continents. 
                Since we are looking at hidden structures in the data, we can think about the components as representing "fictional"/archetypical countries. 
                Thus, if we for example see that the first component has a high loading for Oceania, then a "fictional" country that is similar to Oceanic countries will have a high fraction of renewable energy.
                We can also extract how much a component in its entirety correlates with the response, and we can use this to gauge how well we ultimately model the problem.

                #### **From results to broader perspective**
                First of all, it is worth noting that the correlation coefficients between the components and the response are quite low. 
                However, in reality, whether or not a correlation should be deemed low naturally depends on the use-case[[6]]. 
                The PLS model itself is probably not ideal since it does not model time-dependencies. 
                Apart from the shortcomings of the model itself, the data that we feed into the model is most likely not optimal either.
                There are probably a lot of other signals that would be nice to include in order to fully account for the variation in the data. 
                It is also clear from the analysis that there is a great amount of variation between countries, which ties back to the point about data:
                It is hard to adequately represent the specific circumstances that a country finds itself in from data alone.
                For example, Brazil does not have high scores in the social/economic domain, but nevertheless have a large fraction of renewables, which goes against our initial hypothesis.
                It really only does seem like Europe represents the trend that we expected, namely that higher measures of social/economic development leads to a more green energy profile.
                At some level, this shows that our approach is somewhat oversimplistic. 
                This in turn shows that one should be careful making sweeping generalizations about the nature of how countries act in relation to a green transition. 
                Nuance is very important and it is clear that there is no simple path ahead. 

            """,
            className="section__container",
        ),
        # --------  -------- #
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
                                                "label": str(f"PLS Component {i+1}"),
                                                "value": i + 1,
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
                1. [https://blog.ted.com/what-will-the-future-look-like-elon-musk-speaks-at-ted2017/](/)
                1. [https://www.iea.org/news/renewable-electricity-growth-is-accelerating-faster-than-ever-worldwide-supporting-the-emergence-of-the-new-global-energy-economy](/)
                1. [https://ourworldindata.org/](/)
                1. [https://www.jstor.org/stable/2291207?seq=1](/): Paul H. Garthwaite , "An Interpretation of Partial Least Squares", Journal of the American Statistical Association, (1994)
                1. [https://asset-pdf.scinapse.io/prod/2158863190/2158863190.pdf](/): Paul Geladi and Bruce R. Kowalski: "Partial Least-Squares Regression: A Tutorial", Analytica Chimica Acta, (1986)
                1. [https://www.statology.org/what-is-a-strong-correlation/](/)
            """,
            className="section__container",
        ),
    ],
    className="content__container",
)


###-------------- FIRST SECTION PLOTS --------------###
world_df = pd.read_csv("data/pcc_energy_joined_country_codes.csv", index_col=0)
world_df = world_df[world_df.Year < 2020]
world_df["Fraction of renewables"] = world_df["Low-carbon energy per capita (kWh)"] / world_df["Energy per capita (kWh)"]
world_bar_df = world_df.groupby("Year").sum().unstack().reset_index()
world_bar_df.columns = ["x", "Year", "y"]

@app.callback(
    Output("world_map_energy_animation", "figure"),
    Input("world_energy_type_selection", "value"),
)
def display_animated_worldmap(energy_type):
    # Worldmap Figure
    if energy_type in ['Renewables', 'Wind','Solar', 'Hydro', "Low-carbon energy"]:
        color_scale = ["red", "green"]
    elif energy_type == "Energy":
        color_scale = ["black", "yellow"]
    elif energy_type == "Fraction of renewables":
        color_scale = ["red", "green"]
    else:
        color_scale = ["green", "red"]

    if energy_type == "Fraction of renewables":
        range_color = [0, 1]
    else:
        [world_df[energy_type].quantile(.05), world_df[energy_type].quantile(0.95)],

    energy_type = energy_type + " per capita (kWh)" if energy_type != "Fraction of renewables" else energy_type
    world_animation_fig = px.choropleth(
        world_df,
        locations="country_code",
        color=energy_type,
        animation_frame="Year",
        hover_name="Entity",
        basemap_visible=True,
        color_continuous_scale=color_scale,
        range_color=range_color
    )

    world_animation_fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
    world_animation_fig.update_geos(fitbounds="locations", visible=True)
    world_animation_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return world_animation_fig


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

    if dropdown == "Population":
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
        df_int["size"] = df_int["Population"] ** (1 / 2)  # "Energy per capita (kWh)"
        size_max = 40
    else:
        df_int["size"] = df_int[x] * 0 + 0.001
        size_max = 0.001

    if "  Trendline" in values:
        scope = "trace"
        type = "lowess"
        frac = 0.75
    else:
        scope = "trace"
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
        hover_data={"Continent": True, "Year": False, x: True, y: True, "size": False},
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
    social_feats = pd.Series(
        loadings_v["Feature"][loadings_v["Continent"] == False]
    ).unique()
    continents = pd.Series(
        loadings_v["Feature"][loadings_v["Continent"] == True]
    ).unique()

    colormap = {}
    for indx, i in enumerate(social_feats):
        colormap[i] = px.colors.qualitative.Pastel[indx]
    for indx, i in enumerate(continents):
        colormap[i] = px.colors.qualitative.Antique[indx]

    fig = px.bar(
        loadings_v[loadings_v["PLS Component"] == comp],
        x="x",
        y="Loading",
        color="Feature",
        barmode="group",
        facet_col="Continent",
        facet_col_wrap=1,
        color_discrete_map=colormap,
        category_orders={"Continent": [False, True]},
        labels={"x": ""},
        width=1200,
        height=500,
        facet_row_spacing=0.125,
        hover_name="Feature",
        hover_data={
            "Loading": True,
            "Feature": False,
            "Continent": False,
            "x": False,
            "PLS Component": False,
        },
    )

    fig.update_yaxes(
        tickvals=[-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    )
    fig.update_layout(
        xaxis=dict(showticklabels=False),
        xaxis2=dict(showticklabels=False),
        xaxis3=dict(showticklabels=False),
    )

    fig.update_layout(margin=dict(l=40, r=825, t=40, b=40))

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.05))

    if comp == 1:
        anno_text = str(f'<b>PLS Component 1</b><br><br>'+
                    f'The correlation coefficient <br>with the target variable is: <b>{y_loadings.iloc[0,0]:.3f}' + 
                    '</b><br><br>For the continents, we see that it<br>'+
                    '<b>positively</b> correlates with <b>Europe</b>, while<br>'+ 
                    'it <b>negatively</b> correlates with <b>Asia</b>. For<br>'+
                    'the social/economic metrics, we see<br>'+
                    'high <b>positive</b> loadings in measures<br>'+
                    'related do <b>high development</b>, while we<br>'+
                    'have <b>negative</b> correlation for <b>child<br>'+
                    'mortality</b> and <b>population</b>. It seems like<br>'+
                    'this component captures <b>European</b> countries<br>'+
                    'that are <b>highly developed</b> and puts it in<br>'+
                    'opposition to <b>Asian</b> countries. <br><br>'+
                    'An example of such a country could be <br>'+
                    '<b>Iceland.</b>')

    elif comp == 2:
        anno_text = str(f'<b>PLS Component 2</b><br><br>'+
                        f'The correlation coefficient <br>with the target variable is: <b>{y_loadings.iloc[1,0]:.3f}' + 
                        '</b><br><br>Looking at the continents, we see that<br>'+
                        'this component seems to represent <b>South<br>'+ 
                        'American</b> countries, putting it in<br>'+
                        'opposition to <b>Asia</b>. For the social/economic<br>'+
                        'measures, we see something interesting.<br>'+
                        'Despite the component correlating<br>'+
                        '<b>positively</b> with the response, we have<br>'+
                        '<b>negative</b> correlations for many of the<br>'+
                        'measures. This seems to suggest that<br>'+
                        'the <b>South American</b> can have a relatively<br>'+
                        '<b>high fraction of renewables</b> despite<br>'+
                        'scoring low in the social/economic domain.<br><br>'+
                        'A good example of this situation is <b>Brazil</b>.')

    else:
        anno_text = str(f'<b>PLS Component 3</b><br><br>'+
                        f'The correlation coefficient <br>with the target variable is: <b>{y_loadings.iloc[2,0]:.3f}' + 
                        '</b><br><br>Here, it looks like the component<br>'+
                        'are very <b>populous</b> and are <b>relatively,<br>'+
                        'developed</b> while also somewhat<br>' +
                        'representing <b>Oceania</b>. It also seems<br>'+
                        'like <b>African</b> countries (in particular)<br>' +
                        'in this component show the opposite <br>'+
                        'trend than the <b>Asian</b> ones.<br><br>'+
                        'An example of a country that fits <br>'+
                        'this description is <b>China</b>.')

    fig.add_annotation(
        yanchor="top",
        xanchor="left",
        yref="paper",
        xref="paper",
        x=2.15,
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

    fig.for_each_annotation(
        lambda a: a.update(text=a.text.replace("Continent=True", "<b>Continents</b>"))
    )
    fig.for_each_annotation(
        lambda a: a.update(
            text=a.text.replace("Continent=False", "<b>Social metrics</b>")
        )
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port="8050", host="127.0.0.1")
