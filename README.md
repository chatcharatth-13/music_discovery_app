# 🎵 Music Discovery AI (Secure Edition)

Welcome to **Music Discovery AI**, a comprehensive app designed to help users explore new music through a powerful and intuitive interface.  
It features **two user experiences** — a modern **Desktop GUI** and a **secure Web App**, both powered by the **Last.fm API** and enhanced with **AI-powered playlist summaries** using the OpenAI GPT API.

🌐 **Live Demo:** [music-discovery-app-aq3i.onrender.com](https://music-discovery-app-6fr7.onrender.com)

---

## ✨ Key Features

- **🎨 Dual Interfaces**
  - 🖥️ **Desktop App** (Python + Tkinter)
  - 🌐 **Web App** (HTML, Tailwind CSS, JavaScript)

- **🔒 Secure Backend Proxy**
  - Flask backend securely manages all API keys.
  - Prevents exposure of sensitive information to browsers.

- **🎧 Multi-Faceted Search**
  - Search tracks by **genre**
  - Discover **similar artists**
  - Build **Top 10 Playlists** automatically
  - Add or remove tracks manually
  - **Clear playlists** easily

- **🤖 AI-Powered Summaries**
  - Uses OpenAI GPT API to describe your playlist’s **mood**, **vibe**, and **energy**

- **📦 Data Portability**
  - Export playlists to `.CSV` with **full Thai language support**

- **⚙️ Automated CI/CD Pipeline**
  - GitHub Actions automatically builds and pushes Docker images to GHCR on every commit

- **☁️ Cloud Deployment**
  - Secure web app live on **Render**

---

## 🛠️ Tech Stack & Architecture

| Layer | Technology |
|-------|-------------|
| **Backend & Core Logic** | Python, Flask, OOP |
| **Desktop GUI** | Tkinter, ttkbootstrap |
| **Frontend** | HTML, Tailwind CSS, Vanilla JS |
| **APIs** | Last.fm, OpenAI GPT |
| **DevOps** | Docker, Gunicorn, GitHub Actions |
| **Cloud Platform** | Render |

---

## 🚀 Getting Started

Follow these steps to set up the project locally.

### 1️⃣ Obtain API Keys

#### 🔑 Last.fm API
1. Go to [Last.fm API Account Creation](https://www.last.fm/api/account/create)
2. Fill out the form and obtain your **API key**

#### 🔑 OpenAI API
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create an account and generate a **new API key**
3. (Optional) Add a payment method if required

---

## 💻 How to Run

You can run this project in **two ways** — as a desktop app or as a secure web app.

---

### 🖥️ Option 1: Run the Desktop App (Local)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

2. **Add API Key**
   Open `music_app.py` and paste your Last.fm API key:

   ```python
   API_KEY = "YOUR_LASTFM_API_KEY_HERE"
   ```

3. **Run the App**

   ```bash
   python desktop_app.py
   ```

---

### 🐳 Option 2: Run the Secure Web App (Local Development)

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**

   **Windows (PowerShell):**

   ```powershell
   $env:LASTFM_API_KEY="your_lastfm_api_key_here"
   $env:OPENAI_API_KEY="your_openai_api_key_here"
   ```

   **macOS/Linux (bash):**

   ```bash
   export LASTFM_API_KEY="your_lastfm_api_key_here"
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```

3. **Run Flask Backend**

   ```bash
   python server.py
   ```

4. **Open Browser**
   Navigate to:

   ```
   http://127.0.0.1:5000
   ```

---

## 🧠 AI Playlist Summaries

Using OpenAI’s GPT model, your playlist can be summarized with:

* Emotional tone & genre mix
* Descriptive vibe (e.g., “a moody blend of chillwave and indie pop”)
* Suggestions for similar artists or songs

---

## 🧩 Project Structure

```
music-discovery-app/
├── .github/
│   └── workflows/
│       └── docker-image.yml
├── .gitignore
├── desktop_app.py
├── Dockerfile
├── index.html
├── music_app.py
├── README.md
├── requirements.txt
└── server.py
```

---

## 🚢 CI/CD Pipeline Overview

✅ **GitHub Actions** — Builds & pushes Docker image to GHCR on every push

✅ **Render Deployment** — Automatically redeploys from GHCR

✅ **Environment Variables** securely stored in Render Dashboard

---

## 💬 Author

Chatcharat Thongsuepsai (Knight)
* **Self Grade**
    * API/DB Validation: 5
    * Code Base Structure: 5
    * Test Coverage (Mocking): 5
