import sys
import time
import warnings

#!{sys.executable} -m pip install unidecode

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#pre-processing
import re
import unidecode
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from bs4 import BeautifulSoup
import pickle5 as pickle

import torch
import torch.nn as nn
from torch.optim.optimizer import Optimizer
import torch.nn.functional as F

from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from tqdm import tqdm

def get_prediction(article_content):

    MODEL_FILE               = "/home/kunal03/WeoWater/task-4-scraping-newspapers/Final_Scraper/drought_classifier/model_newsclassifier_drought_v1.pt"
    EMBEDDING_MATRIX_FILE    = "/home/kunal03/WeoWater/task-4-scraping-newspapers/Final_Scraper/drought_classifier/embedding_matrix_v1_2.npy"
    TOKENIZER_FILE           = "/home/kunal03/WeoWater/task-4-scraping-newspapers/Final_Scraper/drought_classifier/tokenizer_drought_v1_2.pkl"
    LABEL_ENCODER_FILE       = "/home/kunal03/WeoWater/task-4-scraping-newspapers/Final_Scraper/drought_classifier/label_encoder_drought_v1_2.pkl"
    
    embed_size = 300 # how big is each word vector
    max_features = 15500 # how many unique words to use (i.e num rows in embedding vector)
    maxlen = 500 # max number of words in a content to use

    embedding_matrix = np.load(EMBEDDING_MATRIX_FILE)

    with open(TOKENIZER_FILE,'rb') as file:
        tokenizer=pickle.load(file)

    with open(LABEL_ENCODER_FILE, 'rb') as file:
        le = pickle.load(file)

    def preprocess(article):
        """
        This function takes a string as input, then performs these operations: 
            - lowercase
            - remove URLs
            - remove ticker symbols 
            - removes punctuation
            - removes any single character tokens
        Parameters
        ----------
            message : The text message to be preprocessed
        Returns
        -------
            text: The preprocessed text
        """ 
        # Lowercase the article
        text = article.lower()
        # Replace URLs with a space in the message
        text = re.sub('https?:\/\/[a-zA-Z0-9@:%._\/+~#=?&;-]*', ' ', text)
        # Replace ticker symbols with a space. The ticker symbols are any stock symbol that starts with $.
        text = re.sub('\$[a-zA-Z0-9]*', ' ', text)
        text = re.sub('\@[a-zA-Z0-9]*', ' ', text)
        # Replace everything not a letter or apostrophe with a space
        text = re.sub('[^a-zA-Z\']', ' ', text)
        # Remove single letter words
        text = ' '.join( [w for w in text.split() if len(w)>1] )
        
        return text

    class BiLSTM(nn.Module): 
        def __init__(self):
            super(BiLSTM, self).__init__()
            self.hidden_size_1 = 64
            self.hidden_size_2 = 64
            self.extra_features = 0
            drp = 0.1
            n_classes = 2
            self.embedding = nn.Embedding(max_features, embed_size)
            self.embedding.weight = nn.Parameter(torch.tensor(embedding_matrix, dtype=torch.float32))
            self.embedding.weight.requires_grad = False
            self.lstm = nn.LSTM(embed_size, self.hidden_size_1, bidirectional=True, batch_first=True)
            self.linear = nn.Linear(self.hidden_size_1*4 + self.extra_features, self.hidden_size_2)
            self.relu = nn.ReLU()
            self.dropout = nn.Dropout(drp)
            self.out = nn.Linear(self.hidden_size_2, n_classes)

        def forward(self, x):
            input = x[:,:maxlen]
            of = x[:,maxlen:]
            
            h_embedding = self.embedding(input)
            
            h_lstm, _ = self.lstm(h_embedding)
            avg_pool = torch.mean(h_lstm, 1)
            max_pool, _ = torch.max(h_lstm, 1)
            conc = torch.cat(( avg_pool, max_pool, of), 1)
            conc = self.relu(self.linear(conc))
            conc = self.dropout(conc)
            out = self.out(conc)
            return out

    model = BiLSTM()
    model.load_state_dict(torch.load(MODEL_FILE))
    model.eval()
    print("Loaded the model")

    article_content = [preprocess(article) for article in tqdm(article_content)]

    predict_X = tokenizer.texts_to_sequences(article_content)
    predict_X = pad_sequences(predict_X, maxlen=maxlen)

    x_cv = torch.tensor(predict_X, dtype=torch.long)

    pred = model(x_cv).detach()
    pred = F.softmax(pred).cpu().numpy()

    pred1 = le.inverse_transform(pred.argmax(axis=1))
    return pred1