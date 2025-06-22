import os
import time
import requests
from flask import Flask, Response, jsonify
from dotenv import load_dotenv
from threading import Lock

load_dotenv()

app = Flask(__name__)

UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
UNSPLASH_SECRET_KEY = os.getenv('UNSPLASH_SECRET_KEY')
CACHE_DURATION_SECONDS = max(600, int(os.getenv('CACHE_DURATION_SECONDS', 600)))

photo_cache = {}
cache_lock = Lock()

def get_photo_from_unsplash(theme):
    """Fetch a random photo from Unsplash API based on theme"""
    url = f"https://api.unsplash.com/photos/random"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {
        "query": theme,
        "orientation": "landscape"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        photo_url = data['urls']['full']
        
        photo_response = requests.get(photo_url)
        photo_response.raise_for_status()
        
        return photo_response.content, photo_response.headers.get('content-type', 'image/jpeg')
    except Exception as e:
        print(f"Error fetching photo from Unsplash: {e}")
        return None, None

@app.route('/random/<theme>')
def get_random_photo(theme):
    """Endpoint to get a random photo based on theme with caching"""
    current_time = time.time()
    
    with cache_lock:
        if theme in photo_cache:
            cached_photo = photo_cache[theme]
            age = current_time - cached_photo['timestamp']
            
            if age < CACHE_DURATION_SECONDS:
                print(f"Cache hit for theme '{theme}' (age: {age:.1f}s)")
                return Response(cached_photo['data'], mimetype=cached_photo['content_type'])
            else:
                print(f"Cache expired for theme '{theme}' (age: {age:.1f}s)")
    
    print(f"Fetching new photo for theme '{theme}'")
    photo_data, content_type = get_photo_from_unsplash(theme)
    
    if photo_data:
        with cache_lock:
            photo_cache[theme] = {
                'data': photo_data,
                'content_type': content_type,
                'timestamp': current_time
            }
        return Response(photo_data, mimetype=content_type)
    else:
        return jsonify({"error": "Failed to fetch photo"}), 500

@app.route('/')
def index():
    """Default route with usage instructions"""
    return "Please use /random/nature or any other theme to access content."

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "cache_duration": CACHE_DURATION_SECONDS})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
