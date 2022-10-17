from textblob import TextBlob
import streamlit as st
import pandas as pd
import datetime

#defining global variables
country_codes = pd.read_csv('./data/country_codes.csv')
language_codes = pd.read_csv('./data/language_codes.csv')

##Title
def setup_front_end():
    st.title("News Article Scraping Tool")

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

    return disaster_event, country_name, language, start_date, end_date