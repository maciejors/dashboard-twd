from datetime import datetime

import pandas as pd
import plotly.express as px


def when_listening_dist(df: pd.DataFrame):
    """
    Returns a barplot showing distribution of when during a day music
    was played

    :param df: DataFrame with spotify streaming history
    :return: Plotly barplot
    """
    df = df.copy()
    # df["hour"] = df["endTime"].apply(
    #     lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M").hour)
    df["endTime"] = pd.to_datetime(df["endTime"], format="%Y-%m-%d %H:%M")
    df["hour"] = df["endTime"].apply(
        lambda date: date.hour)
    df = df[["hour", "artistName"]] \
        .groupby("hour") \
        .agg("count") \
        .reset_index() \
        .rename(columns={"artistName": "count"})
    # add missing hours
    for i in range(24):
        if i not in df["hour"].values:
            df = df.append({"hour": i, "count": 0}, ignore_index=True)
    df = df.sort_values("hour", ignore_index=True)
    # format the interval
    df["hour"] = df["hour"].astype(str)
    df = df.assign(hourInterval=lambda x: x["hour"] + ":00 - " + x["hour"] + ":59")[
        ["hourInterval", "count"]]
    return px.bar(
        data_frame=df,
        x="hourInterval",
        y="count",
        labels={
            "hourInterval": "Hour interval",
            "count": "Number of tracks listened to"
        }
    )
