from facebook_scraper import get_posts
import pandas as pd
import numpy as np
import csv
from tqdm import tqdm

profiles=['FloodDroughtMgt','Idpgroup10','keralafloods','fiercetartan','floodnewsuk','globalfloodnews','NSWFloodUpdate',
          'floodnewsuk','FloodMap.net','FolsomLakeDrought','451917435121']

listposts = []

for profile in profiles:
  for post in get_posts(profile):
    listposts.append(post)

df= pd.DataFrame(listposts)
print(df.head(10))
df.to_csv('FB_scrap.csv', header=True, index=False)

