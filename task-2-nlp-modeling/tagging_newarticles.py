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

# Username of your GitHub account
username = ''

# Personal Access Token (PAO) from your GitHub account
token = ''

# Creates a re-usable session object with your creds in-built
github_session = requests.Session()
github_session.auth = (username, token)

url = 'https://raw.githubusercontent.com/OmdenaAI/WeoWater/main/task-2-nlp-modeling/data/news_articles_for_geoparsing_comparison.csv'
download = github_session.get(url).content #Reading and downloading the data

data = pd.read_csv(io.StringIO(download.decode('utf-8'))) #Converting the data into a pd dataframe
my_cliff= Cliff('http://localhost:8080')
data['Tagged Country']= ''

for row,col in data.iterrows():
    article_title = col['title']
    title_results = my_cliff.parse_text(article_title)
    title_mention = title_results['results']['places']['mentions']
    location_from_title = [val['name'] for val in title_mention]
    country_code = [val['countryCode'] for val in title_mention]
    if location_from_title == []:
        location = 'Not Identified'
        data._set_value(row,'Tagged Country',location)
    else:
        location = location_from_title[0] + ','+ country_code[0]
        data._set_value(row, 'Tagged Country', location)

print(data['Tagged Country'])
data.to_csv('articles_with_tagged_location.csv',index=False)



