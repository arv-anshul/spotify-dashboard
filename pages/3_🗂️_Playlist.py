""" Analysis on Spotify playlist data. """
from typing import Literal
import streamlit as st
from matplotlib import pyplot as plt

from manage_data_file import playlist_df, joined_df


# --- Page config ---
st.set_page_config('Playlist Analysis', '🗂️', 'wide')

# --- DataFrame ---
playlist = playlist_df()
main_df = joined_df()

# --- Global Variables ---
playlist_name = sorted(playlist['playlistName'].unique())
selected = ''


def get_name(data: str,
             belongs_to: Literal['trackName', 'artistName', 'albumName', 'playlistName'],
             to_get: Literal['trackName', 'artistName', 'albumName']):
    return str(main_df[main_df[belongs_to] == data]
               [to_get].value_counts().index.values[0])


# --- sidebar section ---
with st.sidebar:
    st.title('Playlist Analysis')
    analysis_type = st.radio('Select Analysis Type',
                             options=['Overall', 'Individual'])
    if analysis_type == 'Individual':
        selected = str(st.selectbox(
            'Select Playlist', options=playlist_name))

# --- Hero Page ---
if analysis_type == 'Overall':
    st.title(':blue[All playlists analysis]')

    _, col1, col2, col3, _ = st.columns([0.3, 1, 1, 1, 0.3])
    # 1st Row
    col1.metric('No.of **playlists made**', len(playlist_name))
    col2.metric('No.of **songs** added',
                playlist['trackName'].unique().shape[0])
    col3.metric('No.of **artists** added',
                playlist['artistName'].unique().shape[0])
    # 2nd Row
    col1.metric('Most played **playlist**',
                x := main_df['playlistName'].value_counts().index.values[0],
                get_name(x, 'playlistName', 'trackName'))
    col2.metric('Most played **song**',
                x := main_df['trackName'].value_counts().index.values[0],
                get_name(x, 'trackName', 'artistName'))
    col3.metric('Most played **artist**',
                x := main_df['artistName'].value_counts().index.values[0],
                get_name(x, 'artistName', 'trackName'))
    # 3rd Row
    col1.metric('Most played **album**',
                x := main_df['albumName'].value_counts().index.values[0],
                get_name(x, 'albumName', 'artistName'))

    # 4th Row
    if st.checkbox('Show graphs'):
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            (main_df['trackName'].value_counts()[:15]
             .plot(kind='bar', ax=ax,
                   title='Most played tracks in the playlist'))
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots()
            (main_df['artistName'].value_counts()[:15]
             .plot(kind='bar', ax=ax,
                   title='Most played artists in the playlist'))
            st.pyplot(fig)

        _, col, _ = st.columns([1, 2, 1])
        grp = main_df.groupby('trackName')
        with col:
            fig, ax = plt.subplots()
            (grp['msPlayed'].sum()
             .sort_values(ascending=False)[:8]
             .plot(kind='pie', ax=ax,
                        title='Minutes songs played',
                        ylabel='', autopct='%1.0f%%'))
            st.pyplot(fig)
        '---'


if selected != '':
    selected_df = playlist.query('playlistName==@selected')
    st.title(f'Analysis of **:red[{selected}] - {selected_df.shape[0]}**')
    st.dataframe(selected_df)
