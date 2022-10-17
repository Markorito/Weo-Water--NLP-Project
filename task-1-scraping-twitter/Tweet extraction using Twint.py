# !pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint

import twint

c = twint.Config()
c.Search = "#floods"
c.Limit = 10000
c.Format = 'Tweet id: {id} | Date: {date} | Time: {time} | Tweet: {tweet} | Location: {place}'
c.Store_csv = True
c.Output = r"C:\Users\DEBJYOTI BANERJEE\Downloads\extracted_tweets.csv"
c.Lang = "en"
# c.Translate = True
# c.TranslateDest = "it"
twint.run.Search(c)