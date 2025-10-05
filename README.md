# 🎵 Music Discovery Project (Desktop + Web)

Welcome to the Music Discovery App, a comprehensive application designed to help users explore new music through a powerful and intuitive interface. This project features two distinct user experiences: a modern desktop GUI and a feature-rich web application, both powered by the Last.fm API. The web app is enhanced with AI-powered playlist summaries using Google's Gemini AI and is deployed to the cloud via a full CI/CD pipeline.

Live Demo: https://music-discovery-app-aq3i.onrender.com/

## ✨ Key Features
# This application is packed with features designed for a seamless music discovery experience:
- Dual Interfaces: Choose between a polished Desktop App (built with Python/Tkinter) or a responsive Web App.
- Multi-faceted Search:
  - Discover tracks by searching for any Genre.
  - Find new artists by searching for artists Similar to your favorites.
- Dynamic Playlist Creation:
    - Automatically build a Top 10 Playlist for any artist.
    - Manually Add individual tracks from genre searches to create a custom playlist.

- ✨ AI-Powered Summaries: Utilizes the Google Gemini AI to generate creative, descriptive summaries of your custom playlists, describing their overall mood and vibe.
- Data Portability: Export any playlist you create to a .CSV file, correctly formatted for Excel.
- Automated CI/CD Pipeline: Integrates with GitHub Actions to automatically build and publish a new Docker image to the GitHub Container Registry (GHCR) on every push to the main branch.
- Cloud Deployed: The web application is live and publicly accessible, deployed on Render.

## 🛠️ Tech Stack & Architecture
# This project utilizes a modern stack to deliver a robust and feature-rich experience.
- Backend & Core Logic: Python, Object-Oriented Programming (OOP)
- Desktop GUI: Tkinter, ttkbootstrap for modern themes
- Web Frontend: HTML, Tailwind CSS, Vanilla JavaScript
- APIs: Last.fm (for music data), Google Gemini AI (for playlist summaries)
- DevOps: Docker, Docker Compose, GitHub Actions (CI/CD)
- Cloud Platform: Render

## 🚀 Getting Started

Follow these steps to configure the application before running it.

1. Get a Last.fm API Key
The application requires a Last.fm API key to function.

-   Navigate to **[https://www.last.fm/api/account/create](https://www.last.fm/api/account/create)**.
-   Fill out the application form to receive your personal **API Key**.

2. Configure the Project
- Open the music_app.py file.
- Locate the API_KEY variable at the top of the file.
- Replace the placeholder string "YOUR_API_KEY" with the key you obtained.

# In music_app.py
API_KEY = "ํYOUR API KEY" # <-- Paste your Last.fm key here

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
