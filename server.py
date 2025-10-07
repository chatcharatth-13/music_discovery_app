import os
import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

# --- Environment Variables ---
# For security, API keys are loaded from environment variables, not hardcoded.
LASTFM_API_KEY = os.environ.get('LASTFM_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# --- API Routes (Our Proxy Endpoints) ---

@app.route('/api/lastfm', methods=['GET'])
def lastfm_proxy():
    """Proxies requests to the Last.fm API."""
    if not LASTFM_API_KEY:
        return jsonify({"error": "Last.fm API key not configured on server"}), 500

    params = request.args.to_dict()
    params['api_key'] = LASTFM_API_KEY
    params['format'] = 'json'

    try:
        response = requests.get("https://ws.audioscrobbler.com/2.0/", params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error calling Last.fm API: {e}")
        return jsonify({"error": "Failed to fetch data from Last.fm"}), 502 # Bad Gateway

@app.route('/api/openai', methods=['POST'])
def openai_proxy():
    """Proxies requests to the OpenAI API."""
    if not OPENAI_API_KEY:
        return jsonify({"error": "OpenAI API key not configured on server"}), 500

    client_data = request.json
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": client_data.get('messages'),
        "temperature": 0.7,
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenAI API: {e}")
        return jsonify({"error": "Failed to fetch data from OpenAI"}), 502

# --- Serve Frontend ---
@app.route('/')
def serve_index():
    """Serves the main index.html file."""
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
