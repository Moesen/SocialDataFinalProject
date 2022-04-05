import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html

external_stylesheets = [dbc.themes.LUX]

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.Header([
        html.H1("Pedestrians in Melbourne AU")
        ], style = {"margin-top": "1.5rem"}
    ),
    dcc.Markdown(["---------------------------------",
                  "#### **Overview of the data**",
                  "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                  ]),
    ], style={"display": "flex", "align-items": "center", "flex-direction": "column", "max-width": "45vw", "margin": "0 auto"}
)


if __name__ == "__main__":
    app.run_server(debug=True)
