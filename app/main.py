import streamlit as st
import pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime as dt
import datetime
import altair as alt
import pytz

#########################################################################################################################

# SETUP

client = MongoClient(
    host='mongo:27017',
    serverSelectionTimeoutMS=3000
)

db = client.tweets
collection = db.tweet

#########################################################################################################################

# TITLE
st.markdown(
    """<link 
        rel='stylesheet' 
        href='https://use.fontawesome.com/releases/v5.8.1/css/all.css' 
        integrity='sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf' 
        crossorigin='anonymous'
    >""",
    unsafe_allow_html=True
)
st.markdown(
    '<h1><i class="fab fa-twitter"></i> Twitter Dashboard</h1>',
    unsafe_allow_html=True
)

#########################################################################################################################

# FUNCTIONS

def get_top_10_dataframe(df):
    df = df.drop(columns=["_id"])
    df = pd.DataFrame(df.pivot_table(index=['hashtag'], aggfunc='size'))
    df.columns = ['count']
    df = df.nlargest(10, 'count')
    df = pd.DataFrame([df.index, df["count"]]).transpose()
    df.columns = ["hashtag", "count"]
    return df

#########################################################################################################################

# SELECTOR

add_selectbox = st.sidebar.selectbox(
    "Data types",
    ("Main", "test")
)

#########################################################################################################################

if add_selectbox == "Main":
    # MAIN SHOW

    df = pd.DataFrame(list(collection.find({})))
    df = get_top_10_dataframe(df)

    st.markdown('<h1>Top 10 no filter</h1>', unsafe_allow_html=True)

    base = alt.Chart(df).mark_bar().encode(
     x=alt.X('hashtag', sort=None),
     y='count',
     color=alt.condition(
         alt.datum.count >= 1000,
         alt.value('orange'),
         alt.value('steelblue')
         )
    ).properties(
     width=750,
     height=400
    )

    st.write(base)

#########################################################################################################################

    df_between_11_and_12 = pd.DataFrame(list(collection.find({"datetime": {
            '$gte': dt(2021, 6, 25, 11),
            '$lt': dt(2021, 6, 25, 12)
        }})))
    df_between_11_and_12 = get_top_10_dataframe(df_between_11_and_12)

    st.markdown('<h1>Top 10 hashtags between 11am and 12am on friday</h1>', unsafe_allow_html=True)

    base = alt.Chart(df_between_11_and_12).mark_bar().encode(
     x=alt.X('hashtag', sort=None),
     y='count',
     color=alt.condition(
         alt.datum.count >= 1000,
         alt.value('orange'),
         alt.value('steelblue')
         )
    ).properties(
     width=750,
     height=400
    )

    st.write(base)

    
#########################################################################################################################

    df_greater_than_12 = pd.DataFrame(list(collection.find({"datetime": {
            '$gte': dt(2021, 6, 25, 12)
        }})))
    df_greater_than_12 = get_top_10_dataframe(df_greater_than_12)

    st.markdown('<h1>Top 10 hashtags after 12am on friday</h1>', unsafe_allow_html=True)

    base = alt.Chart(df_greater_than_12).mark_bar().encode(
     x=alt.X('hashtag', sort=None),
     y='count',
     color=alt.condition(
         alt.datum.count >= 1000,
         alt.value('orange'),
         alt.value('steelblue')
         )
    ).properties(
     width=750,
     height=400
    )

    st.write(base)

#########################################################################################################################

    hours_removed = datetime.timedelta(hours = 1)
    today = dt.now(pytz.timezone('Europe/Paris'))
    new_datetime = today - hours_removed

    df_since_last_hour = pd.DataFrame(list(collection.find({"datetime": {
            '$gte': new_datetime
        }})))
    df_since_last_hour = get_top_10_dataframe(df_since_last_hour)

    st.markdown('<h1>Top 10 hashtags since last hour</h1>', unsafe_allow_html=True)

    base = alt.Chart(df_since_last_hour).mark_bar().encode(
     x=alt.X('hashtag', sort=None),
     y='count',
     color=alt.condition(
         alt.datum.count >= 1000,
         alt.value('orange'),
         alt.value('steelblue')
         )
    ).properties(
     width=750,
     height=400
    )
    
    st.write(base)

#########################################################################################################################

# if add_selectbox == "Correlations":
#     # DATAFRAME CORRELATIONS
#     correlations = pd.DataFrame(
#         list(spotify_db.correlations.find()),
#         columns=["base_col", "compared_col", "value"]
#     )

#     # DATAFRAME FILTER VALENCE
#     correlations_valence = pd.DataFrame(
#         correlations[correlations["base_col"] == "valence"],
#         columns=["value", "compared_col"]).set_index(['compared_col'])

