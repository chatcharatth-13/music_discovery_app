🎵 Music Discovery App 🎵
Welcome to the Music Discovery App, your personal DJ for finding new tunes! 🎧 This project, built for a university final, uses the power of Python and the Last.fm API to help you explore the vast world of music.

Whether you prefer a classic desktop app or a slick web interface, we've got you covered. Let's get this party started!

✨ Features ✨
🔍 Genre Search: Feeling a certain vibe? Find the top tracks for any genre, from 80s synthwave to acoustic rock.

🤝 Artist Connect: Discover artists similar to your favorites. If you like Queen, you might just find your next obsession!

🎶 Top 10 Playlists: Instantly generate a "Top 10 Hits" playlist for any artist and export it to a CSV file.

💻 Dual Interfaces: Use the simple and speedy desktop app or the modern web app—the choice is yours!

🚀 Getting Started: Your First Quest!
Before you can discover music, you need the magic key. Here’s how to get it.

Get Your API Key:

Head over to the Last.fm API creation page.

Fill out the form (you can call the app anything you like!).

Last.fm will grant you an API Key. Copy this long string of text.

Activate the App:

Open the music_app.py file in a text editor.

Find this line at the top: API_KEY = "YOUR_API_KEY"

Replace "YOUR_API_KEY" with the key you just copied.

Save the file.

That's it! Your app is now connected to the music universe.

🗺️ Choose Your Adventure! 🗺️
You have two paths to choose from. Pick your favorite or try both!

Path 1: The Classic Desktop App 🖥️
Run a native application directly on your computer.

Open Your Terminal:

Launch Command Prompt (Windows) or Terminal (macOS/Linux).

Navigate to the Folder:

Use the cd command to move into your project directory.

# Example:
cd Desktop/music-discovery-app

Install the Tools:

Make sure you have the requests library installed. If not, run this command once:

pip install requests

Launch the App!

Run the following command to start the application.

python desktop_app.py

The application window should pop up on your screen, ready for action!

Path 2: The Modern Web App (with Docker!) 🐳
Serve the web interface from a cool, self-contained Docker container.

Prerequisite: Make sure you have Docker Desktop installed and running on your machine.

Open Your Terminal:

Just like before, cd into your project directory.

Build the Magic Box (Image):

This command reads the Dockerfile and builds a container with a mini-web-server inside.

docker build -t music-app .

Run the Magic Box (Container):

This command starts the container and connects it to your computer's port 8080.

docker run -p 8080:8000 music-app

Open Your Browser:

Go to the following address in Chrome, Firefox, or any browser:

➡️ http://localhost:8080

The first time you open it, you'll need to paste your API key one last time. The app will save it in your browser for next time. Enjoy the web experience!

📂 What's in the Box? (Project Files)
music_app.py: The "brain" of the operation. Contains all the core logic and API communication.

desktop_app.py: The code for the classic desktop GUI.

index.html: The all-in-one file for the sleek web application.

Dockerfile & requirements.txt: The recipe and ingredients for our Docker magic box.

README.md: You're reading it! Your friendly guide to the project.
