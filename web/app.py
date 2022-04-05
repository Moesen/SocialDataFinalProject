from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.LUX]

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
   html.Header("Test")
], style={"display": "flex", "justify-content": "center"})


if __name__ == "__main__":
    app.run_server(debug=True)
