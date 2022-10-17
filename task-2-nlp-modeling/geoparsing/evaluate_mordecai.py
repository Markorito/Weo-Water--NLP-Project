import mordecai
import pandas as pd
from pprint import pprint

def geoparse(geo, text, out):
    results = geo.geoparse(text)
    for result in results:
        print('=> {} {}'.format(
            result['country_predicted'],
            result['country_conf'],
        ), end='', file=out)
        if 'geo' in result:
            print(' ({} -> {})'.format(
                result['word'],
                result['geo']['place_name'],
            ), end='', file=out)
        print(file=out)
    if not results:
        print('=> No geolocation found.', file=out)

if __name__ == '__main__':
    d_twitter = pd.read_csv('data/twitter_geo_v1.csv', encoding='utf-8')
    d_news = pd.read_csv('data/articles_with_tagged_location_v1.csv', encoding='utf-8')
    d_instagram = pd.read_csv('data/IGpost_with_tagged_location_v1.csv', encoding='utf-8')

    geo = mordecai.Geoparser()
    out = open('mordecai.txt', 'w', encoding='utf-8')

    number = 0
    for i, row in d_twitter.iterrows():
        body = row['body']
        assert isinstance(body, str)
        print('\n{}: "{}"'.format(number, body), file=out)
        # Get rid of hash symbols which may confuse geoparsing
        body = body.replace('#', '')
        geoparse(geo, body, out)
        number += 1

    number = 0
    for i, row in d_instagram.iterrows():
        body = row['body']
        assert isinstance(body, str)
        print('\n{}: "{}"'.format(number, body), file=out)
        # Get rid of hash symbols which may confuse geoparsing
        body = body.replace('#', '')
        geoparse(geo, body, out)
        number += 1

    number = 0
    for i, row in d_news.iterrows():
        title = row['title']
        body = row['body']
        assert isinstance(title, str)
        assert isinstance(body, str)
        print('\n{}: "{}"'.format(number, title), file=out)
        geoparse(geo, title, out)
        print('\n{}: "{}"'.format(number, body), file=out)
        geoparse(geo, body, out)
        number += 1

    out.close()
