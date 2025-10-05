import requests
import csv

# --- Configuration ---
# IMPORTANT: Make sure your key is here!
API_KEY = "c688dcd05e8146a8c075644126070340" # Replace with your key
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
    """Represents a single artist."""
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f"Artist(name='{self.name}')"

class ApiClient:
    """Handles all communication with the Last.fm API."""
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = BASE_URL

    def _get(self, params):
        """Private helper method for making GET requests."""
        params['api_key'] = self.api_key
        params['format'] = 'json'
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return None

    def get_top_tracks_by_genre(self, genre, limit=50):
        params = {'method': 'tag.gettoptracks', 'tag': genre, 'limit': limit}
        data = self._get(params)
        if data and 'tracks' in data and 'track' in data['tracks']:
            tracks = []
            for item in data['tracks']['track']:
                tracks.append(Track(name=item['name'], artist=item['artist']['name'], url=item['url']))
            return tracks
        return []

    def get_similar_artists(self, artist_name, limit=50):
        params = {'method': 'artist.getsimilar', 'artist': artist_name, 'limit': limit}
        data = self._get(params)
        if data and 'similarartists' in data and 'artist' in data['similarartists']:
            artists = []
            for item in data['similarartists']['artist']:
                artists.append(Artist(name=item['name'], url=item['url']))
            return artists
        return []
        
    def get_artist_top_tracks(self, artist, limit=10):
        params = {'method': 'artist.gettoptracks', 'artist': artist, 'limit': limit}
        data = self._get(params)
        if data and 'toptracks' in data and 'track' in data['toptracks']:
            return [Track(t['name'], t['artist']['name'], t['url']) for t in data['toptracks']['track']]
        return []

class PlaylistManager:
    """Manages a user's playlist."""
    def __init__(self):
        self.playlist = []

    def add_track(self, track):
        self.playlist.append(track)

    def get_playlist(self):
        return self.playlist

    def set_playlist(self, tracks):
        self.playlist = tracks
        
    def save_playlist_to_csv(self, artist_name):
        if not self.playlist:
            return False, "Playlist is empty."
        
        filename = f"playlist_{artist_name.replace(' ', '_')}.csv"
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                # Use a semicolon as the delimiter for better Excel compatibility
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['Track Name', 'Artist Name', 'URL'])
                for track in self.playlist:
                    writer.writerow([track.name, track.artist, track.url])
            return True, f"Playlist saved to {filename}"
        except IOError as e:
            return False, f"Error saving file: {e}"

