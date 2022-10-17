"""
this script is for use one time to add a label column of keyword to the already cleaned folders

- How it works?
It checks for files in the output_cleaned folder and then compares them against the same csv files in output_to_clean.
The keyword column is marked with keyword for the
"""
import os
import sys
import webbrowser

import numpy as np
import pandas as pd

# set directory for looking through all scraped data
directory = "output_to_clean"

# read in keywords
hashtag_set = {
  "flood" : ['inundacion', 'inundations', 'selyüzünden', 'inundación',
  'inundaçao', 'inondation', 'inundações', 'inundaciones', 'bumabaha',
  'flood', 'powódź', 'pagbaha', 'inundacao', 'selsuyu', 'inundation',
  'overstroming', 'taşkınoldu', 'alluvione', 'Überschwemmung',
  'sel suyunun', 'floods', 'powodzie', 'inundar', 'inondazione',
  'su baskını', 'flooded', 'flooding', 'sutaşkın', 'Flut', 'Hochwasser',
  'banjir', 'inundacão', 'inonder', 'inundated', 'sel bastı', 'inundação',
  'baha', "flashflood", "floodwatch", "floodwarning", "floodwaters", "floodseason", "flud"],
  "drought" : ["drought", "desiccation", "droughtseason", "desertification"]
}


for subdir, dirs, files in os.walk(directory):
    '''
    This loop iterates within the sub-folders 
    '''
    if subdir != 'output_to_clean':
        print(subdir)
        hashtag = subdir.split("\\")[-1]
        print(f"Hashtag: {hashtag}")

        # set directory for already cleaned data without 'none' label
        final_dir = f'output_cleaned\\{hashtag}'

        # set directory for cleaned data with 'none' label
        clean_with_none = f'cleaned_with_none\\{hashtag}'

        # set keyword based on hashtag
        keyword = 'none'
        if (hashtag in hashtag_set['flood']) and (hashtag in hashtag_set['drought']):
            keyword = 'flood_and_drought'
        elif hashtag in hashtag_set['drought']:
            keyword = 'drought'
        elif hashtag in hashtag_set['flood']:
            keyword = 'flood'

        for file in files:
            print(f'Reading file {file}')

            if os.path.exists(f'{final_dir}\\{file}'):
                df_true = pd.read_csv(os.path.join(final_dir, file))
                relevant = df_true['id'].unique()
                try:
                    df_new = pd.read_csv(os.path.join(subdir, file))
                    df_new['keyword'] = 'none'
                    df_new.loc[df_new['id'].isin(relevant), 'keyword'] = keyword
                    if not os.path.isdir(clean_with_none):
                        os.mkdir(clean_with_none)
                    df_new.to_csv(f'{clean_with_none}\\{file}', index=False, header=True)
                    print(f'{clean_with_none}\\{file}')
                except:
                    print('error')