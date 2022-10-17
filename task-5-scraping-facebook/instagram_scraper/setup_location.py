import json
import pandas as pd
import os
from datetime import date
from Scraping_agent import Scraping_agent

ACCESS_TOKEN = 'EAAEKhP7xXfQBADAd7ZCWOii1bccRXYxOD3pUhwRsFaryPZC1P4lXSfZBus3CYcSZAZC3gSeNE9AbX6Wp8iZCICy7xi022gIt1MesxPZAW9eHWxmMpu5TMugJZAVT4W4SSW810CY5ZAgBqmVTpja5VQTqzoNGWapydJ6mCMG6rrmAZAzQZDZD'
CLIENT_ID = '293041305902580'
CLIENT_SECRET = 'd2511561a0b11dc7578e47c0ce441a63'
GRAPH_DOMAIN = 'https://graph.facebook.com/'
GRAPH_VERSION = 'v10.0'
DEBUG = 'no'

# ACCESS_TOKEN = 'EAAD6sqh5EDwBAAS4Cqfxm9fCWvcZBTHcFKTE0eZBdxFqMWdL82ZCT8DxhBmWWnZBIpdcFn5ot8A8VvKTvwkd9qoXeS6ZCYO2SFqQUrhBgp2GeV2QvAAtBXVOXvVDNPeRLUpyxZCNpshhbEJBwG2gK23IKzjQqSSZAORmlenmWylMlPOEXE8lN4wUQ2H6qECnwZCZCWVjUaoDLvDW0yg5rksNi4cOFt8cnx9YZD'
# CLIENT_ID = '275645237628988'
# CLIENT_SECRET = '1e64790f044df0dea4ddbe3cbcb65137'
# GRAPH_DOMAIN = 'https://graph.facebook.com/'
# GRAPH_VERSION = 'v10.0'
# DEBUG = 'no'

agent = Scraping_agent(
    ACCESS_TOKEN,
    CLIENT_ID,
    CLIENT_SECRET,
    GRAPH_DOMAIN,
    GRAPH_VERSION,
    DEBUG
)


"""
If we need to scrape more than 30 unique hashtags in a week we need to use another scraper. 
So we need two business accounts
"""
# agent_2 = Scraping_agent(
#     '''EAANAaqqPfJwBAPayTPZAEtiBRuEES2WBZC5s4nZCxIQSeeDyjYbiNi2rJUWEqXdgaiFMJwEAGKXeGjJCy50PYHGc9suiHMvGetMwhOb0t03ytn1
#     oKZB7nQA6s4ZBJ8YlwLsvIane4ClGwcEFhqnOw9GV5jxHwwdapm2j69P1x2ZAbhpDJl9HDFfrmJTNHcBu42IINoPmf0QOp4krQ6luwT''',
#     "915251802373276",
#     "d0d814a4732e21b174f682594381dda6",
#     GRAPH_DOMAIN,
#     GRAPH_VERSION,
#     DEBUG
# )

hashtag_set = {}

# with open("hashtags/flood_hashtags.txt", "r", encoding='utf-8') as fp:
#     hashtag_set['flood'] = json.load(fp)
#
# with open(r"hashtags/drought_hashtags.txt", "r", encoding='utf-8') as fp:
#     hashtag_set['drought'] = json.load(fp)

with open(r"hashtags/location_hashtags.txt", "r", encoding='utf-8') as fp:
    hashtag_set['location'] = json.load(fp)


today = date.today()

hashtags_to_iter = []
for key in hashtag_set.keys():
    hashtags_to_iter.extend(hashtag_set[key])

for count, hashtag in enumerate(hashtags_to_iter):
    if count <= 30:
        #agent = agent_2
        try:
            print(count)
            hashtag_info = agent.getHashtagInfo(hashtag)
            print(hashtag_info['json_data'])
            hashtag_id = hashtag_info['json_data']['data'][0]['id']  # store hashtag id
            hashtag_recent_media = agent.getHashtagMedia(hashtag_id, 'recent_media')

            df = pd.DataFrame.from_dict(hashtag_recent_media['json_data']['data'])
            directory = f'task-5-scraping-facebook\\instagram_scraper\\output_to_clean\\{hashtag}'
            if not os.path.isdir(directory):
                os.mkdir(directory)
            df.to_csv(f'{directory}\\{today.strftime("%d-%m-%Y")}_{hashtag}_output.csv', index=False, header=True)
        except Exception as e:
            # If the research produces 0 results, an exception is cached
            print(f"exc= {e}")