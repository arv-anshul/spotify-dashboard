""" Module contains some other important functions for the Web-App """

# --- Imports ---
from typing import Literal
import pandas as pd
import numpy as np

from utils.manage_data_file import *


# --- Global Variables ---
main_df = joined_df()
playlist = playlist_df()


def playlist_summary_df():
    """ Like a summary of the playlists. """

    playlist_summary_df = pd.DataFrame()
    playlist_summary_df['playlistName'] = sorted(playlist['playlistName']
                                                 .unique())
    playlist_summary_df['hrsPlayed'] = np.round(np.array(main_df.groupby('playlistName')['msPlayed']
                                                .sum().sort_index().values) / 360000)
    playlist_summary_df['noOfTracks'] = (main_df.groupby('playlistName')['trackName'].nunique()
                                         .sort_index().values)
    playlist_summary_df['noOfAlbums'] = (main_df.groupby('playlistName')['albumName'].nunique()
                                         .sort_index().values)
    return playlist_summary_df


def album_summary_df():
    """ Like a summary of the top-albums. """

    album_summary_df = pd.DataFrame()
    album_summary_df['albumName'] = (main_df['albumName'].value_counts()
                                     [:20].sort_index().index.values)

    # This df contains only those alumbs that which isin album_summary_df
    album_df = (main_df[main_df['albumName']
                        .isin(album_summary_df['albumName'])])

    album_summary_df['noOfTracks'] = (album_df.groupby('albumName')['trackName']
                                      .nunique().sort_index().values)
    album_summary_df['minPlayed'] = np.round(np.array(album_df.groupby('albumName')['msPlayed']
                                                      .sum().sort_index().values) / 60000).astype('int')
    return album_summary_df


def get_name(data: str,
             belongs_to: Literal['trackName', 'artistName', 'albumName', 'playlistName'],
             to_get: Literal['trackName', 'artistName', 'albumName']):
    return str(main_df[main_df[belongs_to] == data]
               [to_get].value_counts().index.values[0])
