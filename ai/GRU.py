import re

import dask.dataframe as dd
import numpy as np
import pandas as pd

from keras.models import Model
from keras.layers import Input, LSTM, Dense, GRU

raw = pd.read_table('/Users/minhmai/Downloads/train.txt', delimiter=' ', header=None)
raw.columns = ['word', 'pos', 'wsj']


def refactor_pos(x):
    # helps deal with imbalances between classes
    if x == '.':
        return 'stopper'
    elif x.startswith('V') or x.startswith('RB') or x == 'JJ':
        return 'verb/adverb/adjective'
    elif x in ['NS', 'NNS', 'NN']:
        return 'noun'
    elif x in ['IN', 'TO', 'DT']:
        return 'preposition'
    else:
        return 'other'

def preprocess_dataframe(data):
    regex = re.compile(r'[^.a-z0-9]')
    data['is_symbol'] = data.pos.apply(lambda x: True if regex.match(x) else False)
    data = data[((data.is_symbol == True) | (data.pos == '.'))]

    # refactor pos tagging
    data['pos'] = data.pos.apply(lambda x: refactor_pos(x))
    data = data[['word', 'pos']]
    data['word'] = data.word.apply(lambda x: x.lower())
    corpus = {k: v for k, v in zip(data['word'].unique(), range(data['word'].nunique()))}
    pos_corpus = {k: v for k, v in zip(data['pos'].unique(), range(1, data['pos'].nunique())) if v != 'stopper'}
    pos_corpus['stopper'] = 9
    data['word'] = data.word.apply(lambda x: corpus[x])
    data['pos'] = data.pos.apply(lambda x: pos_corpus[x])
    return corpus, pos_corpus, data

def determine_max_length(data):
    array = [0] + idx + [data.shape[0]]
    start = 0
    max_num = 0
    for i in array:
        val = i - start
        if val > max_num:
            max_num = val
        start = i
    return max_num

def create_sentence_vectors(data):
    idx = data.loc[data['pos'] == 9, :].index.values.tolist()
    words = np.empty([122, ])
    pos = np.empty([122, ])
    start = 0
    max_length = determine_max_length(data)
    for i in idx:
        _words = data.loc[start:i, 'word'].values
        _pos = data.loc[start:i, 'pos'].values
        start = i + 1
        words = np.vstack((words, np.hstack((_words, np.zeros(max_length - len(_words))))))
        pos = np.vstack((pos, np.hstack((_pos, np.zeros(max_length - len(_pos))))))
    return words, pos


corpus, pos_corpus, data = preprocess_dataframe(raw)
words, pos = create_sentence_vectors(data)

pos[0]
# array([4., 1., 3., 3., 1., 2., 1., 3., 3., 3., 2., 2., 1., 4., 1., 2., 3.,
#        2., 3., 1., 1., 2., 4., 4., 4., 1., 3., 4., 9., 0., 0., 0., 0., 0.,
#        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
#        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
#        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
#        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
#        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
#        0., 0., 0.])

words[3]
# array([52., 53., 54., 55., 56., 15., 48., 44., 57., 58., 59.,  2., 34.,
#        30., 60.,  7., 61., 62., 63., 43., 64.,  1., 65., 66., 67., 68.,
#        69., 70., 33.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#         0.,  0.,  0.,  0.,  0.])

# training models
batch_size = 64  # Batch size for training.
epochs = 5  # Number of epochs to train for.
latent_dim = 256  # Latent dimensionality of the encoding space.
num_samples = 10000  # Number of samples to train on.
num_tokens = determine_max_length(data)
max_length = determine_max_length(data)

encoder_inputs = Input(shape=(None, num_tokens))
encoder = GRU(latent_dim, return_state=True)
encoder_outputs, state_h = encoder(encoder_inputs)

decoder_inputs = Input(shape=(None, num_tokens))
decoder_gru = GRU(latent_dim, return_sequences=True)
decoder_outputs = decoder_gru(decoder_inputs, initial_state=state_h)
decoder_dense = Dense(num_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
model.fit(
    words,
    pos,
    batch_size=batch_size,
    epochs=epochs,
    validation_split=0.2
)
# ValueError: Error when checking model input: the list of Numpy arrays that you are passing to your model is not the size the model expected. Expected to see 2 array(s), but instead got the following list of 1 arrays: [array([[  0.,   1.,   1., ...,   0.,   0.,   0.],
#        [  0.,   1.,   2., ...,   0.,   0.,   0.],
#        [ 34.,  35.,   2., ...,   0.,   0.,   0.],
#        ...,
#        [699., 885., 886., ...,   0., ...