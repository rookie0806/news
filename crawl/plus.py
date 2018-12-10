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
import psycopg2
import sys
from PIL import Image
import base64
import operator
import MeCab

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
#test_chojoong_20181126-20181203
def inserttodb(Office_name,Percentage,date,progress):
    conn_string = "host='localhost' dbname ='news' user='postgres' password='doongji0806'"
    #src = 'image/'+mnet+'.jpg'
    #f = open(src, 'rb')
    #filedata = f.read()
    #print(filedata)
    #filedata=(src)
    conn = psycopg2.connect(conn_string) 
    curs = conn.cursor()
    sql = """insert into news_NewsPaper("Office_name", "Percentage" , "date", "Progress") values (%s,%s,%s,%s)"""
    array2 = [(Office_name, Percentage, date, progress)]
    curs.executemany(sql, array2)
    #curs.execute(sql_string)
    conn.commit()
    conn.close() 

# ### 1. Construct data set
if __name__ == '__main__':
    test_set = ["test_set_20181106-20181113",
                "test_set_20181113-20181120",
                "test_set_20181120-20181127"]
    '''test_set = ["test_dongah_20181106-20181113",
                "test_kyounghyang_20181106-20181113",
                "test_chojoongdong_20181106-20181113",
                "test_hankyoungoh_20181106-20181113",
                "test_cho_20181106-20181113",
                "test_joong_20181106-20181113",
                "test_han_20181106-20181113",
                "test_oh_20181106-20181113"]'''
    name_set = ["동아일보","경향신문","[조중동]","[한경오]","조선일보","중앙일보","한겨례","오마이뉴스"]
    porgress_set = [False,True,False,True,False,False,True,True]
    for k in range(0,len(test_set)):
        news = name_set[k]
        test = test_set[k]
        date = test.split("_")[2]
        db_date = date.split("-")[1]
        df = pd.read_table("train_20180503-20181119") # training set (이전 기사들, 여러 신문)
        pp = pd.read_table(test) # test set (최근 기사, 하나의 신문)

        mecab = Mecab()

        # reviews : title이 tokenizee된 list가 원소
        # labels : reviews와 같은 index의 title의 label
        # _p : test set
        # all_tokens : training set 통해 test set의 판단 하려면 test set 의 토큰들이 같이 indexing 되어야함
        # unique_tokens : token의 개수 체크
        reviews = []
        reviews_p = []
        labels = []
        labels_p = []
        all_tokens = []
        unique_tokens = dict()

        # training set tokenize
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

        # test set tokenize
        for i in range(len(pp)):
            try:
                tokens = mecab.morphs(pp["document"][i])
                reviews_p.append(tokens)
                labels_p.append(pp["label"][i])

                all_tokens += tokens
                for t in tokens:
                    if t in unique_tokens.keys():
                        unique_tokens[t] += 1
                    else:
                        unique_tokens[t] = 1
            except:
                pass

        print("Number of news: ", len(reviews), len(labels))
        print("Number of tokens: ", len(all_tokens))
        print("Number of unique tokens: ", len(unique_tokens))

        # making token-idx, idx-token dictionary function
        # threshold 이상 등장한 token만 사용

        token_to_idx, idx_to_token = create_dictionary(unique_tokens, 100)
        print("Number of using token: ", len(token_to_idx), len(idx_to_token))

        # Using token으로만 title 재구성 & index로 title 배열 재구성
        for i in range(len(reviews)):
            for j in range(len(reviews[i])):
                if reviews[i][j] in token_to_idx.keys():
                    reviews[i][j] = token_to_idx[reviews[i][j]]
                else:
                    reviews[i][j] = None

            reviews[i] = [x for x in reviews[i] if x != None]

        for i in range(len(reviews_p)):
            for j in range(len(reviews_p[i])):
                if reviews_p[i][j] in token_to_idx.keys():
                    reviews_p[i][j] = token_to_idx[reviews_p[i][j]]
                else:
                    reviews_p[i][j] = None

            reviews_p[i] = [x for x in reviews_p[i] if x != None]

        i = 0
        for r in reviews:
            if len(r)!=0:
                i += 1

        print("Number of non-empty title: ", i)

        # Empty title label 지우기
        for i in range(len(reviews)):
            if len(reviews[i]) == 0:
                labels[i] = None

        for i in range(len(reviews_p)):
            if len(reviews_p[i]) == 0:
                labels_p[i] = None

        reviews = [x for x in reviews if len(x) != 0]
        labels = [x for x in labels if x != None]

        reviews_p = [x for x in reviews_p if len(x) != 0]
        labels_p = [x for x in labels_p if x != None]

        print(len(reviews), len(labels))

        # Construct data set with numpy
        X_data = pad_sequences(reviews, maxlen = 30)
        y_data = np.asarray(labels)

        X = pad_sequences(reviews_p, maxlen = 30)
        Y = np.asarray(labels_p)

        print("Number of constructed training set", len(X_data), len(y_data))
        print("Number of constructed test set", len(X), len(Y))

        # ### 2. Create model
        # - Model with two GRU layers (with 50 cells each)

        # Spliting training set & test set
        X_train, X_test, y_train, y_test = train_test_split(np.asarray(X_data), np.asarray(y_data),test_size = 0.2)
        print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

        # Define RNN model by keras
        

        model = simple_rnn_model(False)
        model.summary()

        # ### 3. Model fitting and evaluation

        # Optimization
        hist = model.fit(X_train, y_train, validation_split = 0.2, epochs = 10, batch_size = 1000)

        # model.save('rnn_model.h5')

        # Test
        print("Test Accuracy: ", model.evaluate(X_test, y_test)[1])
        print("Progress Percentage: ", model.evaluate(X, Y)[1])
        progress = str(round(model.evaluate(X, Y)[1]*100,3))
        y_pred = model.predict_classes(X)

        liberal_dict = dict() # 진보 성향이라 판단한 기사에서 토큰들의 개수
        neoliberal_dict = dict() # 보수 성향이라 판단한 기사에서 토큰들의 개수

        for i, c in enumerate(y_pred):
            if c == 0:
                for t in reviews_p[i]:
                    t = idx_to_token[t]
                    if t in liberal_dict.keys():
                        liberal_dict[t] += 1
                    else:
                        liberal_dict[t] = 1
            else:
                for t in reviews_p[i]:
                    t = idx_to_token[t]
                    if t in neoliberal_dict.keys():
                        neoliberal_dict[t] += 1
                    else:
                        neoliberal_dict[t] = 1

        #inserttodb(news,progress,db_date,porgress_set[k])
        print(sorted(liberal_dict.items(), key=operator.itemgetter(1)))
        print(sorted(neoliberal_dict.items(), key=operator.itemgetter(1)))              
    #print(liberal_dict)
    #print(neoliberal_dict)
