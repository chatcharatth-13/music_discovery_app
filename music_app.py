import requests
import csv

# --- Configuration ---
API_KEY = "YOUR API KEY" # Replace with your key
BASE_URL = "https://ws.audioscrobbler.com/2.0/"

# --- Object-Oriented Classes ---

class Track:
    """Represents a single music track."""
    def __init__(self, name, artist, url):
        self.name = name
        self.artist = artist
        self.url = url

    def __repr__(self):
        return f"Track(name='{self.name}', artist='{self.artist}')"

class Artist:
    """Represents an artist."""
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f"Artist(name='{self.name}')"

class ApiClient:
    """Handles all communication with the Last.fm API."""
    def __init__(self, api_key):
        self.api_key = api_key
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            raise ValueError("API Key is not set. Please add it to music_app.py")

    def _get(self, params):
        """Private method to handle GET requests to the API."""
        params['api_key'] = self.api_key
        params['format'] = 'json'
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Last.fm API: {e}")
            return None

    def get_top_tracks_by_genre(self, genre, limit=10):
        """Fetches top tracks for a given genre."""
        params = { 'method': 'tag.gettoptracks', 'tag': genre, 'limit': limit }
        data = self._get(params)
        if data and 'tracks' in data and 'track' in data['tracks']:
            tracks_data = data['tracks']['track']
            return [Track(t['name'], t['artist']['name'], t['url']) for t in tracks_data]
        return []

    def get_similar_artists(self, artist_name, limit=10):
        """Fetches artists similar to a given artist."""
        params = { 'method': 'artist.getsimilar', 'artist': artist_name, 'limit': limit }
        data = self._get(params)
        if data and 'similarartists' in data and 'artist' in data['similarartists']:
            artists_data = data['similarartists']['artist']
            return [Artist(a['name'], a['url']) for a in artists_data]
        return []

    def get_artist_top_tracks(self, artist_name, limit=10):
        """Fetches the top 10 tracks for a specific artist."""
        params = { 'method': 'artist.gettoptracks', 'artist': artist_name, 'limit': limit }
        data = self._get(params)
        if data and 'toptracks' in data and 'track' in data['toptracks']:
            tracks_data = data['toptracks']['track']
            return [Track(t['name'], t['artist']['name'], t['url']) for t in tracks_data]
        return []


class PlaylistManager:
    """Manages creation and storage of playlists."""
    def __init__(self):
        self.playlist = []

    def add_track(self, track):
        self.playlist.append(track)

    def set_playlist(self, tracks):
        self.playlist = tracks

    def clear_playlist(self):
        self.playlist = []

    def save_playlist_to_csv(self, filename="playlist.csv"):
        """Saves the current playlist to a CSV file using semicolons."""
        if not self.playlist:
            print("Playlist is empty. Nothing to save.")
            return False
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            # *** THIS IS THE ONLY LINE THAT CHANGED ***
            # Using delimiter=';' to match regional settings where comma is a decimal.
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['name', 'artist', 'url'])
            for track in self.playlist:
                writer.writerow([track.name, track.artist, track.url])
        return True

    def load_playlist_from_csv(self, filename):
        """Loads a playlist from a CSV file."""
        try:
            with open(filename, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.reader(f, delimiter=';') # Also need to read with semicolon
                next(reader)
                self.playlist = [Track(row[0], row[1], row[2]) for row in reader]
            return True
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return False
        except Exception as e:
            print(f"An error occurred while reading the CSV: {e}")
            return False

