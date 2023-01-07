""" Analysis on Spotify playlist data. """
import streamlit as st
import pandas as pd


# --- DataFrame ---
# Streaming history data
df = pd.read_json('data_files/ListeningHistory.json', orient='index')
# Playlist data
plist = pd.read_json('data_files/AllPlaylists.json')

# Normalizing the playlist data
playlist = pd.json_normalize(data=plist['playlists'].to_list(),
                             record_path='items',
                             record_prefix='pl_',
                             meta=['name'],
                             meta_prefix='pl_')

# Removing unnecessary rows and columns
playlist.drop(columns=[
    'pl_episode',
    'pl_localTrack',
    'pl_track',
    'pl_track.trackUri',
    'pl_episode.episodeName',
    'pl_episode.showName',
    'pl_episode.episodeUri'
], inplace=True)
playlist.dropna(inplace=True)

# Removing unnecessary texts
for col in ['pl_track.trackName', 'pl_track.albumName']:
    playlist[col] = (playlist[col]
                     .str.replace(r'\(.+|\[.+', '', regex=True)
                     .str.replace(r' feat\. .*', '', regex=True)
                     .str.replace(r' - .*', '', regex=True)
                     .str.strip())

# Adding some important columns
df['endTime'] = pd.to_datetime(df['endTime'])

# Joining the dfs for more analysis
ij_df = pd.merge(df, playlist, how='inner', left_on='trackName',
                 right_on='pl_track.trackName')
oj_df = pd.merge(df, playlist, how='outer', left_on='trackName',
                 right_on='pl_track.trackName')


# --- Global Variables ---
playlist_name = sorted(playlist['pl_name'].unique())
selected = ''


# --- sidebar section ---
with st.sidebar:
    st.title('Playlist Analysis')
    analysis_type = st.radio('Select Analysis Type',
                             options=['Overall', 'Individual'])
    if analysis_type == 'Individual':
        selected = str(st.selectbox(
            'Select Playlist', options=playlist_name))

# --- Hero Page ---
if selected != '':
    selected_df = playlist.query('pl_name==@selected')
    with st.expander(f'Analysis of **{selected} - {selected_df.shape[0]}**', True):
        st.dataframe(selected_df)
