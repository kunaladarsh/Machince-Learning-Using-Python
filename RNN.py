# -*- coding: utf-8 -*-
"""RNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10ZuPqQXah80sV5Bh9FMFxqBV4NLWfIBn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#To Create a DataFrame 
import pandas as pd
#Use of arrays in Python
import numpy as np
#For Plotting the accuracy
import matplotlib.pyplot as plt
import seaborn as sns
#Natural Language Toolkit for NLP related work
import nltk

# !conda install keras
#Tokenizing the sentences to word
from nltk.tokenize import word_tokenize
from keras.preprocessing.text import Tokenizer
#Padding the sentences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from sklearn.preprocessing import LabelEncoder

import warnings
warnings.filterwarnings('ignore')
sns.set()
nltk.download('punkt')

data = pd.read_csv("IMDB Dataset.csv", engine='python', encoding='utf-8',error_bad_lines=False)
data = pd.DataFrame(data)

print(data)
print (data.shape)
data.head(10)

# Data Vocabulary Creation

def remove_html(review):
    bs = review.BeautifulSoup(review, "html.parser")
    return ' ' + bs.get_review() + ' '
 
def keep_only_letters(review):
    review=re.sub(r'[^a-zA-Z\s]',' ',)
    return review
 
def convert_to_lowercase(review):
    return review.lower()
 
def clean_reviews(review):
    review = remove_html(review)
    review = keep_only_letters(review)
    review = convert_to_lowercase(review)
    return review

imdb_train = data[:]

imdb_test = data[:]



from collections import Counter
 
counter = Counter([words for reviews in imdb_train['review'] for words in reviews.split()])
df = pd.DataFrame()
df['key'] = counter.keys()
df['value'] = counter.values()
df.sort_values(by='value', ascending=False, inplace=True)
 
print (df.shape[0])
print (df[:10000].value.sum()/df.value.sum())
top_10k_words = list(df[:10000].key.values)

#Converting Reviews into lists of integers
import pandas as np
def get_encoded_input(review):
    words = review.split()
    if len(words) > 500:
        words = words[:500]
    encoding = []
    for word in words:
        try:
            index = top_10k_words.index(word)
        except:
            index = 10000
        encoding.append(index)
    while len(encoding) < 500:
        encoding.append(10001)
    return encoding
 
training_data = np.array([get_encoded_input(review) for review in imdb_train['review']])
testing_data = np.array([get_encoded_input(review) for review in imdb_test['review']])
print(training_data.shape, testing_data.shape)

data['review_word_length'] = [len(review.split()) for review in data['review']]
data['review_word_length'].plot(kind='hist', bins=30)
plt.title('Word length distribution')
plt.show()

train_labels = [1 if sentiment=='positive' else 0 for sentiment in imdb_train['sentiment']]
test_labels = [1 if sentiment=='positive' else 0 for sentiment in imdb_test['sentiment']]
train_labels = np.array(train_labels)
test_labels = np.array(test_labels)

# Output labels into numerical form

train_labels = [1 if sentiment=='positive' else 0 for sentiment in imdb_train['sentiment']]
test_labels = [1 if sentiment=='positive' else 0 for sentiment in imdb_test['sentiment']]
train_labels = np.array(train_labels)
test_labels = np.array(test_labels)

# Multi-layer Perceptron (Dense Neural Network) model
import tensorflow
from tensorflow.keras.layers import Activation
 
input_data = tensorflow.keras.layers.Input(shape=(500))
 
data = tensorflow.keras.layers.Embedding(input_dim=10002, output_dim=32, input_length=500)(input_data)
 
data = tensorflow.keras.layers.Flatten()(data)
 
data = tensorflow.keras.layers.Dense(16)(data)
data = tensorflow.keras.layers.Activation('relu')(data)
data = tensorflow.keras.layers.Dropout(0.5)(data)
 
data = tensorflow.keras.layers.Dense(8)(data)
data = tensorflow.keras.layers.Activation('relu')(data)
data = tensorflow.keras.layers.Dropout(0.5)(data)
 
data = tensorflow.keras.layers.Dense(4)(data)
data = tensorflow.keras.layers.Activation('relu')(data)
data = tensorflow.keras.layers.Dropout(0.5)(data)
 
data = tensorflow.keras.layers.Dense(1)(data)
output_data = tensorflow.keras.layers.Activation('sigmoid')(data)
 
model = tensorflow.keras.models.Model(inputs=input_data, outputs=output_data)
 
model.compile(loss='binary_crossentropy', optimizer='adam', metrics='accuracy')
model.summary()

print(testing_data)

print(test_labels)

print(training_data)

print(train_labels)

model.fit(training_data, train_labels, epochs=10, batch_size=61, validation_data=(testing_data, test_labels))

## RNN

import tensorflow
from tensorflow.keras.layers import Activation
 
input_data = tensorflow.keras.layers.Input(shape=(500))
 
data = tensorflow.keras.layers.Embedding(input_dim=10002, output_dim=32, input_length=500)(input_data)
 
data = tensorflow.keras.layers.Bidirectional(tensorflow.keras.layers.SimpleRNN(50))(data)
 
data = tensorflow.keras.layers.Dense(1)(data)
output_data = tensorflow.keras.layers.Activation('sigmoid')(data)
 
model = tensorflow.keras.models.Model(inputs=input_data, outputs=output_data)
 
model.compile(loss='binary_crossentropy', optimizer='adam', metrics='accuracy')
model.summary()

history = model.fit(training_data, train_labels, epochs=10, batch_size=256, validation_data=(testing_data, test_labels))