import re

import numpy as np
import pandas as pd

from keras.models import Model, Sequential
from keras.layers import Input, LSTM, GRU

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
    pos_corpus = {k: v for k, v in zip(data['pos'].unique(), range(data['pos'].nunique())) if v != 'stopper'}
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


def create_assets(data):
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


def create_nn_assets(words_data, word_corpus, pos_corpus):
    # ensures all vector length for sentences are the same length
    assert(len(set([len(d) for d in words_data])) == 1)
    sentence_length = len(words_data)
    max_sentence_length = len(words_data[0])
    max_word_length = len(str("{0:b}".format(len(word_corpus))))
    input_data = np.zeros(
        (
            sentence_length, # denotes sentence
            max_sentence_length, # denotes word position
            max_word_length # denotes actual word
        ),
        dtype='float32'
    )
    target_data = np.zeros(
        (
            sentence_length,
            max_sentence_length,
            len(pos_corpus),
        ),
    dtype='float32'
    )
    for i, (word, tag) in enumerate(zip(words_data, pos)):
        for t, char in enumerate(word):
            binary = "{0:b}".format(int(char)).zfill(max_word_length)
            input_data[i, t, :] = [i for i in binary]
        for t, char in enumerate(tag):
            target_data[i, t, int(char)] = 1.
    return input_data, target_data
    

# preprocessing data
corpus, pos_corpus, data = preprocess_dataframe(raw)
words, pos, idx = create_assets(data)
x, y = create_nn_assets(words, corpus, pos_corpus)
print('shape of x:', x.shape)
print('shape of y:', x.shape)

# shape of x: (8828, 122, 15)
# shape of y: (8828, 122, 15)

# actually training
batch_size = 64  # Batch size for training.
epochs = 2 # Number of epochs to train for.
latent_dim = 4  # Latent dimensionality of the encoding space.
sentence_length = len(words[0]) # length of the words in a sentence (time step)
num_outputs = len(pos_corpus)
output_shape = len(x[0][0]) # base 2 binary represented as an array for each number (input dimensino)

model = Sequential()
model.add(GRU(4, input_shape=(max_length, output_shape)))
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
model.fit(
    x,
    y,
    batch_size=batch_size,
    epochs=epochs,
    validation_split=0.2
)

# ValueError: Error when checking target: expected gru_22 to have 2 dimensions, but got array with shape (8828, 122, 4)


