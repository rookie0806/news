#-*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from konlpy.tag import Mecab
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from keras.preprocessing.sequence import pad_sequences
from keras.models import *
from keras.layers import *
import MeCab



def create_dictionary(unique_tokens, threshold):
    token_to_idx = dict()
    idx_to_token = dict()
    unique_token_keys = list(unique_tokens.keys())

    j = 0
    for i in range(len(unique_token_keys)):
        if unique_tokens[unique_token_keys[i]] > threshold:
            token_to_idx[unique_token_keys[i]] = j
            idx_to_token[j] = unique_token_keys[i]
            j += 1

    return token_to_idx, idx_to_token

def simple_rnn_model(gpu = False):
    model = Sequential()
    model.add(Embedding(len(token_to_idx), 50, input_length = X_train.shape[1]))
    if gpu:
        model.add(CuDNNGRU(50, return_sequences = True))
        model.add(CuDNNGRU(50))
    else:
        model.add(GRU(50, return_sequences = True))
        model.add(GRU(50))
    model.add(Dense(50, activation = "relu"))
    model.add(Dense(1, activation = "sigmoid"))
    model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ["acc"])
    return model

if __name__ == '__main__':
    df = pd.read_table("train_20181105-20181126.txt")
    mecab = Mecab()
    reviews = []
    labels = []
    all_tokens = []
    unique_tokens = dict()
    for i in range(len(df)):
        try:
            tokens = mecab.morphs(df["document"][i])
            reviews.append(tokens)
            labels.append(df["label"][i])

            all_tokens += tokens
            for t in tokens:
                if t in unique_tokens.keys():
                    unique_tokens[t] += 1
                else:
                    unique_tokens[t] = 1
        except:
            pass
    token_to_idx, idx_to_token = create_dictionary(unique_tokens, 100)
    print("Number of using token: ", len(token_to_idx), len(idx_to_token))

    
    i = 0
    for r in reviews:
        if len(r)!=0:
            i += 1

    print("Number of non-empty title: ", i)

    # Empty title label 지우기
    for i in range(len(reviews)):
        if len(reviews[i]) == 0:
            labels[i] = None

    reviews = [x for x in reviews if len(x) != 0]
    labels = [x for x in labels if x != None]
    print(len(reviews), len(labels))

    X_data = pad_sequences(reviews, maxlen = 30)
    y_data = np.asarray(labels)
    print("1")
    print("Number of constructed training set", len(X_data), len(y_data))
    X_train, y_train = train_test_split(np.asarray(X_data), np.asarray(y_data),test_size = 0.2)
    model = simple_rnn_model(False)
    model.summary()

    # ### 3. Model fitting and evaluation

    # Optimization
    hist = model.fit(X_train, y_train, validation_split = 0.2, epochs = 10, batch_size = 1000)

    # model.save('rnn_model.h5')

    # Test
    #print("Test Accuracy: ", model.evaluate(X_test, y_test)[1])

