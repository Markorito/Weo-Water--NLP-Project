import pandas as pd
import streamlit as st

from src.newspaper_scraping import Newspaper_agent
from src.instagram_scraping import Instagram_agent
from src.twitter_scraping import Twitter_agent
from tokens import IG_ACCESS_TOKEN, IG_CLIENT_ID, IG_CLIENT_SECRET

country_codes = pd.read_csv("data/country_codes.csv")
language_codes = pd.read_csv("data/language_codes.csv")
gn_data = pd.read_csv("data/gn_supported.csv", index_col=0)


class Query:
    def __init__(
        self,
        start_date,
        end_date,
        location,
        event_type,
        scraper_type,
        languages,
        number_of_articles,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.event_type = event_type
        self.scraper_type = scraper_type
        self.languages = languages
        self.number_of_articles = number_of_articles


class Scraper:
    def __init__(self, query: Query):
        self.query = query

    def scrape(self) -> pd.DataFrame:
        final_result = []
        if self.query.scraper_type.lower() == "newspaper":
            for name in self.query.location:
                country_code_final = country_codes[country_codes["Country"] == name][
                    "Alpha-2 code"
                ].values[0]
                for language in self.query.languages:
                    language_code_final = language_codes[
                        language_codes["Language"] == language
                    ]["language_code"].values[0]
                    if language_code_final not in gn_data["Language_code"].to_list():
                        language_code_final = "en"
                        st.warning(
                            "**There are no news articles available in this language.**"
                            "**Displaying the results in Default Language and Country Setting.**"
                        )
                    if self.query.event_type.lower() == "flood":
                        keyword_final = gn_data.loc[
                            gn_data.Language_code == language_code_final,
                            "Flood_keyword",
                        ].values[0]
                    elif self.query.event_type.lower() == "drought":
                        keyword_final = gn_data.loc[
                            gn_data.Language_code == language_code_final,
                            "Drought_keyword",
                        ].values[0]
                    keywords = str(str(name) + " " + str(keyword_final))
                    newspaper = Newspaper_agent(
                        self.query,
                        keywords,
                        country_code_final,
                        language_code_final,
                        name,
                        language,
                    )
                    news_results_list = newspaper.get_news_links()
                    if news_results_list is not None and len(news_results_list) > 0:
                        final_result.append(news_results_list)
            return pd.concat(final_result) if len(final_result) > 0 else None

        elif self.query.scraper_type.lower() == "instagram":
            agent = Instagram_agent(
                IG_ACCESS_TOKEN,
                IG_CLIENT_ID,
                IG_CLIENT_SECRET,
            )

            return pd.concat(
                [
                    agent.getAtLeastNMediaFromHashtag(location, 50)
                    for location in self.query.location
                ]
            ).rename(columns=dict(caption="body"))

        elif self.query.scraper_type.lower() == "twitter":
            return pd.concat(
                [
                    Twitter_agent(
                        keyword=self.query.event_type.lower(),
                        location=location,
                        start_date=self.query.start_date,
                        end_date=self.query.end_date,
                        min_n_tweets=max(self.query.number_of_articles, 1000),
                        ).get_tweets()
                    for location in self.query.location
                ]
            )

        else:
            st.error("Scraper not supported")
            return
