import os
import gensim.downloader as api
from gensim.models import Word2Vec

# Load a substantial dataset from Gensim's API
dataset = api.load("text8")  # Replace with a larger dataset if needed

# Train the Word2Vec model
model = Word2Vec(sentences=dataset, vector_size=100, window=5, min_count=2, workers=4)

# Ensure the directory for model saving exists
model_dir = 'model'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Save the trained model's word vectors to a .bin file
model_save_path = os.path.join(model_dir, 'word2vec_training.bin')
model.wv.save_word2vec_format(model_save_path, binary=True)
print(f"Model saved to '{model_save_path}'")
