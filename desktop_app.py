import tkinter as tk
from tkinter import ttk, messagebox
# Import the classes AND the API_KEY from music_app.py
from music_app import ApiClient, PlaylistManager, Track, Artist, API_KEY

class MusicDiscoveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Discovery")
        self.root.geometry("800x600")

        # *** THIS IS THE FIX ***
        # Pass the imported API_KEY when creating the ApiClient
        self.api_client = ApiClient(API_KEY)
        self.playlist_manager = PlaylistManager()

        # --- UI Setup ---
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Search Frame ---
        search_frame = ttk.LabelFrame(main_frame, text="Discover Music", padding="10")
        search_frame.pack(fill=tk.X, pady=5)
        search_frame.columnconfigure(1, weight=1)

        # Genre Search
        ttk.Label(search_frame, text="Search by Genre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.genre_entry = ttk.Entry(search_frame)
        self.genre_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(search_frame, text="Search Genre", command=self.search_by_genre).grid(row=0, column=2, padx=5, pady=5)

        # Artist Search
        ttk.Label(search_frame, text="Find Similar Artists:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.artist_entry = ttk.Entry(search_frame)
        self.artist_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(search_frame, text="Find Similar", command=self.find_similar_artists).grid(row=1, column=2, padx=5, pady=5)

        # --- Results Frame ---
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.results_tree = ttk.Treeview(results_frame, columns=("Type", "Name", "Details"), show="headings")
        self.results_tree.heading("Type", text="Type")
        self.results_tree.heading("Name", text="Name")
        self.results_tree.heading("Details", text="Artist / URL")
        self.results_tree.column("Type", width=80)
        self.results_tree.column("Name", width=250)
        self.results_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        results_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_tree.bind("<Double-1>", self.on_result_double_click)


        # --- Playlist Frame ---
        playlist_frame = ttk.LabelFrame(main_frame, text="Playlist", padding="10")
        playlist_frame.pack(fill=tk.X, pady=5)
        playlist_frame.columnconfigure(0, weight=1)
        
        # Playlist controls
        controls_frame = ttk.Frame(playlist_frame)
        controls_frame.pack(fill=tk.X)
        self.artist_playlist_entry = ttk.Entry(controls_frame, width=30)
        self.artist_playlist_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.artist_playlist_entry.insert(0, "Artist for Top 10 Playlist")

        ttk.Button(controls_frame, text="Build Top 10 by Artist", command=self.build_top_10).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(controls_frame, text="Save Playlist (CSV)", command=self.save_playlist).pack(side=tk.LEFT, padx=5, pady=5)


    def search_by_genre(self):
        genre = self.genre_entry.get()
        if not genre:
            messagebox.showwarning("Input Error", "Please enter a genre.")
            return
        tracks = self.api_client.get_top_tracks_by_genre(genre)
        self.populate_results(tracks)

    def find_similar_artists(self):
        artist = self.artist_entry.get()
        if not artist:
            messagebox.showwarning("Input Error", "Please enter an artist name.")
            return
        artists = self.api_client.get_similar_artists(artist)
        self.populate_results(artists)
        
    def build_top_10(self):
        artist = self.artist_playlist_entry.get()
        if not artist or artist == "Artist for Top 10 Playlist":
            messagebox.showwarning("Input Error", "Please enter an artist's name for the playlist.")
            return
        top_tracks = self.api_client.get_artist_top_tracks(artist)
        if top_tracks:
            self.playlist_manager.set_playlist(top_tracks)
            messagebox.showinfo("Success", f"Top 10 playlist for {artist} has been built and is ready to save.")
        else:
            messagebox.showerror("Error", f"Could not fetch Top 10 tracks for {artist}.")


    def populate_results(self, results):
        # Clear previous results
        for i in self.results_tree.get_children():
            self.results_tree.delete(i)
        
        # Store full objects for later use
        self.current_results = {}
        
        for item in results:
            item_id = self.results_tree.insert("", "end")
            self.current_results[item_id] = item # Store the object
            
            if isinstance(item, Track):
                self.results_tree.item(item_id, values=("Track", item.name, item.artist))
            elif isinstance(item, Artist):
                self.results_tree.item(item_id, values=("Artist", item.name, item.url))

    def on_result_double_click(self, event):
        selected_id = self.results_tree.focus()
        if not selected_id:
            return
            
        item = self.current_results.get(selected_id)
        if isinstance(item, Track):
            if messagebox.askyesno("Add to Playlist", f"Add '{item.name}' to your playlist?"):
                self.playlist_manager.add_track(item)
                messagebox.showinfo("Success", f"'{item.name}' added to playlist.")
        else:
             messagebox.showinfo("Info", "Double click a track to add it to the playlist.")
             
    def save_playlist(self):
        artist_name = self.artist_playlist_entry.get()
        if not artist_name or artist_name == "Artist for Top 10 Playlist":
             # Use a generic name if no artist is specified
            artist_name = "custom"

        success, message = self.playlist_manager.save_playlist_to_csv(artist_name)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicDiscoveryApp(root)
    root.mainloop()