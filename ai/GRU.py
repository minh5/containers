import re

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
    del pos_corpus['stopper']
    return corpus, pos_corpus, data

def determine_max_length(data, idx):
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
    max_length = determine_max_length(data, idx)
    for i in idx:
        _words = data.loc[start:(i-1), 'word'].values
        _pos = data.loc[start:(i-1), 'pos'].values
        start = i + 1
        words = np.vstack((words, np.hstack((_words, np.zeros(max_length - len(_words))))))
        pos = np.vstack((pos, np.hstack((_pos, np.zeros(max_length - len(_pos))))))
    return words, pos, idx


corpus, pos_corpus, data = preprocess_dataframe(raw)
words, pos, idx = create_sentence_vectors(data)
max_length = determine_max_length(data, idx)
num_output_classes = len(pos_corpus)
num_input_classes = len(corpus)

encoder_input_data = np.zeros(
    (len(words), max_length, num_input_classes) + 1),
    dtype='float32')
decoder_input_data = np.zeros(
    (len(pos), max_length, num_output_classes + 1),
    dtype='float32')
decoder_target_data = np.zeros(
    (len(pos), max_length, num_output_classes + 1),
    dtype='float32')

try:
    for i, (word, tag) in enumerate(zip(words, pos)):
        for t, char in enumerate(word):
            encoder_input_data[i, t, int(char)] = 1.
        for t, char in enumerate(tag):
            # decoder_target_data is ahead of decoder_input_data by one timestep
            decoder_input_data[i, t, int(char)] = 1.
            if t > 0:
                # decoder_target_data will be ahead by one timestep
                # and will not include the start character.
                decoder_target_data[i, t - 1, int(char)] = 1.
except:
    import pdb; pdb.post_mortem()
    

# actually training
batch_size = 64  # Batch size for training.
epochs = 10  # Number of epochs to train for.
latent_dim = 256  # Latent dimensionality of the encoding space.

encoder_inputs = Input(shape=(max_length, num_input_classes + 1))
encoder = GRU(latent_dim, return_state=True)
encoder_outputs, state_h = encoder(encoder_inputs)

decoder_inputs = Input(shape=(max_length, num_output_classes + 1))
decoder_gru = GRU(latent_dim, return_sequences=True)
decoder_outputs = decoder_gru(decoder_inputs, initial_state=state_h)
decoder_dense = Dense(num_output_classes + 1, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
model.fit(
    [encoder_input_data, decoder_input_data],
    decoder_target_data,
    batch_size=batch_size,
    epochs=epochs,
    validation_split=0.2
)

