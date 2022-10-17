# Task 4: Scraping News Articles

The purpose of this task is to create a scraping tool for retrieving news articles related to a particular disaster event from the internet.

Link to task summaries - [here](https://drive.google.com/drive/folders/1q5-RXg991nKYBEI5B2Ihqfuh8J_MA8bE)

Meeting Recordings - [here](https://drive.google.com/drive/folders/1D98918kgUwlDSA1y24DJrP1X4vKhejGJ)

**Subtasks -**
1. **Subtask 1** - Get news articles for events mentioned in the [glide dataset](https://github.com/OmdenaAI/WeoWater/blob/main/task-7-data-collection-historical-events/glide_historical_events.csv) using the scraper [code](https://github.com/OmdenaAI/WeoWater/blob/main/task-4-scraping-newspapers/scraping_news_from_historical_data.ipynb) and store it [here](https://github.com/OmdenaAI/WeoWater/tree/main/task-4-scraping-newspapers/output_to_clean). We have used pygooglenews and newspaper3k python libraries for the same.
2. **Subtask 2** - Automate scraping tool(Dataset creation for building the NLP model) 
3. **Subtask 3** - Scraping tool for the final application.
4. **Subtask 4** - Front-end tool using streamlit. 
5. **Subtask 5** - Manual labelling of news articles(relevant or irrelevant). Articles stored in this [folder](https://github.com/OmdenaAI/WeoWater/tree/main/task-4-scraping-newspapers/labelled_data).
6. **Subtask 6** - Translation tool 

Directions to use the newspaper article scraper on local machine- 
1. Open the file [newspaper_article_scaper.py](https://github.com/OmdenaAI/WeoWater/blob/main/task-4-scraping-newspapers/newspaper_article_scraper.py)
2. Run this command in the terminal - `streamlit run newspaper_article_scaper.py`
3. The application will open in a browser tab. Enter all the event details. **Note** - First letter for the country name should be capital.(e.g. India, Egypt, etc.)
4. The search results will be stored in a file named **'country_name.csv'** or **'state_name.csv'**
  
You can find the demonstration video of the news articles scraper [here](https://drive.google.com/file/d/1KRJbvX06p8_yBLFNEt98vtWfkqbAPsiK/view?usp=sharing). 
