import requests
import csv
import os

# --- Configuration ---
# IMPORTANT: Replace with your own Last.fm API key
API_KEY = "c688dcd05e8146a8c075644126070340" # <-- PASTE YOUR KEY HERE
BASE_URL = "https://ws.audioscrobbler.com/2.0/"

# --- Data Models ---
class Track:
    def __init__(self, name, artist_name, url):
        self.name = name
        self.artist_name = artist_name
        self.url = url
    def __str__(self):
        return f'"{self.name}" by {self.artist_name}'
    def to_dict(self):
        return {"name": self.name, "artist": self.artist_name, "url": self.url}

class Artist:
    def __init__(self, name, match_score, url):
        self.name = name
        self.match_score = match_score
        self.url = url
    def __str__(self):
        return f'{self.name} (Match: {self.match_score}%)'

# --- API Client ---
class ApiClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def _make_request(self, params):
        all_params = {'api_key': self.api_key, 'format': 'json', **params}
        try:
            response = requests.get(BASE_URL, params=all_params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def find_similar_artists(self, artist_name, limit=20):
        params = {'method': 'artist.getsimilar', 'artist': artist_name, 'limit': limit}
        return self._make_request(params)
        
    def get_top_tracks_by_artist(self, artist_name, limit=10):
        params = {'method': 'artist.gettoptracks', 'artist': artist_name, 'limit': limit}
        return self._make_request(params)

    def get_top_tracks_by_genre(self, genre, limit=20):
        params = {'method': 'tag.gettoptracks', 'tag': genre, 'limit': limit}
        return self._make_request(params)

# --- Playlist Manager ---
class PlaylistManager:
    def __init__(self):
        self.playlist = []

    def add_track(self, track):
        self.playlist.append(track)
        print(f"Added: {track}")

    def create_playlist_from_top_tracks(self, top_tracks_data):
        self.playlist.clear()
        if top_tracks_data and 'toptracks' in top_tracks_data and 'track' in top_tracks_data['toptracks']:
            for track_data in top_tracks_data['toptracks']['track']:
                track = Track(
                    name=track_data['name'],
                    artist_name=track_data['artist']['name'],
                    url=track_data['url']
                )
                self.playlist.append(track)
        return self.playlist

    def save_playlist_to_csv(self):
        if not self.playlist:
            print("Playlist is empty. Nothing to save.")
            return False, ""
        artist_name = self.playlist[0].artist_name.replace(' ', '_').replace('/', '_')
        filename = f"playlist_{artist_name}.csv"
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['name', 'artist', 'url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                for track in self.playlist:
                    writer.writerow(track.to_dict())
            return True, os.path.abspath(filename)
        except IOError as e:
            print(f"Error saving file: {e}")
            return False, ""

