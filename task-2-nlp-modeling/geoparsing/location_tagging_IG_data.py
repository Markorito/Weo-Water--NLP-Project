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

url = 'https://raw.githubusercontent.com/OmdenaAI/WeoWater/main/task-3-wrangling-preprocessing/All_data_sources_merged_updated.csv'
download = github_session.get(url).content #Reading and downloading the data
data = pd.read_csv(io.StringIO(download.decode('utf-8'))) #Converting the data into a pd dataframe

#Extract instagram data from all dataseources
ig_data = data.loc[data['data source']=='Instagram']
ig_data.to_csv('ig_data.csv')

#choose random 17 post with location and 4 without location
ig_post= pd.read_csv('C:\Python37\Scripts\Geotagging\IGpost_without_tagged_location.csv')
ig_post['country']= ig_post['country'].astype(object)

my_cliff= Cliff('http://localhost:8080')
location=[]
for row,col in ig_post.iterrows():
    ig_captions= col['body']
    ig_results= my_cliff.parse_text(ig_captions)
    ig_mention= ig_results['results']['places']['mentions']
    if ig_mention == []:
        location='Not Identified'
        ig_post._set_value(row,'country',location)
    else:
        location_from_caption = [val['name'] for val in ig_mention]
        country_code= [val['countryCode'] for val in ig_mention]
        location= location_from_caption[0]+ ',' +country_code[0]
        ig_post._set_value(row, 'country', location)

print(ig_post['country'])
ig_post.to_csv('IGpost_with_tagged_location.csv',index=False)