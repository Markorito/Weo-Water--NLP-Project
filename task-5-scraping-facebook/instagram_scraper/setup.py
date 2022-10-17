import pandas as pd
import os
from datetime import date
from Scraping_agent import Scraping_agent
from utils.json_reader import read_json

ACCESS_TOKEN = 'EAAD6sqh5EDwBAAS4Cqfxm9fCWvcZBTHcFKTE0eZBdxFqMWdL82ZCT8DxhBmWWnZBIpdcFn5ot8A8VvKTvwkd9qoXeS6ZCYO2SFqQUrhBgp2GeV2QvAAtBXVOXvVDNPeRLUpyxZCNpshhbEJBwG2gK23IKzjQqSSZAORmlenmWylMlPOEXE8lN4wUQ2H6qECnwZCZCWVjUaoDLvDW0yg5rksNi4cOFt8cnx9YZD'
CLIENT_ID = '275645237628988'
CLIENT_SECRET = '1e64790f044df0dea4ddbe3cbcb65137'
GRAPH_DOMAIN = 'https://graph.facebook.com/'
GRAPH_VERSION = 'v10.0'
DEBUG = 'no'

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
agent_2 = Scraping_agent(
    'EAANAaqqPfJwBAPayTPZAEtiBRuEES2WBZC5s4nZCxIQSeeDyjYbiNi2rJUWEqXdgaiFMJwEAGKXeGjJCy50PYHGc9suiHMvGetMwhOb0t03ytn1oKZB7nQA6s4ZBJ8YlwLsvIane4ClGwcEFhqnOw9GV5jxHwwdapm2j69P1x2ZAbhpDJl9HDFfrmJTNHcBu42IINoPmf0QOp4krQ6luwT',
    "915251802373276",
    "d0d814a4732e21b174f682594381dda6",
    GRAPH_DOMAIN,
    GRAPH_VERSION,
    DEBUG
)

file_path = r'task-5-scraping-facebook\\instagram_scraper\\hashtags.json'
hashtag_set = read_json(file_path)
print(hashtag_set)
# hashtag_set = {
#   "flood" : ['inundacion', 'inundations', 'selyüzünden', 'inundación',
#   'inundaçao', 'inondation', 'inundações', 'inundaciones', 'bumabaha',
#   'flood', 'powódź', 'pagbaha', 'inundacao', 'selsuyu', 'inundation',
#   'overstroming', 'taşkınoldu', 'alluvione', 'Überschwemmung',
#   'sel suyunun', 'floods', 'powodzie', 'inundar', 'inondazione',
#   'su baskını', 'flooded', 'flooding', 'sutaşkın', 'Flut', 'Hochwasser',
#   'banjir', 'inundacão', 'inonder', 'inundated', 'sel bastı', 'inundação',
#   'baha', "flashflood", "floodwatch", "floodwarning", "floodwaters", "floodseason", "flud"],
#   "drought" : ["drought", "desiccation", "droughtseason", "desertification"]
# }

today = date.today()

hashtags_to_iter = list(hashtag_set.values())[0] + list(hashtag_set.values())[1]

for count, hashtag in enumerate(hashtags_to_iter):
  if count == 29 :
    agent = agent_2
  try:
    print(count)
    hashtag_info = agent.getHashtagInfo(hashtag)
    hashtag_id = hashtag_info['json_data']['data'][0]['id']; # store hashtag id
    hashtag_recent_media = agent.getHashtagMedia(hashtag_id,'recent_media')

    df = pd.DataFrame.from_dict(hashtag_recent_media['json_data']['data'])
    dir = f'task-5-scraping-facebook\\instagram_scraper\\output_to_clean\\{hashtag}'
    if not os.path.isdir(dir):
      os.mkdir(dir)
    df.to_csv(f'{dir}\\{today.strftime("%d-%m-%Y")}_{hashtag}_output.csv', index = False, header=True)
  except Exception as e:
    # If the research produces 0 results, an exception is catched
    print(f"exc= {e}")