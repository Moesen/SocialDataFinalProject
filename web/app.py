import os

from dash import Dash, Input, Output, dcc, html

app = Dash(__name__)

server = app.server

app.layout = html.Div(
    [
        html.H2("Hello World"),
        dcc.Dropdown(["LA", "NYC", "MTL"], "LA", id="dropdown"),
        html.Div(id="display_value"),
    ]
)


@app.callback(Output("display_value", "children"), [Input("dropdown", "value")])
def display_value(value):
    return f"You have selected {value}"


if __name__ == "__main__":
    app.run_server(debug=True)
