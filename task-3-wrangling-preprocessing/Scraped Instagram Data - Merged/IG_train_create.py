import os
import numpy as mp
import pandas as pd

# move directory to task 3 folder
os.chdir('..')

# read in merged data with only english posts
all_data = pd.read_csv(r'All_merged/All_consolidated_and_little_processed.csv')

# Extract Instagram posts only
ig_data = all_data.loc[all_data['data_source']=='Instagram']

ig_data.to_csv('IG_english_only.csv')

ig_data.sample

