# 🎵 Music Discovery Project (Desktop + Web)

A Python-based toolkit for music discovery, featuring both a desktop and web-based UI.
Built with Python and Tkinter for the desktop app, and HTML/JS for the web interface. Data is fetched from the Last.fm API. The web application is containerized with Docker for easy deployment.


## ✨ Features
- Artist Search: Find top tracks for any artist.
- Similar Artists: Get recommendations based on your favorite artists.
- Genre Exploration: Discover popular tracks within a specific genre.
- Playlist Export: Save an artist's top 10 tracks to a .csv file.

## 🚀 Getting Started

Follow these steps to configure the application before running it.

1. Get a Last.fm API Key
- The application requires a Last.fm API key to function.
    - Navigate to https://www.last.fm/api/account/create.
    - Fill out the application form to receive your personal API Key.

2. Configure the Project
    - Open the music_app.py file.
    - Locate the API_KEY variable at the top of the file.
    - Replace the placeholder string "YOUR_API_KEY" with the key you obtained.

# In music_app.py
API_KEY = "ํYOUR API KEY" # <-- Paste your key here

# 💻 How to Run
You can run the application in two different ways.

## 🖥️ Option 1: Run the Desktop App (Local)
This method runs the native tkinter GUI on your machine.
1. Install dependencies:

    `pip install requests`

2. Run the application:

    `python desktop_app.py`

## 🐳 Option 2: Run the Web App (Docker)
This method uses Docker to build and run the web interface in a container.
Prerequisite: Docker Desktop must be installed and running.

1. Build the Docker image:

    `docker build -t music-app .`

2. Run the Docker container:

    `docker run -p 8080:8000 music-app`

3. Access the application:

- Open your browser and navigate to `http://localhost:8080.`
- You will be prompted to enter your API key on first launch.
