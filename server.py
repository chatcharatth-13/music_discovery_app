import os
import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

# --- Environment Variables ---
LASTFM_API_KEY = os.environ.get('LASTFM_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# --- API Routes ---

@app.route('/api/lastfm', methods=['GET'])
def lastfm_proxy():
    if not LASTFM_API_KEY:
        return jsonify({"error": "Last.fm API key not configured on server"}), 500

    params = request.args.to_dict()
    params['api_key'] = LASTFM_API_KEY
    params['format'] = 'json'

    try:
        response = requests.get("https://ws.audioscrobbler.com/2.0/", params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error calling Last.fm API: {e}")
        return jsonify({"error": "Failed to fetch data from Last.fm"}), 502

@app.route('/api/openai', methods=['POST'])
def openai_proxy():
    if not OPENAI_API_KEY:
        return jsonify({"error": "OpenAI API key not configured on server"}), 500

    client_data = request.json
    
    # --- THIS IS THE NEW DEBUGGING LINE ---
    print(f"Received data from frontend: {client_data}") 
    # This will show us exactly what the browser sent.

    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": client_data['messages'], # Changed to use direct access for clearer error
            "temperature": 0.7,
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except (KeyError, TypeError) as e:
        print(f"Data format error from frontend: {e}")
        return jsonify({"error": "Invalid data format received from frontend."}), 400
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenAI API: {e}")
        return jsonify({"error": "Failed to fetch data from OpenAI"}), 502

# --- Serve Frontend ---
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
