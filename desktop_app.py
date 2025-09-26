import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from music_app import ApiClient, PlaylistManager, Track # Import our logic

class MusicDiscoveryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Discovery")
        self.geometry("800x600")

        # Initialize backend components
        try:
            self.api_client = ApiClient()
            self.playlist_manager = PlaylistManager()
        except ValueError as e:
            messagebox.showerror("Configuration Error", f"{e}\nPlease set your API key in music_app.py and restart the application.")
            self.destroy()
            return

        # Style configuration
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TLabel", padding=5, font=('Helvetica', 10))
        style.configure("TButton", padding=5, font=('Helvetica', 10, 'bold'))
        style.configure("TEntry", padding=5, font=('Helvetica', 10))
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'))
        style.configure("Treeview", rowheight=25, font=('Helvetica', 10))

        # Main layout
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Controls Frame ---
        controls_frame = ttk.LabelFrame(main_frame, text="Discover Music", padding="10")
        controls_frame.pack(fill=tk.X, expand=False)
        
        # Genre Search
        ttk.Label(controls_frame, text="Search by Genre:").grid(row=0, column=0, sticky="w")
        self.genre_entry = ttk.Entry(controls_frame, width=30)
        self.genre_entry.grid(row=0, column=1, padx=5, sticky="ew")
        self.genre_button = ttk.Button(controls_frame, text="Search Genre", command=self.search_by_genre)
        self.genre_button.grid(row=0, column=2, padx=5)

        # Similar Artist Search
        ttk.Label(controls_frame, text="Find Similar Artists:").grid(row=1, column=0, pady=5, sticky="w")
        self.artist_entry = ttk.Entry(controls_frame, width=30)
        self.artist_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.artist_button = ttk.Button(controls_frame, text="Find Similar", command=self.find_similar_artists)
        self.artist_button.grid(row=1, column=2, padx=5, pady=5)
        
        controls_frame.columnconfigure(1, weight=1)

        # --- Results Frame ---
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.results_tree = ttk.Treeview(results_frame, columns=('col1', 'col2'), show='headings')
        self.results_tree.heading('col1', text='Name / Track')
        self.results_tree.heading('col2', text='Artist')
        self.results_tree.pack(fill=tk.BOTH, expand=True)

        # --- Playlist Frame ---
        playlist_frame = ttk.LabelFrame(main_frame, text="Playlist", padding="10")
        playlist_frame.pack(fill=tk.X, expand=False)

        self.build_playlist_button = ttk.Button(playlist_frame, text="Build Top 10 by Artist", command=self.build_top_10_playlist)
        self.build_playlist_button.pack(side=tk.LEFT, padx=5)

        self.save_playlist_button = ttk.Button(playlist_frame, text="Save Playlist (CSV)", command=self.save_playlist)
        self.save_playlist_button.pack(side=tk.LEFT, padx=5)

        self.load_playlist_button = ttk.Button(playlist_frame, text="Load Playlist (CSV)", command=self.load_playlist)
        self.load_playlist_button.pack(side=tk.LEFT, padx=5)


    def clear_results(self):
        """Clears the results treeview."""
        for i in self.results_tree.get_children():
            self.results_tree.delete(i)

    def search_by_genre(self):
        """Handler for the 'Search Genre' button."""
        genre = self.genre_entry.get()
        if not genre:
            messagebox.showwarning("Input Error", "Please enter a genre.")
            return
        
        self.clear_results()
        self.results_tree.heading('col1', text='Track')
        self.results_tree.heading('col2', text='Artist')
        
        tracks = self.api_client.search_tracks_by_genre(genre)
        if tracks:
            for track in tracks:
                self.results_tree.insert('', 'end', values=(track.name, track.artist))
        else:
            messagebox.showinfo("No Results", f"No tracks found for genre '{genre}'.")

    def find_similar_artists(self):
        """Handler for the 'Find Similar' button."""
        artist_name = self.artist_entry.get()
        if not artist_name:
            messagebox.showwarning("Input Error", "Please enter an artist's name.")
            return
            
        self.clear_results()
        self.results_tree.heading('col1', text='Similar Artist')
        self.results_tree.heading('col2', text='Match %') # Last.fm API provides a 'match' score

        artists = self.api_client.get_similar_artists(artist_name)
        if artists:
            for artist in artists:
                self.results_tree.insert('', 'end', values=(artist.name, ""))
        else:
            messagebox.showinfo("No Results", f"No similar artists found for '{artist_name}'.")

    def build_top_10_playlist(self):
        """Prompts for an artist and builds their Top 10 playlist."""
        artist_name = simpledialog.askstring("Input", "Enter artist's name for Top 10 Playlist:", parent=self)
        if artist_name:
            playlist = self.playlist_manager.build_top_10_playlist(artist_name, self.api_client)
            self.clear_results()
            self.results_tree.heading('col1', text='Playlist Track')
            self.results_tree.heading('col2', text='Artist')
            if playlist:
                for track in playlist:
                    self.results_tree.insert('', 'end', values=(track.name, track.artist))
                messagebox.showinfo("Success", f"Top 10 playlist for {artist_name} has been created.")
            else:
                messagebox.showerror("Error", f"Could not create playlist for {artist_name}.")

    def save_playlist(self):
        """Saves the current playlist in the manager."""
        if not self.playlist_manager.playlist:
            messagebox.showwarning("Empty Playlist", "The playlist is empty. Build one first.")
            return
        self.playlist_manager.save_to_csv()
        messagebox.showinfo("Success", f"Playlist saved to {self.playlist_manager.filename}")

    def load_playlist(self):
        """Loads a playlist and displays it."""
        self.playlist_manager.load_from_csv()
        if self.playlist_manager.playlist:
            self.clear_results()
            self.results_tree.heading('col1', text='Playlist Track')
            self.results_tree.heading('col2', text='Artist')
            for track in self.playlist_manager.playlist:
                self.results_tree.insert('', 'end', values=(track.name, track.artist))
            messagebox.showinfo("Success", f"Playlist loaded from {self.playlist_manager.filename}")
        else:
            messagebox.showwarning("Load Failed", "Could not load a playlist. The file might be empty or missing.")

if __name__ == "__main__":
    app = MusicDiscoveryApp()
    app.mainloop()
