import os
import re

from lyricsgenius import Genius


def get_lyrics(streaming_history_df):
    lyrics = ""
    df = streaming_history_df.tail(200)
    for ind in df.index:
        lyrics += scrape_lyrics(df['artistName'][ind], df['trackName'][ind])
    return lyrics


def scrape_lyrics(artistname, songname):
    token = "iAWTneaCajreA1nrWBVBnaW_qYNu2g7i9FoOQ-33BffLnilwO_w4d8DuOPOl2jsb"
    genius = Genius(token)
    try:
        song = genius.search_song(songname, artistname)
    except TimeoutError:
        print("TIMEOUT ERROR OCCURED")
        return ''
    try:
        lyrics = song.lyrics.lower()
        # remove identifiers like chorus, verse, etc
        lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
        # remove empty lines
        lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
        lyrics = re.sub("embedshare urlcopyembedcopy", "", lyrics)
        lyrics = re.sub(r'\d+', ' ', lyrics)
        return lyrics
    except AttributeError:
        return ''
