import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import skipgrams
from tensorflow.keras import layers
from gensim.models import KeyedVectors

# Ensure reproducibility
SEED = 42
tf.random.set_seed(SEED)

# Data Preparation
sentence = "The quick brown fox jumps over the lazy dog"
tokens = sentence.lower().split()
vocab = {word: i for i, word in enumerate(set(tokens), 1)}
vocab_size = len(vocab) + 1

# Generate skip-grams
sequences = [vocab[word] for word in tokens]
pairs, labels = skipgrams(sequences, vocab_size, window_size=2, negative_samples=0)

# Define the Word2Vec Keras model
class Word2Vec(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim):
        super(Word2Vec, self).__init__()
        self.target_embedding = layers.Embedding(vocab_size, embedding_dim, input_length=1, name="w2v_embedding")
        self.context_embedding = layers.Embedding(vocab_size, embedding_dim, input_length=1)

    def call(self, pair):
        target, context = pair
        if len(target.shape) == 2:
            target = tf.squeeze(target, axis=1)
        word_emb = self.target_embedding(target)
        context_emb = self.context_embedding(context)
        return tf.tensordot(word_emb, context_emb, axes=[[1], [2]])

# Model Training
embedding_dim = 128
word2vec = Word2Vec(vocab_size, embedding_dim)
word2vec.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])
word2vec.fit([np.array(pairs, dtype="int32")[:, 0], np.array(pairs, dtype="int32")[:, 1]], np.array(labels, dtype="int32"), epochs=10, batch_size=1024)

# Save the embeddings - convert to a more manageable format such as KeyedVectors
weights = word2vec.get_layer('w2v_embedding').get_weights()[0]
word_vectors = KeyedVectors(vector_size=embedding_dim)
word_vectors.add_vectors(list(vocab.keys()), weights)

# Save the model in Word2Vec binary format (this is your .bin file)
bin_path = '/home/jooskim/cpsc406/WikipediaGame/server/word2vec_training.bin'
word_vectors.save_word2vec_format(bin_path, binary=True)
print(f"Model saved to {bin_path}")