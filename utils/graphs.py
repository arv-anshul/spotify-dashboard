""" Makes some useful graphsfor Spotify Dashboard Web-App """

# --- Imports ---
import streamlit as st
import plotly.express as px

from utils.utils import playlist_summary_df, album_summary_df


def playlists_premise():
    """ Plotly graph to show the playlists premise. """
    fig = px.scatter(playlist_summary_df(), x='noOfTracks', y='hrsPlayed',
                     size='noOfTracks', color='playlistName')
    st.plotly_chart(fig, use_container_width=True)


def albums_premise():
    """ Plotly graph to show the playlists premise. """
    fig = px.scatter(data_frame=album_summary_df(), x='noOfTracks', y='minPlayed',
                     size='noOfTracks', color='albumName')
    st.plotly_chart(fig, use_container_width=True)
