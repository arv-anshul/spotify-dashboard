""" Manages the data files for this application. """


# --- Imports ---
from typing import Callable, Literal
import json
import os
import pandas as pd


# --- Making new data files from unorganized data files ---
# Making the StreamingHistory file
def make_stream_json() -> None:
    # Changing directory
    os.chdir('./data_files/unorganized_data')

    streams_files = [
        file for file in sorted(os.listdir()) if file.startswith('StreamingHistory')]

    if len(streams_files) > 1:
        stream_df = pd.DataFrame()
        for fname in streams_files:
            df = pd.read_json(fname)

            # Concatenate the streaming history files
            stream_df = pd.concat([stream_df, df])

        stream_df['endTime'] = pd.to_datetime(stream_df['endTime'])
        stream_df['trackName'] = (stream_df['trackName']
                                  .str.replace(r'\(.+|\[.+', '', regex=True)
                                  .str.replace(r' feat\. .*', '', regex=True)
                                  .str.replace(r'-.*', '', regex=True)
                                  .str.strip())
        stream_df['month'] = stream_df['endTime'].dt.month_name()
        stream_df['year'] = stream_df['endTime'].dt.year
        stream_df.reset_index(drop=True, inplace=True)

        # Export updated file
        stream_df.to_json('../lis-his.json', orient='index', indent=2,
                          date_format='iso', date_unit='s')


# Making the Playlist file
def update_playlist_json() -> None:
    # Changing directory
    os.chdir('./data_files/unorganized_data')

    playlist_files = [
        file for file in sorted(os.listdir()) if file.startswith('Playlist')]

    if len(playlist_files) > 1:
        with open(playlist_files[0], 'r+') as f:
            file_data = json.load(f)
            for file in playlist_files[1:]:
                new_data = json.load(open(file, 'r'))

                # Append the new data
                for data in new_data['playlists']:
                    file_data['playlists'].append(data)

            # Dump the updated json data
            json.dump(file_data, open('../plist.json', 'w'), indent=2)


# --- Importing data files and organize it for later use ---
# ListeningHistory data
def stream_df() -> pd.DataFrame:
    """ Return the listening history data as DataFrame. """
    df = pd.read_json('data_files/ListeningHistory.json', orient='index')

    # Modifications
    df['endTime'] = pd.to_datetime(df['endTime'])

    # Drop 2023 rows
    drop_index = df.query('year==2023').index
    df.drop(index=drop_index, inplace=True)

    return df


def playlist_df() -> pd.DataFrame:
    """ Return the playlist data as DataFrame. """
    plist = pd.read_json('data_files/AllPlaylists.json')

    # --- Modifications ---
    # Normalizing the playlist data
    playlist_df = pd.json_normalize(data=plist['playlists'].to_list(),
                                    record_path='items',
                                    record_prefix='pl_',
                                    meta=['name'],
                                    meta_prefix='pl_')

    # Removing unnecessary columns
    playlist_df.drop(columns=[
        'pl_episode',
        'pl_localTrack',
        'pl_track',
        'pl_track.trackUri',
        'pl_episode.episodeName',
        'pl_episode.showName',
        'pl_episode.episodeUri'
    ], inplace=True)
    playlist_df.dropna(inplace=True)

    # Removing unnecessary texts form some columns
    for col in ['pl_track.trackName', 'pl_track.albumName']:
        playlist_df[col] = (playlist_df[col]
                            .str.replace(r'\(.+|\[.+', '', regex=True)
                            .str.replace(r' feat\. .*', '', regex=True)
                            .str.replace(r' - .*', '', regex=True)
                            .str.strip())

    # Rename the columns
    playlist_df.rename(columns={
        'pl_addedDate': 'addedDate',
        'pl_track.trackName': 'trackName',
        'pl_track.artistName': 'artistName',
        'pl_track.albumName': 'albumName',
        'pl_name': 'playlistName'
    }, inplace=True)

    # Datetime column
    playlist_df['addedDate'] = pd.to_datetime(playlist_df['addedDate'])

    return playlist_df


def joined_df(how: Literal['inner', 'outer'] = 'inner') -> pd.DataFrame:
    """ Return a joined/merged DataFrame of playlist_df and stream_df. """
    pl_df = playlist_df()
    pl_df.drop(columns=['artistName'], inplace=True)

    merge_df = pd.merge(stream_df(), pl_df, how=how, on='trackName')

    return merge_df


# Same function as lambda function
merge_df: Callable[[Literal['inner', 'outer']], pd.DataFrame] = lambda how: pd.merge(stream_df(),
                                                                                     playlist_df(),
                                                                                     how=how,
                                                                                     left_on='trackName',
                                                                                     right_on='pl_track.trackName')
