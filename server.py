from flask import Flask, request, jsonify, send_from_directory, Response
import numpy as np
import gensim.models
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load Word2Vec embeddings
model = gensim.models.KeyedVectors.load_word2vec_format('question', binary=True)

app = Flask(__name__, static_folder='../client')
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["5 per minute"])

def convert_url_to_token(url):
    token = url.split('/')[-1].replace('_', ' ')  # Assumes URLs are in the format of Wikipedia titles
    return token

def token_to_url(token):
    # Placeholder: Implement according to how you want to handle URL display or retrieval
    return f"https://en.wikipedia.org/wiki/{token.replace(' ', '_')}"

@app.route('/', methods=['GET'])
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/find_path', methods=['POST'])
@limiter.limit("5/minute")
def find_path():
    try:
        data = request.get_json()
        start_page = data['start']
        finish_page = data['finish']
        path, logs, time, discovered = crawler.find_path(start_page, finish_page)
        return jsonify({'path': path, 'logs': logs, 'time': time, 'discovered': discovered})
    except crawler.TimeoutErrorWithLogs as e:
        return jsonify({'error': str(e), 'logs': e.logs, 'time': e.time, 'discovered': e.discovered}), 500

@app.route('/midpoint', methods=['POST'])
def find_midpoint():
    data = request.get_json()
    start_url = data['start']
    end_url = data['finish']
    try:
        start_vector = model[convert_url_to_token(start_url)]
        end_vector = model[convert_url_to_token(end_url)]
        midpoint_vector = (start_vector + end_vector) / 2
        closest_index = model.similar_by_vector(midpoint_vector, topn=1)[0][0]
        closest_url = token_to_url(closest_index)
        return jsonify({'midpoint_url': closest_url})
    except KeyError:
        return jsonify({'error': 'One or both URLs are invalid'}), 404

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/logs', methods=['GET'])
def stream_logs():
    def generate():
        for log in logs:
            yield f"data: {log}\n\n"
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)