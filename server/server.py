from flask import Flask, request, jsonify, send_from_directory
import gensim.models
import numpy as np
import logging

app = Flask(__name__, static_folder='client', static_url_path='')

model = None

def load_model():
    global model
    try:
        model = gensim.models.KeyedVectors.load_word2vec_format('model/word2vec_training.bin', binary=True)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {str(e)}")
        raise RuntimeError("Failed to load the Word2Vec model, cannot start the server.")

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/midpoint', methods=['POST'])
def find_midpoint():
    if model is None:
        load_model()

    data = request.get_json()
    start_key = data.get('start')
    end_key = data.get('end')

    if start_key in model.key_to_index and end_key in model.key_to_index:
        start_vector = model[start_key]
        end_vector = model[end_key]
        midpoint_vector = (start_vector + end_vector) / 2
        most_similar = model.similar_by_vector(midpoint_vector, topn=1)[0]
        wikipedia_url = f"https://en.wikipedia.org/wiki/{most_similar[0].replace(' ', '_')}"
        return jsonify({
            'midpoint_page': most_similar[0],
            'similarity': most_similar[1],
            'wikipedia_url': wikipedia_url
        })
    else:
        return jsonify({'error': 'One or both keywords not in model vocabulary'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
