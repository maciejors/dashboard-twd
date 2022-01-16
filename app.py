from datetime import datetime
import io
import base64

import dash
import pandas as pd
import matplotlib.pyplot as plt
import wordcloud
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from utils.decorators import all_args_none
from utils.readingfiles import parse_zip, get_streaming_history
from utils.lyrics_getter import get_lyrics

from plots.favourite_artist import favourite_artist
from plots.song_most_skipped import most_skipped
from plots.when_listening_dist import when_listening_dist
from plots.wordcloud_maker import create_wordcloud

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
)
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


# ========== FAVOURITE ARTIST ========== #


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


# ========== MOST SKIPPED TRACK ========== #


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
    return [
        html.Img(
            src=f"data:image/png;base64,{data}",
            alt="most skipped track"
        )
    ]


# ========== WHEN LISTENING DISTRIBUTION ========== #


@app.callback(
    Output("when-listening", "children"),
    Input("streaming-history-storage", "data"))
@all_args_none(default_val=None)
def update_when_listening(streaming_history):
    df = pd.DataFrame(streaming_history)
    dates = pd.to_datetime(df["endTime"], format="%Y-%m-%d %H:%M")
    min_date = dates.min()
    max_date = dates.max()
    return [
        dcc.Store(
            id="streaming-history-dates-filtered",
            data=streaming_history,
        ),
        dcc.DatePickerRange(
            id="when-listening-date-range",
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            initial_visible_month=max_date,
            start_date=min_date,
            end_date=max_date,
        ),
        dcc.Graph(
            id="when-listening-plot",
            figure=when_listening_dist(df),
        ),
    ]


@app.callback(
    Output("when-listening-plot", "figure"),
    Input("when-listening-date-range", "start_date"),
    Input("when-listening-date-range", "end_date"),
    State("streaming-history-storage", "data"))
def on_date_range_changed(start_date, end_date, streaming_history):
    df = pd.DataFrame(streaming_history)
    df["endTime"] = pd.to_datetime(df["endTime"], format="%Y-%m-%d %H:%M")
    df = df[(df["endTime"] > start_date) & (df["endTime"] < end_date)]
    return when_listening_dist(df)


# ========== WORD CLOUD ========== #


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
    return [
        dcc.Slider(
            min=5,
            max=20,
            marks={i: '{}'.format(i) for i in range(3, 21)},
            value=10,
        ),
        html.Img(
            src=f"data:image/png;base64,{data}",
            alt="Wordcloud of words in lyrics"
        )
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
