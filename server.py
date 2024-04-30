from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import gensim.models
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import crawler  # Ensure this module is implemented correctly.
import logging

# Setting up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='../client')
CORS(app)  # Enable Cross-Origin Resource Sharing
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["5 per minute"])

# Define the path to the Word2Vec model
model_path = '/home/jooskim/cpsc406/WikipediaGame/server/word2vec_training.bin'
model = None  # Initialize model variable

# Attempt to load the Word2Vec model
try:
    model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {str(e)}")

# Serve the main HTML page
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

# Find path between two Wikipedia pages
@app.route('/find_path', methods=['POST'])
@limiter.limit("5/minute")
def find_path():
    if not model:
        return jsonify({'error': 'Word2Vec model is not loaded'}), 500
    
    data = request.get_json()
    start_page = data.get('start')
    finish_page = data.get('finish')
    
    if not start_page or not finish_page:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        path, logs, time, discovered = crawler.find_path(start_page, finish_page)
        return jsonify({'path': path, 'logs': logs, 'time': time, 'discovered': discovered})
    except Exception as e:
        logging.error(f"Error processing path: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Find midpoint based on Word2Vec similarities
@app.route('/midpoint', methods=['POST'])
def find_midpoint():
    if not model:
        return jsonify({'error': 'Word2Vec model is not loaded'}), 500
    
    data = request.get_json()
    try:
        start_vector = model[convert_url_to_token(data['start'])]
        end_vector = model[convert_url_to_token(data['finish'])]
        midpoint_vector = (start_vector + end_vector) / 2
        closest_index = model.similar_by_vector(midpoint_vector, topn=1)[0][0]
        closest_url = token_to_url(closest_index)
        return jsonify({'midpoint_url': closest_url})
    except KeyError:
        return jsonify({'error': 'One or both URLs are invalid'}), 404

def convert_url_to_token(url):
    """Converts a URL to a token suitable for querying the Word2Vec model."""
    return url.split('/')[-1].replace('_', ' ')

def token_to_url(token):
    """Converts a token back to a Wikipedia URL."""
    return f"https://en.wikipedia.org/wiki/{token.replace(' ', '_')}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)