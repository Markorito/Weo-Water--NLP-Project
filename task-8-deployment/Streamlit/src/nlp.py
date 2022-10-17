import streamlit as st
from fastai.text.all import *
import pandas as pd
import torch
import torch.nn as nn
from torch.optim.optimizer import Optimizer
import torch.nn.functional as F
import numpy as np

#pre-processing
import re

from tqdm import tqdm
import pickle5 as pickle
from keras.preprocessing.sequence import pad_sequences

from src.download_models import MODELS_DIR_FASTAI, MODELS_DIR_BiLSTM, MODELS_DIR_LSTM, FASTAI_MODELS, BiLSTM_MODELS, LSTM_MODELS

from tensorflow import keras
import nltk
nltk.download('stopwords')

class FastaiModel:
    # Here we can keep a list of relevant models
    models = FASTAI_MODELS

    def __init__(self, model_name, event_type):
        self.model = None
        self.model_name = model_name
        self.event_type = event_type
        self.load_classifier()

    def load_classifier(self) -> None:
        """
        Load classifier from storage into memory.
        """
        # select the model that matches the given `model_name` (the latest version)
        try:
            selected_model = max(
                [
                    x
                    for x in FastaiModel.models
                    if x["name"] == self.model_name
                    and x["event_type"] == self.event_type
                ],
                key=lambda x: x.get("version", ""),
            )
        except ValueError:
            raise ValueError("Classifier not found")

        # load model and store in class property
        save_dest = MODELS_DIR_FASTAI / selected_model["name"]
        self.model = load_learner(save_dest)

    def get_predictions_df(self, elements_to_predict, with_original_inputs=False) -> pd.DataFrame:
        """
        Compute predicted scores for each element in `elements_to_predict`
        and return a dataframe with the input elements and their scores

        with_original_inputs: if True, the dataframe will have one column with the original input
        """
        test_dl = self.model.dls.test_dl(elements_to_predict)

        # sometimes the progress bar from fastai conflicts with the streamllit app,
        # so here we avoid building such progress bar
        with self.model.no_bar():
            preds = self.model.get_preds(dl=test_dl)[0]

        tmp = pd.Series(preds).apply(pd.Series).applymap(lambda x: x.item())

        if not with_original_inputs:
            return tmp

        df_predictions = test_dl.items.to_frame()
        tmp.index = df_predictions.index
        df_predictions[tmp.columns.astype(str)] = tmp

        return df_predictions

class BiLSTM_Model:
    # Here we can keep a list of relevant models
    models = BiLSTM_MODELS

    embed_size = 300
    maxlen = 500

    def __init__(self, model_name, event_type, scraper_type):
        self.model = None
        self.model_name = model_name
        self.event_type = event_type
        self.scraper_type = scraper_type
        self.load_classifier()

    def load_classifier(self) -> None:
        """
        Load classifier from storage into memory.
        """
        # select the model that matches the given `model_name` (the latest version)
        try:
            selected_model = max(
                [
                    x
                    for x in BiLSTM_Model.models
                    if x["name"] == self.model_name
                    and x["event_type"] == self.event_type
                    and x["scraper_type"] == self.scraper_type
                ],
                key=lambda x: x.get("version", ""),
            )
        except ValueError:
            raise ValueError("Classifier not found")

        embedding_matrix_file = self.scraper_type + '_embedding_matrix_' + self.event_type +'.npy'
        Embedding_Matrix_location = MODELS_DIR_BiLSTM / embedding_matrix_file
        embedding_matrix = np.load(Embedding_Matrix_location)

        if self.scraper_type == "Newspaper":
            if self.event_type == "Flood":
                max_features = 35000
            else:
                max_features = 15500

        elif self.scraper_type == "Instagram":
            if self.event_type == "Flood":
                max_features = 8900
            else:
                max_features = 4000

        elif self.scraper_type == "Twitter":
            if self.event_type == "Flood":
                max_features = 2000
            else:
                max_features = 800

        embed_size = self.embed_size
        maxlen = self.maxlen

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

        # load model and store in class property
        save_dest = MODELS_DIR_BiLSTM / selected_model["name"]
        model = BiLSTM()
        model.load_state_dict(torch.load(save_dest))
        self.model = model

    def get_predictions_df(self, elements_to_predict, scraper_type, event_type,with_original_inputs=False) -> pd.DataFrame:
        """
        Compute predicted scores for each element in `elements_to_predict`
        and return a dataframe with the input elements and their scores

        with_original_inputs: if True, the dataframe will have one column with the original input
        """

        self.model.eval()
        tokenizer_file = scraper_type + '_tokenizer_' + event_type +'.pkl'
        tokenizer_file_location = MODELS_DIR_BiLSTM / tokenizer_file
        with open(tokenizer_file_location,'rb') as file:
            tokenizer=pickle.load(file)

        def preprocess(article):
            if pd.isna(article):
                return None

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

        article_content = [preprocess(article) for article in tqdm(elements_to_predict)]
        predict_X = tokenizer.texts_to_sequences(article_content)
        predict_X = pad_sequences(predict_X, maxlen=self.maxlen)
        x_cv = torch.tensor(predict_X, dtype=torch.long)
        pred = self.model(x_cv).detach()
        pred = F.softmax(pred).cpu().numpy()
        preds = pred[:,0]

        df_predictions = elements_to_predict
        df_predictions['score'] = preds

        return df_predictions

class LSTM_Model:
    # Here we can keep a list of relevant models
    models = LSTM_MODELS

    def __init__(self, model_name, event_type, scraper_type):
        self.model = None
        self.model_name = model_name
        self.event_type = event_type
        self.scraper_type = scraper_type
        self.load_classifier()

    def load_classifier(self) -> None:
        """
        Load classifier from storage into memory.
        """
        # select the model that matches the given `model_name` (the latest version)
        try:
            selected_model = max(
                [
                    x
                    for x in LSTM_Model.models
                    if x["name"] == self.model_name
                    and x["event_type"] == self.event_type
                    and x["scraper_type"] == self.scraper_type
                ],
                key=lambda x: x.get("version", ""),
            )
        except ValueError:
            raise ValueError("Classifier not found")

        # load model and store in class property
        save_dest = MODELS_DIR_LSTM / selected_model["name"]
        self.model = keras.models.load_model(save_dest)

    def get_predictions_df(self, elements_to_predict, scraper_type, event_type,with_original_inputs=False) -> pd.DataFrame:
        """
        Compute predicted scores for each element in `elements_to_predict`
        and return a dataframe with the input elements and their scores

        with_original_inputs: if True, the dataframe will have one column with the original input
        """
        tokenizer_file = scraper_type + '_tokenizer_' + event_type +'.pkl'
        tokenizer_file_location = MODELS_DIR_LSTM / tokenizer_file
        with open(tokenizer_file_location,'rb') as file:
            tokenizer=pickle.load(file)

        def preprocess(article):
            if pd.isna(article):
                return None

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

        article_content = [preprocess(article) for article in tqdm(elements_to_predict)]
        article_content = tokenizer.texts_to_sequences(article_content)
        article_content = pad_sequences(article_content, maxlen=20)
        preds = self.model.predict(article_content)[0][0]
        df_predictions = elements_to_predict
        df_predictions['score'] = preds

        return df_predictions
