import dash
from dash import dcc
from dash import html


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
])

if __name__ == '__main__':
    app.run_server(debug=True)
