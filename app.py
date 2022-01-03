import io
import base64

import dash
import pandas as pd
import matplotlib.pyplot as plt
import wordcloud
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from utils.decorators import all_args_none
from utils.readingfiles import parse_zip, get_streaming_history
from utils.lyrics_getter import get_lyrics

from plots.favourite_artist import favourite_artist
from plots.song_most_skipped import most_skipped
from plots.when_listening_dist import when_listening_dist
from plots.wordcloud_maker import create_wordcloud

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Upload(
        id="upload-data",
        children=html.Button("Upload zipped Spotify data"),
        accept=".zip",
        multiple=False,
    ),
    dcc.Store(id="streaming-history-storage"),
    html.Div(id="favourite-artist"),
    html.Br(),
    html.Div(id="most-skipped"),
    html.Br(),
    html.Div(id="when-listening"),
    html.Br(),
    html.Div(id="wordcloud"),
])


@app.callback(
    Output("streaming-history-storage", "data"),
    Input("upload-data", "contents"))
@all_args_none(default_val=None)
def update_streaming_history(file_contents):
    streaming_history = get_streaming_history(parse_zip(file_contents))
    return streaming_history.to_dict()


@app.callback(
    Output("favourite-artist", "children"),
    Input("streaming-history-storage", "data"))
@all_args_none(default_val=None)
def update_favourite_artist(streaming_history):
    streaming_history = pd.DataFrame(streaming_history)
    artist_name, img_url = favourite_artist(streaming_history)
    return [
        html.H4(f"Most listened to artist: {artist_name}"),
        html.Img(
            alt=f"Image of {artist_name}",
            src=img_url
        ),
    ]


@app.callback(
    Output("most-skipped", "children"),
    Input("streaming-history-storage", "data"))
@all_args_none(default_val=None)
def update_most_skipped(streaming_history):
    streaming_history = pd.DataFrame(streaming_history)
    fig = most_skipped(streaming_history)
    plt.figure(fig.number)
    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    data = base64.b64encode(img.getvalue()).decode("utf8")
    return html.Img(
        src=f"data:image/png;base64,{data}",
        alt="most skipped track"
    )


@app.callback(
    Output("when-listening", "children"),
    Input("streaming-history-storage", "data"))
@all_args_none(default_val=None)
def update_when_listening(streaming_history):
    streaming_history = pd.DataFrame(streaming_history)
    return dcc.Graph(figure=when_listening_dist(streaming_history))


@app.callback(
    Output("wordcloud", "children"),
    Input("streaming-history-storage", "data"))
@all_args_none(default_val=None)
def update_wordcloud(streaming_history):
    number_of_tracks = 10  # później mozna dodac zeby to sie wybieralo interaktywnie
    streaming_history = pd.DataFrame(streaming_history)
    wcloud: wordcloud.WordCloud = create_wordcloud(
        get_lyrics(
            streaming_history.tail(number_of_tracks)
        )
    )
    img = io.BytesIO()
    wcloud.to_image().save(img, format="png")
    data = base64.b64encode(img.getvalue()).decode("utf8")
    return html.Img(
        src=f"data:image/png;base64,{data}",
        alt="Wordcloud of words in lyrics"
    )


if __name__ == '__main__':
    app.run_server(debug=True)
