import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from utils.readingfiles import *


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1(children="siema"),
    dcc.Upload(
        id="upload-data",
        children=html.Button("Upload zipped Spotify data"),
        accept=".zip",
        multiple=True,
    ),
    # jak już będziemy mieli wykresy to tutaj się wstawi ich id:
    # dcc.Graph(id="test-plot1"),
    # dcc.Graph(id="test-plot2"),
    # ...
])

# Wtedy te id wrzuci się tu:
#
# @app.callback(
#     Output("test-plot1", "figure"),
#     Input("upload-data", "contents"))
# def update_test_plot1(file_contents):
#     df = get_streaming_history(parse_zip(file_contents))
#     return test_plot1(df)
#
# @app.callback(
#     Output("test-plot2", "figure"),
#     Input("upload-data", "contents"))
# def update_test_plot2(file_contents):
#     df = get_streaming_history(parse_zip(file_contents))
#     return test_plot2(df)
#
# ...

if __name__ == '__main__':
    app.run_server(debug=True)
