from textblob import TextBlob
import streamlit as st
import pandas as pd

from front_end import setup_front_end
from scraper import custom_scraper, get_article_content_display, get_article_content, get_news_links 
from flood_classifier import flood_classifier
from drought_classifier import drought_classifier

#defining global variables
gn_data = pd.read_csv('./data/gn_supported.csv',index_col=0)
country_codes = pd.read_csv('./data/country_codes.csv')
language_codes = pd.read_csv('./data/language_codes.csv')

(
    disaster_event,
    country_name, 
    language, 
    start_date, 
    end_date
) = setup_front_end()

number_of_articles = st.slider('Select the number of articles to be viewed')

if st.button('Find Articles'):
    final_result = pd.DataFrame()
    predictions = pd.DataFrame()
    
    for name in country_name:

        #st.write(name)
        country_code_final = country_codes[country_codes['Country'] == name]['Alpha-2 code'].values[0]

        for lang in language:
            #st.write(lang)
            language_code_final = language_codes[language_codes.Language == lang]['language_code'].values[0]

            ##Verify the input language 
            if language_code_final not in gn_data['Language_code'].to_list():
                language_code_final = 'en'
                st.write("**There are no news articles available in this language.**") 
                st.write("**Displaying the results in Default Language and Country Setting.**") 

            ##Determine the type of disaster
            if disaster_event == 'Flood':
                keyword_final = gn_data.loc[gn_data.Language_code == language_code_final,'Flood_keyword'].values[0]
            else:
                keyword_final = gn_data.loc[gn_data.Language_code == language_code_final,'Drought_keyword'].values[0] 
              
            keywords = str(str(name)+' '+str(keyword_final))

            news_results_list = get_news_links(keywords,country_code_final, language_code_final,str(start_date),str(end_date),number_of_articles,disaster_event,name,lang)
            final_result = final_result.append(news_results_list)

    ##Storing the final scraped data.
    final_result.drop_duplicates('title', inplace=True)
    print("Scraping done!")

    if disaster_event == 'Flood':
        predictions = flood_classifier.get_prediction(final_result['title'] + final_result['body'])
        print(predictions)
    
    else:
        predictions = drought_classifier.get_prediction(final_result['title'] + final_result['body'])
        print(predictions)


    final_result.to_csv("Scraped_news_articles_for"+str(keywords)+'.csv')    


    


