import pandas as pd
import numpy as np
import pickle
import operator
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

def cleanup(sentence):
    word_tok = nltk.word_tokenize(sentence)
    stemmed_words = [stemmer.stem(w) for w in word_tok]
    return ' '.join(stemmed_words)

# Load and preprocess the data
data = pd.read_csv('BankFAQs.csv')
questions = data['Question'].values

X = []
for question in questions:
    X.append(cleanup(question))

# Initialize and fit the TF-IDF vectorizer
tfv = TfidfVectorizer(min_df=1, stop_words='english')
X = tfv.fit_transform(X)

# Initialize and fit the label encoder
le = LabelEncoder()
y = le.fit_transform(data['Class'])

# Initialize and train the model
model = SVC(kernel='linear')
model.fit(X, y)

# Save the trained model and objects using pickle
with open('trained_model.pkl', 'wb') as file:
    pickle.dump(model, file)

with open('tfv.pkl', 'wb') as file:
    pickle.dump(tfv, file)

with open('le.pkl', 'wb') as file:
    pickle.dump(le, file)
