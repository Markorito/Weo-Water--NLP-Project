"""
this script iters through the Instagram data scraped
and allows the user to tag if the output is useful or not.

- How it works?
The script reads the csv files (inside the specified folder "dir") row by row.
For each post (row) it opens a browser page (default browser "microsoft edge",
more browsers will be added later) using he permalink related to the post.
Every time a page is opened, the script asks the user, via terminal, if the post is useful or not.
All the useful post are saved in the "output_cleaned" folder
"""
import os
import sys
import webbrowser

import numpy as np
import pandas as pd
import datetime

ts = datetime.datetime.now().timestamp()
t_stamp = pd.Timestamp(ts, unit='s')



directory = "cleaned_with_none"  # the script reads the csv files from this directory
# output_folder =

columns = ['id', 'caption', 'comments_count', 'like_count', 'media_type', 'media_url', 'permalink', 'timestamp', 'keyword']
insta_merged = pd.DataFrame(columns=columns)

for subdir, dirs, files in os.walk(directory):
    '''
    This loop iterates within the sub-folders 
    '''
    print(subdir)
    hashtag = subdir.split("\\")[-1]
    print(f"Hashtag: {hashtag}")
    for file in files:
        print(f'Reading file {file}')
        df = pd.read_csv(os.path.join(directory, hashtag, file))
        df['hashtag'] = hashtag
        insta_merged = pd.concat([insta_merged, df])

os.chdir('../..')

        
insta_merged.to_csv(r'task-3-wrangling-preprocessing\Scraped Instagram Data - Merged\insta_merged{year}_{month}_{day}.csv'.format(year=t_stamp.year, month=t_stamp.month, day=t_stamp.day))