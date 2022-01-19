import random

import let
import pandas as pd
import plotly.express as px
from zipfile import ZipFile
import utils
from Spotipy import get_sp
from utils.readingfiles import get_streaming_history

def popularity(df):
    '''
    :param df: Dataframe with spotify streaming history
    :return: plotly.express figure (histogram plot)
    '''
    songs = df
    sp = get_sp()
    print(songs)
    artists = []
    for song in songs.iterrows():
        artists.append(song[1].artistName)
    artists = list(set(artists))
    artists = random.sample(artists, round(len(artists)/10))
    popularity = []
    for artistName in artists:
        artist = sp.search(q=artistName, type="artist")
        if artist["artists"]["items"] == []:
            popularity.append(None)
            continue
        popularity.append(artist["artists"]["items"][0]["popularity"])
        if artist["artists"]["items"][0]["popularity"] == 1:
            print(artist["artists"]["items"][0])
    data = {'artist': artists,
            'popularity': popularity}
    df = pd.DataFrame(data, columns=['artist', 'popularity'])
    df = df.groupby("popularity").count().reset_index()
    fig = px.histogram(df, x="popularity", y="artist", nbins=100,
                       title="popularity distribution <br><sub>How mainstream are you?</sup>",
                       labels={"artist": "number of artists"})
    fig.update_layout(
        xaxis_title="number of artists",
        yaxis_title="popularity",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig


