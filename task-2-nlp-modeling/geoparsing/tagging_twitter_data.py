import pandas as pd
import argparse
from cliff.api import Cliff
import numpy as np
import csv
from tqdm import tqdm
import base64
from io import BytesIO
import requests
import io
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import *

# Username of your GitHub account
username = 'mansimht'

# Personal Access Token (PAO) from your GitHub account
token = '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'

# Creates a re-usable session object with your creds in-built
github_session = requests.Session()
github_session.auth = (username, token)

url = 'https://raw.githubusercontent.com/OmdenaAI/WeoWater/main/task-2-nlp-modeling/geoparsing/data/twitter_geo_v1.csv'
download = github_session.get(url).content #Reading and downloading the data
data = pd.read_csv(io.StringIO(download.decode('utf-8'))) #Converting the data into a pd dataframe

# clean_tweets=[]
# for posts in tqdm(data['body']):
#   tokenizer= RegexpTokenizer(r'\w+')
#   token_words= tokenizer.tokenize(posts)
#   token_with_stopword= [word for word in token_words if not word in stopwords.words()]
#   clean_tweets.append(token_with_stopword)
# data['Cleaned_body']= clean_tweets

my_cliff= Cliff('http://localhost:8080')
location=[]
for row,col in data.iterrows():
    tweets= col['body']
    tweet_results= my_cliff.parse_text(tweets)
    tweet_mention= tweet_results['results']['places']['mentions']
    if tweet_mention == []:
        location='Not Identified'
        data._set_value(row,'country',location)
    else:
        location_from_caption = [val['name'] for val in tweet_mention]
        country_code= [val['countryCode'] for val in tweet_mention]
        location= location_from_caption[0]+ ',' +country_code[0]
        data._set_value(row, 'country', location)

print(data['country'])
data.to_csv('twitter_with_tagged_location_v1.csv',index=False)