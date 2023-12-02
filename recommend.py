import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import dataset
import pandas as pd



class recommender:
    def __init__(self, playlist_link):
       # Retrieve your client ID and client secret from environment variables
        c_id = os.getenv("SPOTIFY_CLIENT_ID")
        c_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        c_uri = os.getenv("SPOTIFY_REDIRECT_URI") 
        scope = "playlist-read-private"
        cache_path = os.path.join(os.getcwd(), "token.txt")
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=c_id, 
                                                       client_secret=c_secret, 
                                                       redirect_uri="http://localhost/", 
                                                       cache_path=cache_path))
        if "open.spotify.com/playlist/" in playlist_link:
            playlist_id = playlist_link.split("/playlist/")[-1].split('?')[0]
        else:
            return None #TODO: Change this in the future
        try:
            self.target = self.sp.playlist(playlist_id)
        except spotipy.SpotifyException as e:
            return None #TODO: Change this in the future 

    def get_recommendations(self) -> list:
        # Exits if playlist is empty
        tracks_data = []
        for item in self.target['tracks']['items']:
            # Get track
            track = item['track']
            # Get track ID
            track_id = track['id']
            # Get artist
            artist = self.sp.artist(track['artists'][0]['external_urls']['spotify'])
            # Get album
            album = self.sp.album(track["album"]["external_urls"]["spotify"])
            # Get year
            year = album['release_date'][:4] # type: ignore
            # Get genre of track
            if len(artist['genres']) != 0: # type: ignore
                genre = artist['genres'][0] # type: ignore
            else:
                genre = 'none'
            #Get audio features
            audio_features = self.sp.audio_features(track_id)[0] # type: ignore
            track_data = {
                'artist_name' : artist['name'], # type: ignore
                'track_id' : track_id,
                'popularity' : track['popularity'],
                'track_name' : track['name'],
                'genre' : genre,
                'danceability' : audio_features['danceability'],
                'energy' : audio_features['energy'],
                'key' : audio_features['key'],
                'loudness' : audio_features['loudness'],
                'mode' : audio_features['mode'],
                'speechiness' : audio_features['speechiness'],
                'acousticness' : audio_features['acousticness'],
                'instrumentalness' : audio_features['instrumentalness'],
                'liveness' : audio_features['liveness'],
                'valence' : audio_features['valence'],
                'tempo' : audio_features['tempo'],
            }
            tracks_data.append(track_data)
        topTen = dataset.generate_similarity_matrix('data/small_data.csv', tracks_data)
        
        new_tracks_info = []
        for index, row in topTen.iterrows():
            new_track = self.sp.track(row['track_id'])
            track_name = new_track['name']
            artist = new_track['artists'][0]['name']   
            cover_url = new_track['album']['images'][0]['url']
            sim = row['similarity']
            new_tracks_info.append((track_name, artist, cover_url, sim))
        return new_tracks_info
        
    
mainRuntime = recommender('https://open.spotify.com/playlist/3j9sYe8hKn3LnejbgDv4Eo?si=f5c3fcd44a0a4fca')
recommendations = mainRuntime.get_recommendations()
for i in recommendations:
    print(f'{i[0]} - {i[1]}: {i[3]}')

