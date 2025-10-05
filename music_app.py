import requests
import csv
import os

# --- Configuration ---
# IMPORTANT: Replace with your own Last.fm API key
API_KEY = "c688dcd05e8146a8c075644126070340" # <-- Make sure to put your Last.fm key here
BASE_URL = "https://ws.audioscrobbler.com/2.0/"

# --- Data Models ---
class Track:
    """Represents a single music track."""
    def __init__(self, name, artist_name, url):
        self.name = name
        self.artist_name = artist_name
        self.url = url

    def __str__(self):
        return f'"{self.name}" by {self.artist_name}'

    def to_dict(self):
        return {"name": self.name, "artist": self.artist_name, "url": self.url}

class Artist:
    """Represents a single artist."""
    def __init__(self, name, match_score, url):
        self.name = name
        self.match_score = match_score
        self.url = url

    def __str__(self):
        return f'{self.name} (Match: {self.match_score}%)'

# --- API Client ---
class ApiClient:
    """Handles all communication with the Last.fm API."""
    def __init__(self, api_key):
        self.api_key = api_key

    def _make_request(self, params):
        """Internal helper to make a generic API request."""
        all_params = {
            'api_key': self.api_key,
            'format': 'json',
            **params
        }
        try:
            response = requests.get(BASE_URL, params=all_params)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def find_similar_artists(self, artist_name, limit=10):
        """Finds artists similar to the given artist name."""
        params = {'method': 'artist.getsimilar', 'artist': artist_name, 'limit': limit}
        return self._make_request(params)

    def get_top_tracks_by_artist(self, artist_name, limit=10):
        """Gets the top tracks for a given artist."""
        params = {'method': 'artist.gettoptracks', 'artist': artist_name, 'limit': limit}
        return self._make_request(params)

# --- Playlist Manager ---
class PlaylistManager:
    """Manages the creation and export of playlists."""
    def __init__(self):
        self.playlist = []

    def add_track(self, track):
        """Adds a single track to the playlist."""
        self.playlist.append(track)
        print(f"Added: {track}")

    def create_playlist_from_top_tracks(self, top_tracks_data):
        """Clears the current playlist and creates a new one from API data."""
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
        """Saves the current playlist to a CSV file."""
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
            print(f"Playlist successfully saved to {filename}")
            return True, os.path.abspath(filename)
        except IOError as e:
            print(f"Error saving file: {e}")
            return False, ""

