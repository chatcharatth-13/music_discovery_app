import tkinter as tk
from tkinter import messagebox, PanedWindow
# Import the new ttkbootstrap library for a modern look
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# The core logic file remains the same
from music_app import ApiClient, PlaylistManager, Track, Artist, API_KEY

class ModernMusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Music Discovery")
        self.root.geometry("900x700")

        # Initialize core components
        self.api_client = ApiClient(API_KEY)
        self.playlist_manager = PlaylistManager()

        # UI State
        self.current_results = {}

        self.create_widgets()

    def create_widgets(self):
        # --- Main Layout ---
        # A PanedWindow allows the user to resize the sections by dragging the separator
        main_paned_window = PanedWindow(self.root, orient=VERTICAL, sashrelief=RAISED, sashwidth=5)
        main_paned_window.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Top pane for searching and results
        top_frame = ttk.Frame(main_paned_window, padding=5)
        main_paned_window.add(top_frame, height=400)

        # Bottom pane for the playlist
        bottom_frame = ttk.Frame(main_paned_window, padding=5)
        main_paned_window.add(bottom_frame)

        # --- Search Controls (in top_frame) ---
        search_frame = ttk.LabelFrame(top_frame, text="🔍 Discover Music", padding=10)
        search_frame.pack(fill=X, pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)

        # Genre Search
        ttk.Label(search_frame, text="Genre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.genre_entry = ttk.Entry(search_frame)
        self.genre_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(search_frame, text="Search", command=self.search_by_genre, bootstyle="info").grid(row=0, column=2, padx=5, pady=5)

        # Artist Search
        ttk.Label(search_frame, text="Artist:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.artist_entry = ttk.Entry(search_frame)
        self.artist_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(search_frame, text="Find Similar", command=self.find_similar_artists, bootstyle="info").grid(row=1, column=2, padx=5, pady=5)

        # --- Results Treeview (in top_frame) ---
        results_container = ttk.LabelFrame(top_frame, text="🎶 Results", padding=10)
        results_container.pack(fill=BOTH, expand=True)

        self.results_tree = ttk.Treeview(results_container, columns=("Type", "Name", "Details"), show="headings")
        self.results_tree.heading("Type", text="Type")
        self.results_tree.heading("Name", text="Name")
        self.results_tree.heading("Details", text="Artist / Info")
        self.results_tree.column("Type", width=80, anchor=W)
        self.results_tree.column("Name", width=300, anchor=W)
        self.results_tree.pack(fill=BOTH, expand=True, side=LEFT)

        results_scrollbar = ttk.Scrollbar(results_container, orient=VERTICAL, command=self.results_tree.yview)
        results_scrollbar.pack(side=RIGHT, fill=Y)
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        # --- NEW: Right-click context menu for results ---
        self.results_menu = tk.Menu(self.root, tearoff=0)
        self.results_tree.bind("<Button-3>", self.show_results_context_menu)


        # --- Playlist View (in bottom_frame) ---
        playlist_container = ttk.LabelFrame(bottom_frame, text="📜 Your Playlist", padding=10)
        playlist_container.pack(fill=BOTH, expand=True)
        playlist_container.columnconfigure(0, weight=1)

        # Playlist Treeview
        self.playlist_tree = ttk.Treeview(playlist_container, columns=("Track", "Artist"), show="headings")
        self.playlist_tree.heading("Track", text="Track")
        self.playlist_tree.heading("Artist", text="Artist")
        self.playlist_tree.column("Track", anchor=W, width=350)
        self.playlist_tree.column("Artist", anchor=W, width=300)
        self.playlist_tree.pack(fill=BOTH, expand=True, side=LEFT)

        playlist_scrollbar = ttk.Scrollbar(playlist_container, orient=VERTICAL, command=self.playlist_tree.yview)
        playlist_scrollbar.pack(side=RIGHT, fill=Y)
        self.playlist_tree.configure(yscrollcommand=playlist_scrollbar.set)

        # Save button is now part of the playlist frame
        save_btn = ttk.Button(playlist_container, text="💾 Save Playlist (CSV)", command=self.save_playlist, bootstyle="success")
        save_btn.pack(side=BOTTOM, pady=(10, 0), fill=X)
        
        # --- Status Bar ---
        self.status_bar = ttk.Label(self.root, text="Welcome! Enter a search to begin.", anchor=W, padding=5)
        self.status_bar.pack(side=BOTTOM, fill=X)


    def update_status(self, message):
        self.status_bar.config(text=message)
        
    def search_by_genre(self):
        genre = self.genre_entry.get().strip()
        if not genre:
            messagebox.showwarning("Input Error", "Please enter a genre.")
            return
        self.update_status(f"Searching for tracks in genre: {genre}...")
        tracks = self.api_client.get_top_tracks_by_genre(genre)
        self.populate_results(tracks)
        self.update_status(f"Found {len(tracks)} tracks for genre: {genre}.")

    def find_similar_artists(self):
        artist = self.artist_entry.get().strip()
        if not artist:
            messagebox.showwarning("Input Error", "Please enter an artist name.")
            return
        self.update_status(f"Searching for artists similar to: {artist}...")
        artists = self.api_client.get_similar_artists(artist)
        self.populate_results(artists)
        self.update_status(f"Found {len(artists)} artists similar to: {artist}.")

    def populate_results(self, results):
        self.results_tree.delete(*self.results_tree.get_children())
        self.current_results.clear()
        
        for i, item in enumerate(results):
            item_id = str(i) # Use index as a simple ID
            self.current_results[item_id] = item 
            
            if isinstance(item, Track):
                self.results_tree.insert("", END, iid=item_id, values=("Track", item.name, item.artist))
            elif isinstance(item, Artist):
                self.results_tree.insert("", END, iid=item_id, values=("Artist", item.name, item.url))

    def show_results_context_menu(self, event):
        self.results_menu.delete(0, END) # Clear previous menu items
        selected_id = self.results_tree.identify_row(event.y)
        
        if selected_id:
            self.results_tree.selection_set(selected_id)
            item = self.current_results.get(selected_id)
            
            if isinstance(item, Track):
                self.results_menu.add_command(label=f"Add '{item.name}' to Playlist", command=lambda: self.add_track_to_playlist(item))
            elif isinstance(item, Artist):
                self.results_menu.add_command(label=f"Build Top 10 for '{item.name}'", command=lambda: self.build_top_10(item.name))
            
            self.results_menu.post(event.x_root, event.y_root)
            
    def add_track_to_playlist(self, track):
        self.playlist_manager.add_track(track)
        self.update_playlist_view()
        self.update_status(f"Added '{track.name}' to playlist.")

    def update_playlist_view(self):
        self.playlist_tree.delete(*self.playlist_tree.get_children())
        for track in self.playlist_manager.get_playlist():
            self.playlist_tree.insert("", END, values=(track.name, track.artist))

    def build_top_10(self, artist_name):
        self.update_status(f"Building Top 10 for {artist_name}...")
        top_tracks = self.api_client.get_artist_top_tracks(artist_name)
        if top_tracks:
            self.playlist_manager.set_playlist(top_tracks)
            self.update_playlist_view()
            self.update_status(f"Successfully built Top 10 playlist for {artist_name}.")
        else:
            messagebox.showerror("Error", f"Could not fetch Top 10 tracks for {artist_name}.")
            self.update_status("Error fetching Top 10.")
             
    def save_playlist(self):
        playlist = self.playlist_manager.get_playlist()
        if not playlist:
            messagebox.showwarning("Empty Playlist", "Your playlist is empty. Add some tracks before saving.")
            return

        # Let's try to get an artist name from the playlist for a smart filename
        artist_name = playlist[0].artist if playlist else "custom"
        
        success, message = self.playlist_manager.save_playlist_to_csv(artist_name)
        if success:
            messagebox.showinfo("Success", message)
            self.update_status("Playlist saved successfully!")
        else:
            messagebox.showerror("Error", message)
            self.update_status("Failed to save playlist.")

if __name__ == "__main__":
    # The 'darkly' theme is a nice modern dark theme.
    # Other options: 'lumen', 'superhero', 'cyborg'
    root = ttk.Window(themename="darkly")
    app = ModernMusicApp(root)
    root.mainloop()

