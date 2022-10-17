import geograpy
import pandas as pd

d = pd.read_csv('data/cleaned_merged_labbeled_newspaper_data.csv')

for _, row in d.iterrows():
    category = row['category']
    if category != 'flood':
        continue
    print('## {}\n'.format(row['article_title']))
    content = row['article_content']
    print(content)
    places = geograpy.get_geoPlace_context(text=content)
    print('>>> countries:', places.countries)
    print('>>> regions:', places.regions)
    print('>>> cities:', places.cities)
    print('>>> other:', places.other)
    print('>>> country_mentions:', places.country_mentions)
    print('>>> region_mentions:', places.region_mentions)
    print('>>> city_mentions:', places.city_mentions)
    print('[press Enter to continue]'
    input()