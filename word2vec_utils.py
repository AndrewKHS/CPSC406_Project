# Imports and Setup
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.sequence import skipgrams
import io

# Ensure reproducibility
SEED = 42
tf.random.set_seed(SEED)

# Data Preparation
sentence = "The quick brown fox jumps over the lazy dog"
tokens = sentence.lower().split()
vocab = {word: i for i, word in enumerate(set(tokens), 1)}  # unique index for each word, starting from 1
vocab_size = len(vocab) + 1  # including a padding index 0

# Skip-Gram Generation
window_size = 2
sequences = [vocab[word] for word in tokens]
pairs, labels = skipgrams(sequences, vocab_size, window_size=window_size, negative_samples=0)

# Model Definition
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
        dots = tf.einsum('be,bce->bc', word_emb, context_emb)
        return dots

# Model Training
embedding_dim = 128
word2vec = Word2Vec(vocab_size, embedding_dim)
word2vec.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])
pairs = np.array(pairs, dtype="int32")
labels = np.array(labels, dtype="int32")
word2vec.fit([pairs[:, 0], pairs[:, 1]], labels, epochs=10, batch_size=1024)

# Saving Embeddings
weights = word2vec.get_layer('w2v_embedding').get_weights()[0]
out_v = io.open('vectors.tsv', 'w', encoding='utf-8')
out_m = io.open('metadata.tsv', 'w', encoding='utf-8')
for index, word in enumerate(vocab):
    vec = weights[index]
    out_v.write('\t'.join([str(x) for x in vec]) + "\n")
    out_m.write(word + "\n")
out_v.close()
out_m.close()