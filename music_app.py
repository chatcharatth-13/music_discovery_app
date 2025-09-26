import requests
import csv
import os

# --- Configuration ---
# IMPORTANT: Replace with your own Last.fm API key
# You can get one here: https://www.last.fm/api/account/create
API_KEY = "c688dcd05e8146a8c075644126070340"
BASE_URL = "https://ws.audioscrobbler.com/2.0/"

# --- Core Classes (OOP Style) ---

class Track:
    """Represents a single music track."""
    def __init__(self, name, artist, url):
        self.name = name
        self.artist = artist
        self.url = url

    def __str__(self):
        return f'"{self.name}" by {self.artist}'

    def to_dict(self):
        """Serializes the track object to a dictionary."""
        return {
            'name': self.name,
            'artist': self.artist,
            'url': self.url
        }

class Artist:
    """Represents an artist."""
    def __init__(self, name, url, similar=None):
        self.name = name
        self.url = url
        self.similar = similar if similar else []

    def __str__(self):
        return self.name

class ApiClient:
    """A client to handle all communication with the Last.fm API."""

    def _make_request(self, params):
        """Internal method to make a request to the API."""
        if API_KEY == "YOUR_API_KEY":
            raise ValueError("API Key is not set in music_app.py. Please get one from Last.fm.")
        
        params['api_key'] = API_KEY
        params['format'] = 'json'
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Last.fm API: {e}")
            return None

    def search_tracks_by_genre(self, genre, limit=10):
        """Searches for tracks by a specific genre tag."""
        params = {
            'method': 'tag.gettoptracks',
            'tag': genre,
            'limit': limit
        }
        data = self._make_request(params)
        if not data or 'tracks' not in data or 'track' not in data['tracks']:
            return []
        
        tracks = []
        for item in data['tracks']['track']:
            track = Track(
                name=item['name'],
                artist=item['artist']['name'],
                url=item['url']
            )
            tracks.append(track)
        return tracks

    def get_similar_artists(self, artist_name, limit=5):
        """Finds artists similar to the given artist."""
        params = {
            'method': 'artist.getsimilar',
            'artist': artist_name,
            'limit': limit
        }
        data = self._make_request(params)
        if not data or 'similarartists' not in data or 'artist' not in data['similarartists']:
            return []

        artists = []
        for item in data['similarartists']['artist']:
            artist = Artist(name=item['name'], url=item['url'])
            artists.append(artist)
        return artists

    def get_artist_top_tracks(self, artist_name, limit=10):
        """Gets the most popular tracks for a given artist."""
        params = {
            'method': 'artist.gettoptracks',
            'artist': artist_name,
            'limit': limit
        }
        data = self._make_request(params)
        if not data or 'toptracks' not in data or 'track' not in data['toptracks']:
            return []

        tracks = []
        for item in data['toptracks']['track']:
            track = Track(
                name=item['name'],
                artist=item['artist']['name'],
                url=item['url']
            )
            tracks.append(track)
        return tracks

class PlaylistManager:
    """Manages creation, saving, and loading of playlists."""
    def __init__(self, filename="playlist.csv"):
        self.playlist = []
        self.filename = filename

    def add_track(self, track):
        """Adds a single track to the playlist."""
        self.playlist.append(track)
        print(f"Added: {track}")

    def build_top_10_playlist(self, artist_name, api_client):
        """Builds a Top 10 playlist for a given artist."""
        self.playlist.clear()
        print(f"Building Top 10 playlist for {artist_name}...")
        top_tracks = api_client.get_artist_top_tracks(artist_name, limit=10)
        if top_tracks:
            self.playlist = top_tracks
            print("Playlist created successfully.")
        else:
            print(f"Could not retrieve top tracks for {artist_name}.")
        return self.playlist

    def save_to_csv(self):
        """Saves the current playlist to a CSV file."""
        if not self.playlist:
            print("Playlist is empty. Nothing to save.")
            return
        
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'artist', 'url'])
                writer.writeheader()
                for track in self.playlist:
                    writer.writerow(track.to_dict())
            print(f"Playlist successfully saved to {self.filename}")
        except IOError as e:
            print(f"Error saving file: {e}")

    def load_from_csv(self):
        """Loads a playlist from a CSV file."""
        if not os.path.exists(self.filename):
            print("No playlist file found to load.")
            return

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.playlist.clear()
                for row in reader:
                    track = Track(name=row['name'], artist=row['artist'], url=row['url'])
                    self.playlist.append(track)
            print(f"Playlist loaded from {self.filename}")
        except (IOError, csv.Error) as e:
            print(f"Error loading file: {e}")

# --- Example Usage (for testing) ---
if __name__ == '__main__':
    # This block runs only when the script is executed directly
    # It won't run when this file is imported by other scripts.
    
    # 1. Initialize our tools
    client = ApiClient()
    playlist_manager = PlaylistManager()

    # 2. Feature: Search tracks by genre
    print("\n--- Searching for '80s' tracks ---")
    genre_tracks = client.search_tracks_by_genre('80s', 5)
    if genre_tracks:
        for t in genre_tracks:
            print(f"- {t}")
    else:
        print("Could not fetch tracks by genre.")
    
    # 3. Feature: Recommend similar artists
    artist = "Daft Punk"
    print(f"\n--- Finding artists similar to {artist} ---")
    similar_artists = client.get_similar_artists(artist)
    if similar_artists:
        for a in similar_artists:
            print(f"- {a}")
    else:
        print(f"Could not find similar artists for {artist}.")
    
    # 4. Feature: Build and export a "Top 10" playlist
    playlist_artist = "Queen"
    print(f"\n--- Building and saving a Top 10 playlist for {playlist_artist} ---")
    playlist_manager.build_top_10_playlist(playlist_artist, client)
    
    # Display the created playlist
    if playlist_manager.playlist:
        print("\nPlaylist content:")
        for t in playlist_manager.playlist:
            print(f"- {t}")
        # Save it
        playlist_manager.save_to_csv()
    
    # 5. Feature: Load a playlist from CSV
    print("\n--- Loading playlist from CSV ---")
    new_playlist_manager = PlaylistManager()
    new_playlist_manager.load_from_csv()
    if new_playlist_manager.playlist:
        print("\nLoaded playlist content:")
        for t in new_playlist_manager.playlist:
            print(f"- {t}")
