import pandas as pd
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

track_id = 'spotify:track:5Pztwlnd8mwy5FYdPGflYl'

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials())

# Function to fetch album images and artist genres using track IDs


def get_track_details(track_id):
    track = spotify.track(track_id)
    artist = spotify.artist(track['artists'][0]['id'])
    
    album = track['album']

    # Check if there are genres (handle cases where it might be empty)
    artist_genre = artist['genres'][0] if artist['genres'] else None

    # Get album cover URL from the smallest available image size
    album_cover = album['images'][0]['url']

    return artist_genre, album_cover


df = pd.read_csv('consolidated_spotify_data_2024.csv')

# for idx, row in df.sample(10).iterrows():
#     track_uri = row.loc['spotify_track_uri']
#     artist_genre, album_image_uri = get_track_info(track_uri)

#     print('track:', row.loc['track_name'])
#     print('album:', row.loc['album_name'])
#     print('album_image_uri:', album_image_uri)
#     print('artist_genre:', artist_genre)

#     print()

df['artist_genre'] = df['spotify_track_uri'].apply(lambda uri: get_track_details(uri)[0])
df['album_cover_uri'] = df['spotify_track_uri'].apply(lambda uri: get_track_details(uri)[1])

df.to_csv('consolidated_spotify_data_2024-enriched.csv', index=False)

print('Enriched data saved!')
