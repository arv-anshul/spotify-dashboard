"""
A streamlit web app which accepts `spotify` provided data.
## This file only anlyse artists.
"""

# --- imports ---
from matplotlib import pyplot as plt
import streamlit as st
import numpy as np

from manage_data_file import stream_df


# --- Page config ---
st.set_page_config('Spotify Data Analysis', '🎙', 'wide')


# --- import files ---
# Listening history
df = stream_df()


# --- sidebar ---
with st.sidebar:
    st.title('Artist Data Analysis')
    individual_analysis_btn = st.radio('Select Individual Analysis',
                                       options=['Songs', 'Artists'])

# --- Hero Page ---
if individual_analysis_btn == 'Songs':
    unique_songs = (df['trackName'].value_counts() > 5)
    unique_songs = unique_songs.index[:unique_songs.sum()]
    song = st.selectbox(f'Select a song ({len(unique_songs)})*',
                        options=unique_songs.sort_values())
    artist = df.query('trackName==@song')['artistName'].values[0]

    song_df = df.query('trackName==@song')

    with st.expander(f'Summary of **{song}** song by **{artist}**', True):
        _, col1, col2, col3, _ = st.columns([1, 2, 2, 2, 1])
        with col1:
            st.metric('Times Listend', song_df.count()[0])
        with col2:
            date = song_df['endTime'].dt.strftime(r'%b %d %y').max()
            st.metric('First Listend On', date,
                      help='First date on song listend')
        with col3:
            st.metric('Minutes Listend',
                      round(song_df['msPlayed'].sum()/60000))


elif individual_analysis_btn == 'Artists':
    unique_artists = (df['artistName'].value_counts() > 5)
    unique_artists = unique_artists.index[:unique_artists.sum()]
    artist = st.selectbox(f'Select Artist ({len(unique_artists)})*',
                          options=unique_artists.sort_values())

    with st.expander(f'Summary of **{artist}**', True):
        col1, _, col2 = st.columns([2, 0.2, 2])
        with col1:
            st.subheader('Most times listened songs')
            fig, ax = plt.subplots()
            (df.query('artistName==@artist')
                ['trackName']
                .value_counts()[:8]
                .plot(kind='pie',
                      ax=ax,
                      figsize=(6, 6),
                      ylabel='',
                      autopct=r'%1.0f%%')
             )
            st.pyplot(fig)
        with col2:
            st.subheader('Most minutes listened songs')
            fig, ax = plt.subplots()
            (df.query('artistName==@artist')
                .groupby('trackName')
                .sum(numeric_only=True)
                .head(8)
                ['msPlayed']
                .plot(kind='pie',
                      ax=ax,
                      figsize=(6, 6),
                      ylabel='',
                      autopct=r'%1.0f%%')
             )
            st.pyplot(fig)

    display_df = (df.query('artistName==@artist')
                  .pivot_table('trackName', 'month', 'year', 'value_counts', fill_value=0))
    st.dataframe(display_df, use_container_width=True)