#     # DATAFRAME FILTER DANCEABILITY
#     correlations_danceability = pd.DataFrame(
#         correlations[correlations["base_col"] == "danceability"],
#         columns=["value", "compared_col"]).set_index(['compared_col'])

#     # VIEW VALENCE
#     st.write("Correlation valence")
#     st.bar_chart(data=correlations_valence)

#     # VIEW DANCEABILITY
#     st.write("Correlation danceability")
#     st.bar_chart(data=correlations_danceability)

# #########################################################################################################################

# if add_selectbox == "Songs":

#     # DATAFRAME FILTER SONGS PER DURATION
#     songs_per_duration = pd.DataFrame({
#         "minutes": ["1min", "2min", "3min", "6min", "9min"],
#         "number of songs": [
#             spotify_db.songs.find(
#                 {"duration_ms": {"$gte": 60000, "$lt": 120000}}
#             ).count(),
#             spotify_db.songs.find(
#                 {"duration_ms": {"$gte": 120000, "$lt": 180000}}
#             ).count(),
#             spotify_db.songs.find(
#                 {"duration_ms": {"$gte": 180000, "$lt": 360000}}
#             ).count(),
#             spotify_db.songs.find(
#                 {"duration_ms": {"$gte": 360000, "$lt": 540000}}
#             ).count(),
#             spotify_db.songs.find(
#                 {"duration_ms": {"$gte": 540000}}
#             ).count(),
#         ]
#     }).set_index('minutes')

#     # VIEW SONGS PER DURATION
#     st.write("Song per duration")
#     st.area_chart(data=songs_per_duration)

# #########################################################################################################################

# if add_selectbox == "Genres":

#     # DATAFRAME FILTER SONGS PER GENRE
#     songs_per_genre = pd.DataFrame(
#         list(spotify_db.counts.find({"genre": {"$ne": "all"}})),
#         columns=["genre", "value"]
#     ).set_index('genre')

#     # DATAFRAME GENRE
#     genre = pd.DataFrame(list(spotify_db.genres.find()), columns=[
#         "genre", "tempo", "energy", "liveness", "speechiness", "valence",
#         "acousticness", "danceability", "loudness", "instrumentalness"
#     ])

#     # DATAFRAME FILTER DANCEABILITY
#     genre_danceability = genre[['genre', 'danceability']].set_index(['genre'])

#     # DATAFRAME FILTER VALENCE
#     genre_valence = genre[['genre', 'valence']].set_index(['genre'])

#     # DATAFRAME FILTER ENERGY
#     genre_energy = genre[['genre', 'energy']].set_index(['genre'])

#     # DATAFRAME FILTER LIVENESS
#     genre_liveness = genre[['genre', 'liveness']].set_index(['genre'])

#     # DATAFRAME FILTER SPEECHINESS
#     genre_speechiness = genre[['genre', 'speechiness']].set_index(['genre'])

#     # DATAFRAME FILTER ACOUSTICNESS
#     genre_acousticness = genre[['genre', 'acousticness']].set_index(['genre'])

#     # DATAFRAME FILTER LOUDNESS
#     genre_loudness = genre[['genre', 'loudness']].set_index(['genre'])

#     # DATAFRAME FILTER TEMPO
#     genre_tempo = genre[['genre', 'tempo']].set_index(['genre'])

#     # DATAFRAME FILTER INSTRUMENTALNESS
#     genre_instrumentalness = genre[['genre', 'instrumentalness']] \
#         .set_index(['genre'])

#     # VIEW SONGS PER GENRE
#     st.write("Songs per genre")
#     st.bar_chart(songs_per_genre)

#     # VIEW DANCEABILITY
#     st.write("Danceability per genre")
#     st.bar_chart(data=genre_danceability)

#     # VIEW VALENCE
#     st.write("Valence per genre")
#     st.bar_chart(data=genre_valence)

#     # VIEW ENERGY
#     st.write("Energy per genre")
#     st.bar_chart(data=genre_energy)

#     # VIEW INSTRUMENTALNESS
#     st.write("Instrumentalness per genre")
#     st.bar_chart(data=genre_instrumentalness)

#     # VIEW SPEECHINESS
#     st.write("Speechiness per genre")
#     st.bar_chart(data=genre_speechiness)

#     # VIEW ACOUSTICNESS
#     st.write("Acousticness per genre")
#     st.bar_chart(data=genre_acousticness)

#     # VIEW LOUDNESS
#     st.write("Loudness per genre")
#     st.bar_chart(data=genre_loudness)

#     # VIEW LIVENESS
#     st.write("Liveness per genre")
#     st.bar_chart(data=genre_liveness)

#     # VIEW TEMPO
#     st.write("Tempo per genre")
#     st.bar_chart(data=genre_tempo)
