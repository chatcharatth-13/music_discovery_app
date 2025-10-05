import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from music_app import ApiClient, PlaylistManager, Track, Artist, API_KEY # Import the API_KEY

class MusicDiscoveryApp(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Music Discovery App")
        self.geometry("800x800")

        # --- Initialize Backend ---
        if not API_KEY or API_KEY == "YOUR_LASTFM_API_KEY_HERE":
             messagebox.showerror("API Key Error", "Please add your Last.fm API Key to the 'music_app.py' file.")
             self.destroy()
             return
        
        self.api_client = ApiClient(API_KEY) # <-- CRITICAL FIX: Pass the key here
        self.playlist_manager = PlaylistManager()

        self._create_widgets()

    def _create_widgets(self):
        main_pane = ttk.PanedWindow(self, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Top Pane: Search & Results ---
        top_frame = ttk.Frame(main_pane, padding=10)
        main_pane.add(top_frame, weight=3)

        # Search Controls
        search_controls_frame = ttk.LabelFrame(top_frame, text="Search Controls", padding=10)
        search_controls_frame.pack(fill=tk.X, pady=(0, 10))

        # Genre Search
        ttk.Label(search_controls_frame, text="Search by Genre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.genre_entry = ttk.Entry(search_controls_frame, width=30)
        self.genre_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.genre_search_btn = ttk.Button(search_controls_frame, text="Search Tracks", command=self.search_by_genre)
        self.genre_search_btn.grid(row=0, column=2, padx=5, pady=5)

        # Artist Search
        ttk.Label(search_controls_frame, text="Find Similar Artists:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.artist_entry = ttk.Entry(search_controls_frame, width=30)
        self.artist_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.artist_search_btn = ttk.Button(search_controls_frame, text="Find Artists", command=self.find_similar_artists)
        self.artist_search_btn.grid(row=1, column=2, padx=5, pady=5)
        
        search_controls_frame.columnconfigure(1, weight=1)

        # Results Treeview
        results_frame = ttk.LabelFrame(top_frame, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)

        self.results_tree = ttk.Treeview(results_frame, columns=("col1", "col2"), show="headings")
        self.results_tree.heading("col1", text="Name")
        self.results_tree.heading("col2", text="Artist / Match %")
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        self.results_tree.bind("<Button-3>", self.show_context_menu) # Right-click event

        # --- Bottom Pane: Playlist ---
        bottom_frame = ttk.Frame(main_pane, padding=10)
        main_pane.add(bottom_frame, weight=2)

        playlist_frame = ttk.LabelFrame(bottom_frame, text="Your Playlist", padding=10)
        playlist_frame.pack(fill=tk.BOTH, expand=True)

        self.playlist_tree = ttk.Treeview(playlist_frame, columns=("track", "artist"), show="headings")
        self.playlist_tree.heading("track", text="Track Name")
        self.playlist_tree.heading("artist", text="Artist")
        self.playlist_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.save_playlist_btn = ttk.Button(playlist_frame, text="Save Playlist to CSV", command=self.save_playlist)
        self.save_playlist_btn.pack(side=tk.RIGHT)

        # --- Status Bar ---
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    def search_by_genre(self):
        genre = self.genre_entry.get().strip()
        if not genre: return
        self.status_var.set(f"Searching for tracks in genre: {genre}...")
        self.update_idletasks()
        
        data = self.api_client.get_top_tracks_by_genre(genre)
        self.results_tree.delete(*self.results_tree.get_children())
        
        if data and data.get('tracks') and data['tracks'].get('track'):
            tracks = data['tracks']['track']
            for item in tracks:
                self.results_tree.insert("", "end", values=(item['name'], item['artist']['name']), tags=('track',))
            self.status_var.set(f"Found {len(tracks)} tracks for genre: {genre}")
        else:
            self.status_var.set(f"No tracks found for genre: {genre}")

    def find_similar_artists(self):
        artist = self.artist_entry.get().strip()
        if not artist: return
        self.status_var.set(f"Finding artists similar to {artist}...")
        self.update_idletasks()

        data = self.api_client.find_similar_artists(artist)
        self.results_tree.delete(*self.results_tree.get_children())

        if data and data.get('similarartists') and data['similarartists'].get('artist'):
            artists = data['similarartists']['artist']
            for item in artists:
                match_percent = f"{float(item['match'])*100:.2f}%"
                self.results_tree.insert("", "end", values=(item['name'], match_percent), tags=('artist',))
            self.status_var.set(f"Found {len(artists)} similar artists.")
        else:
            self.status_var.set(f"No similar artists found for {artist}.")
            
    def show_context_menu(self, event):
        item_id = self.results_tree.identify_row(event.y)
        if not item_id: return
        
        self.results_tree.selection_set(item_id)
        item = self.results_tree.item(item_id)
        item_tags = item.get('tags', [])
        
        context_menu = tk.Menu(self, tearoff=0)
        
        if 'track' in item_tags:
            track_name, artist_name = item['values']
            context_menu.add_command(label=f"Add '{track_name}' to Playlist", command=lambda: self.add_track_to_playlist(track_name, artist_name))
        
        if 'artist' in item_tags:
            artist_name, _ = item['values']
            context_menu.add_command(label=f"Build Top 10 for '{artist_name}'", command=lambda: self.build_top_10_playlist(artist_name))
        
        context_menu.post(event.x_root, event.y_root)

    def add_track_to_playlist(self, track_name, artist_name):
        track = Track(name=track_name, artist_name=artist_name, url="") # URL is optional for this action
        self.playlist_manager.add_track(track)
        self.update_playlist_view()
        self.status_var.set(f"Added '{track_name}' to playlist.")

    def build_top_10_playlist(self, artist_name):
        self.status_var.set(f"Building Top 10 for {artist_name}...")
        self.update_idletasks()
        data = self.api_client.get_top_tracks_by_artist(artist_name)
        self.playlist_manager.create_playlist_from_top_tracks(data)
        self.update_playlist_view()
        self.status_var.set(f"Playlist created for {artist_name}.")

    def update_playlist_view(self):
        self.playlist_tree.delete(*self.playlist_tree.get_children())
        for track in self.playlist_manager.playlist:
            self.playlist_tree.insert("", "end", values=(track.name, track.artist_name))

    def save_playlist(self):
        success, filepath = self.playlist_manager.save_playlist_to_csv()
        if success:
            messagebox.showinfo("Success", f"Playlist saved successfully!\n\nLocation: {filepath}")
        else:
            messagebox.showerror("Error", "Could not save the playlist. Is it empty?")

if __name__ == "__main__":
    # This check ensures the API_KEY is imported before the app runs
    if API_KEY and API_KEY != "YOUR_LASTFM_API_KEY_HERE":
        app = MusicDiscoveryApp()
        app.mainloop()
    else:
        # This will only happen if the user runs the file directly without setting the key
        # The check inside the app class handles the pop-up message
        print("API Key not found in music_app.py. Please set it before running.")

