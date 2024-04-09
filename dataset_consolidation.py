import os
import pandas as pd

# FILES_DIRECTORY = 'Spotify data/2023-08-30'
FILES_DIRECTORY = 'Spotify data/2024-03-25'
COLS = {
    'ts': 'timestamp_play',
    'platform': 'platform',
    'ms_played': 'ms_played',
    'master_metadata_track_name': 'track_name',
    'master_metadata_album_artist_name': 'artist_name',
    'master_metadata_album_album_name': 'album_name',
    'spotify_track_uri': 'spotify_track_uri',
    'reason_start': 'reason_start',
    'reason_end': 'reason_end'
}

def read_files(directory: str) -> pd.DataFrame:
    dfs = []

    for filename in os.listdir(directory):
        if filename.endswith('.json') and 'Audio' in filename:
            filepath = os.path.join(directory, filename)
            df = pd.read_json(filepath)
            
            dfs.append(df)

    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df

df = read_files(FILES_DIRECTORY)
df = df[COLS.keys()]

df_only_tracks = df[
    (~df['master_metadata_track_name'].isna()) \
        & (~df['master_metadata_album_artist_name'].isna()) \
        & (~df['master_metadata_album_album_name'].isna())
]

df_only_tracks = df_only_tracks.rename(columns=COLS)

df_only_tracks.to_csv('consolidated_spotify_data_2024.csv', index=False)

print('Consolidated data saved!')
