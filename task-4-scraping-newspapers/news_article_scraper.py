#importing requiring libraries
import nltk
from textblob import TextBlob
import streamlit as st
import datetime
from newspaper import Article
from newspaper import Config
from pygooglenews import GoogleNews
from PIL import Image
from PIL import UnidentifiedImageError
import requests
from io import BytesIO
import pandas as pd
import requests
import regex as re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

#defining global variables
gn_data = pd.read_csv('./gn_supported.csv',index_col=0)
custom_tags = pd.read_csv('./Custom_Websites_Tags.csv')
country_codes = pd.read_csv('./country_codes.csv')
language_codes = pd.read_csv('./language_codes.csv')


#defining custom scraper
def custom_scraper(url, title_tag, title_class, date_tag, date_class):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    article_title = soup.find(title_tag, class_=title_class)
    article_title = article_title.get_text()

    article_content = ""

    regex = re.compile('.*Paragraph')
    for each in soup.find_all('p'):
        article_content = article_content + each.get_text() + " "
    date_published = soup.find(date_tag, class_=date_class).get_text()
    return article_content,date_published


#Get the sumary of the articles
def get_article_content_display(article_url):
    # try block added
    try:
        news_article = Article(article_url)

        news_article.download()
        news_article.parse()  
        news_article.nlp()

        # get a summary of article
        st.write("**Summary:** %s" % news_article.summary)
    except:
        pass

    return 


def get_article_content(article_url):
    # get the date of posting the article
    news_content = ""
    date_published = ""
    try:
        news_article = Article(article_url)
        news_article.download()
        news_article.parse()
        news_article.nlp()
        news_content = news_article.text
        date_published = news_article.publish_date
        
    except:
        pass

    if len(news_content)==0:
        domain = urlparse(article_url).netloc
        if domain in custom_tags['Newspaper website name'].tolist():
            title_tag = custom_tags[custom_tags['Newspaper website name']==domain]['title_tag'].values[0]
            title_class = custom_tags[custom_tags['Newspaper website name']==domain]['title_class'].values[0]
            date_tag = custom_tags[custom_tags['Newspaper website name']==domain]['date_tag'].values[0]
            date_class = custom_tags[custom_tags['Newspaper website name']==domain]['date_class'].values[0]
            news_content,date_published = custom_scraper(article_url, title_tag, title_class, date_tag, date_class)
           
    #get the article text
    return news_content, date_published,news_article.top_image, news_article.keywords


# function to get top n news links
def get_news_links(search_terms,country_code_final, language_code_final,start_date,end_date,num_articles,disaster_event,name,lang):

     #to access through the firewall
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent

    gn = GoogleNews(country=country_code_final, lang=language_code_final)
    article_num =[]
    article_title = []
    article_link = []
    article_content = []
    publishing_date = []
    article_image = []
    article_keywords =[]
    search = gn.search(query=search_terms, helper = True, when = None, from_ = start_date, to_ = end_date , proxies=None, scraping_bee=None)

    count = 0
    i=0
   
    for item in search['entries']:
        if count < num_articles:
            st.write('**Result no. %s:**' % int(i+1))
            article_num.append(count)
            count += 1
            ##Title
            article_title.append(item['title'])
            st.write("**Title:** %s" % article_title[i])
            
            ##Link
            article_link.append(item['link'])
            st.write("**Link:** %s" %article_link[i])

            ##Publishing Date
            if item['published'] is None: 
                publishing_date.append(get_article_content(item['link'])[1])
            else:
                publishing_date.append(item['published'])

            st.write("**Published Date:** %s" % str(publishing_date[i]))

            ##Complete Content
            article_content.append(get_article_content(item['link'])[0])

            ##Image
            article_image.append(get_article_content(item['link'])[2])
            try:
                 image = Image.open(requests.get(article_image[i], stream=True).raw)
                 res = requests.get(article_image[i])
                 res.raise_for_status()
                 st.image(image, width=500)

            except UnidentifiedImageError:
                 st.write("**No Image Provided**")
            except requests.exceptions.MissingSchema:
                 st.write("**No Image Provided**")

            ##Summary of the article
            get_article_content_display(item['link']) 

            ##Keywords
            article_keywords.append(get_article_content(item['link'])[3])
            st.write("**Keywords:** %s" % article_keywords[i])

            st.write("-------------------------------------------------------------------------------------")    

            i=i+1
        else:
            break
     
    articles_dict = {'ID': article_num,'title':article_title,'time':publishing_date,'keywords':article_keywords,'data_source':"news_article",'category':disaster_event,'country':name,'source_URL':article_link,'body':article_content,'language':lang}

    df = pd.DataFrame(articles_dict)
    return df


##Streamlit is used to build the frontend.
##Input keywords to be searched
country_name = []
language = []
##Title
st.title("News Article Scraping Tool")

number_of_articles = st.slider('Select the number of articles to be viewed')

disaster_event = st.selectbox('Enter Disaster Type',('Flood', 'Drought'))

country_name = st.multiselect('Select the countries', options= country_codes['Country'].to_list())

language = st.multiselect('Select the languages', options= language_codes['Language'].to_list())


## Input The Date Inputs
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
start_date = st.date_input('Start Date:', today)
end_date = st.date_input('End Date:', tomorrow)
if start_date < end_date:
    st.success('Start date: `%s`\n\nEnd date: `%s`' % (start_date, end_date))
else:
    st.error('Error: End date must fall after start date.')



##Find links and titles (Calls Backend Functions)
if st.button('Find Articles'):
    final_result = pd.DataFrame()
    
    for name in country_name:

        st.write(name)
        country_code_final = country_codes[country_codes['Country'] == name]['Alpha-2 code'].values[0]

        for lang in language:
            st.write(lang)
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
    final_result.to_csv("Scraped_news_articles_for"+str(keywords)+'.csv')    
    



        
##End        

