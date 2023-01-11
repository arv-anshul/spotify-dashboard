""" Analysis on Spotify playlist data. """
import streamlit as st
from matplotlib import pyplot as plt
import plotly.express as px

from utils.manage_data_file import playlist_df, joined_df
from utils.utils import get_name
from utils.graphs import playlists_premise, albums_premise


# --- Page config ---
st.set_page_config('Playlist Analysis', '🗂️', 'wide')

# --- DataFrame ---
playlist = playlist_df()
main_df = joined_df()
outer_df = joined_df('outer')

# --- Global Variables ---
selected = ''
PLAYLIST_NAME = sorted(playlist['playlistName'].unique())


def show_graphs(data):
    if st.checkbox('Show graphs'):
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            (data['trackName'].value_counts()[:15]
             .plot(kind='bar', ax=ax,
                   title='Most played tracks in the playlist'))
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots()
            (data['artistName'].value_counts()[:15]
             .plot(kind='bar', ax=ax,
                   title='Most played artists in the playlist'))
            st.pyplot(fig)

        _, col, _ = st.columns([1, 2, 1])
        grp = data.groupby('trackName')
        with col:
            fig, ax = plt.subplots()
            (grp['msPlayed'].sum()
             .sort_values(ascending=False)[:8]
             .plot(kind='pie', ax=ax,
                        title='Minutes songs played',
                        ylabel='', autopct='%1.0f%%'))
            st.pyplot(fig)
        '---'


# --- sidebar section ---
with st.sidebar:
    st.title('Playlist Analysis')
    analysis_type = st.radio('Select Analysis Type',
                             options=['Overall', 'Individual', 'Albums'])
    if analysis_type == 'Individual':
        selected = str(st.selectbox(
            'Select Playlist', options=PLAYLIST_NAME))
    if analysis_type == 'Albums':
        selected = str(st.selectbox(
            'Select Album', options=(outer_df['albumName']
                                     .value_counts()[:-50].index)))

# --- Hero Page ---
if analysis_type == 'Overall':
    st.title(':blue[All playlists analysis]')

    _, col1, col2, col3, _ = st.columns([0.3, 1, 1, 1, 0.3])
    # 1st Row
    col1.metric('No.of **playlists made**', len(PLAYLIST_NAME))
    col2.metric('No.of **songs** added',
                playlist['trackName'].unique().shape[0])
    col3.metric('No.of **artists** added',
                playlist['artistName'].unique().shape[0])
    # 2nd Row
    col1.metric('Most played **playlist**',
                _x := main_df['playlistName'].value_counts().index.values[0],
                get_name(_x, 'playlistName', 'trackName'))
    col2.metric('Most played **song**',
                _x := main_df['trackName'].value_counts().index.values[0],
                get_name(_x, 'trackName', 'artistName'))
    col3.metric('Most played **artist**',
                _x := main_df['artistName'].value_counts().index.values[0],
                get_name(_x, 'artistName', 'trackName'))
    # 3rd Row
    col1.metric('Most played **album**',
                _x := main_df['albumName'].value_counts().index.values[0],
                get_name(_x, 'albumName', 'artistName'))

    # 4th Row
    playlists_premise()
    show_graphs(main_df)


if analysis_type == 'Individual':
    selected_df = main_df.query('playlistName==@selected')
    st.title(
        f'Analysis of **:red[{selected}] - {selected_df["trackName"].unique().shape[0]}**')

    _, col1, col2, col3, _ = st.columns([0.3, 1, 1, 1, .3])
    col1.metric('Most played song',
                _x := selected_df['trackName'].value_counts().index.values[0],
                get_name(_x, 'trackName', 'artistName'))
    col2.metric('Most played artist',
                _x := selected_df['artistName'].value_counts().index.values[0],
                get_name(_x, 'artistName', 'trackName'))
    col3.metric('Most played album',
                _x := selected_df['albumName'].value_counts().index.values[0],
                f"{get_name(_x, 'albumName', 'trackName')} - {get_name(_x, 'albumName', 'artistName')}")

    show_graphs(selected_df)

    # DataFrame of each playlist
    if st.checkbox('Show Playlist Contents'):
        st.table((playlist.query('playlistName==@selected')
                  .drop(columns=['addedDate', 'playlistName'])
                  .reset_index(drop=True)))


if analysis_type == 'Albums':
    f'# Analysis of :red[{selected}]'

    if st.checkbox('Show all album premise'):
        albums_premise()

    st.table(main_df.query('albumName==@selected')
             [['trackName', 'artistName', 'playlistName']].drop_duplicates().reset_index(drop=True))
