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

print(sys.argv)

# Get the desired browser
if len(sys.argv) == 1 or len(sys.argv) > 2:
    browser = 'msedge'
else:
    browser = sys.argv[1]

print(browser)
# Add the browser paths to the webbrowser library (@TODO add path for IUNIX systems)
webbrowser.register('msedge',
    None,
    webbrowser.BackgroundBrowser(r"C:\Program Files (x86)//Microsoft//Edge//Application//msedge.exe"))

webbrowser.register('mschrome',
    None,
    webbrowser.BackgroundBrowser(r"C:\Program Files (x86)//Google//Chrome//Application//chrome.exe"))


directory = "tmp_output_to_clean"  # the script reads the csv files from this directory

# set keyword based on hashtag
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
    print(subdir)
    hashtag = subdir.split("\\")[-1]
    print(f"Hashtag: {hashtag}")
    final_dir = f'cleaned_with_none\\{hashtag}'  # destination directory

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
        try:
            if os.path.exists(f'{final_dir}\\{file}'):
                continue
            df = pd.read_csv(os.path.join(subdir, file))
            df_len = len(df)
            df['keyword'] = 'none'  # add a column to be updated if an element has been skipped
            for count, (id, permalink) in enumerate(zip(df['id'], df['permalink'])):
                # print(permalink)
                webbrowser.get(browser).open_new(permalink)  # using the desired browser, the script opens a webpage
                # using the post's permalink
                is_useful = input("is the post useful? [y/n/s (skip)]")
                # print(is_useful)
                is_useful = is_useful.lower().strip()
                if is_useful == 'y' or is_useful == 'yes':
                    print("yes")
                    df.loc[df['id'] == id, 'keyword'] = keyword  # mark row true if not relevant
                elif is_useful == 'n' or is_useful == 'no':
                    print("no")
                    df.loc[df['id'] == id, 'keyword'] = 'none'  # mark row false if not relevant
                else:
                    print("!" * 40)
                    print("You typed a wrong letter, please, manually correct the problem.")
                print(f'remaining {df_len - count - 1}')
            if not os.path.isdir(final_dir):
                os.mkdir(final_dir)
            df.to_csv(f'{final_dir}\\{file}', index=False, header=True)
            
        except Exception as e:
            # If the file is empty catch error
            print(f"exc= {e}")
