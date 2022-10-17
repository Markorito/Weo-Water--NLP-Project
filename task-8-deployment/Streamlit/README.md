# WEO-Water ground truth app

This web app provides a frontend for finding ground truths about floods and
droughts via news articles and social media posts on the internet for a given
country and time period. This process has three steps:

1. **Scraping:** Find potentially relevant texts from news articles and social
   media posts.
2. **Classification:** Filter out irrelevant texts with natural language processing.
3. **Geoparsing:** Find geographic locations in the texts. This is used for
   filtering out texts about irrelevant locations and for providing geographical
   coordinates.


## Setup

There are two options to run the app:

### Running the Streamlit app with Docker Compose (Option 1, recommended)

The easiest way to run the app is to use Docker Compose
(this requires installing Docker and Docker Compose first):

```
docker compose build
docker compose up
```

Docker Compose also takes care of running the CLIFF server required for
geoparsing and downloading the models.

After running the commands above, the Streamlit app should be accessible with a
web browser via http://localhost:8080.

### Running the Streamlit app in a local environment (Option 2)

First, the geoparsing has to be set up. It is provided by
[CLIFF](https://github.com/mediacloud/cliff-annotator). CLIFF needs to run as a
server. The easiest way to do do that, is to run it in a Docker container:

```
docker pull rahulbot/cliff-clavin
docker run -p 8081:8080 -m 8G -d rahulbot/cliff-clavin
```

This will run the CLIFF server so it can be accessed via
http://localhost:8081.  (We are using port 8081 so it does not conflict with
the Streamlit app, which will run on port 8080.)

To run the Streamlit app locally, make sure the to install **Python 3.8** (or
**Python 3.7**) and the dependencies listed in `requirements.txt`, download the
models, and run the `streamlit` command:

```
pip install -r requirements.txt
python src/download_models.py
streamlit run app.py -- --cliff=http://localhost:8081
```

The last argument to Streamlit has to be the URL to a running CLIFF server, see
above. After running these commands, the Streamlit app should be accesible with
a web browser via http://localhost:8080.


## Information for users

### Input

The app needs the following information from the user to be able to find
relevant ground truths:

* **Disaster type:** Flood or drought. This implies the keywords to be searched
  on the internet and the classifier to use.
* **Number of texts to be scraped:** How many text the classifier and geoparser
  should analyze. For news articles, 30 is usually a good number. For tweets, it
  may make sense to use more if there are a lot of results being discarded by
  the classifier.
* **Data source:** Which source of texts to scrape. There are the following options:
  - **Newspaper:** Articles from various news websites for the given country, language
    and time window, which can be almost any time in the past.
  - **Twitter:** Tweets for the given country, language and time window, which
  can be almost any time in the past. Depending on the country, time and
  language, it may be necessary to scrape significantly more results than for
  news articles.
  - **Instagram:** Instagram posts for the given country. This requires an
  Instagram API key. Due to limitations of the Instagram API, it is only
  possible to scrape recent posts. Also, only 30 hashtags can be scraped (any
  number of times) per week. These include the keywords in the relevant
  languages (flood or drought), and the country. For example, it may be possible
  to scrape Instagram posts for France, but not for Germany, because the number
  of hashtags was used up for the week.
* **Classifier:** Which NLP model to use for classifying the texts. There are
  three options:
  - **BiLSTM:** This is our most accurate classifier, but it may use a lot of
  CPU time and memory.
  - **Fastai:** A more lightweight classifier that trades accuracy for less
  resource usage.
  - **LSTM:** Better accuracy than Fastai, and more lightweight than BiLSTM.
* **Countries:** The countries for which texts should be found.
* **Languages:** The languages of the texts to be scraped. **Note that only
  English is properly supported.** The scrapers usually work with different
  languages, but the classifier was only trained for English, giving bad results
  for other languages. While the geoparser supports other languages, it is
  currently configured for English.
* **Start data and end date:** The beginning and end of the desired time window.
  Note that this corresponds to the publication of the text, which is not
  necessarily the time of the corresponding disaster event.


### Output

Given the user input, texts from the chosen source are scraped for the relevant
country and time. The results are refined with the classifier ("Is this text about
the relevant type of disaster?") and geoparsing ("Does this text mention the
right countries?"). Each of these filters can be disabled with the corresponding
checkbox. (This is sometimes useful to understand why so many results are
filtered out.)

The final results are displayed in a table with the following columns:
* **Score:** Relevancy score from the classifier, a number between `0` and `1`.
  A score of `1` means the classifier thinks the text is about the chosen
  disaster type, `0` means it's not. Numbers in between represent the confidence
  of the classifier.  The results are sorted by this score, and results with
  less than `0.5` are not shown by default.
* **Countries:** Countries extracted from the text by the geoparser. The
  geoparser tries to guess which countries the text is about, based on how often
  locations from the respective countries are mentioned. By default, texts that
  are not about the countries specified by the user are not displayed.
* **Source:** The source of the text. Contains link with the URL where the text
  was found.
* **Text:** The beginning of the text. Only the first 100 characters are displayed.
* **Locations:** The locations mentioned in the text, how often they are
  mentioned, and their geographical coordinates. Only the two most mentioned
  locations are displayed. This column is populated by the geoparser.

More details can be found in the CSV output, which can be downloaded by clicking
the button below the table. The CSV output contains the unabridged columns and
any additional columns specific to the data source.


## Information for developers

### Project structure
You'll see the following directories:
* `data` - This is where any data artifacts your app needs can live. Note that
  if you're using large datasets, you should look at storing them with a cloud
  storage provider of your choice.
* `src` - It's a good idea to try and separate out your 'frontend' code from
  your 'backend' code -- it can really help with debugging your app and can make
  the app easier to extend too. Try and keep useful 'backend' code (e.g.
  standard data transformations) in here.
* `tests` - testing code for the application


### About the files in the top-level directory

* `app.py` - This is your Streamlit App code and acts as an entry point for your
  app. You can build other bits and pieces elsewhere if you're working on a
  complex app, but just make sure this is where your app is 'knitted together'.
* `requirements.txt` - This file contains your app's requirements -- the
  packages you need to get it all running. Makes sure to keep this up-to-date.
* `Dockerfile` - This file defines the image used to build the container your
  app is going to deploy into. By default, it runs with Python 3.8, and will
  install the packages you provide in requirements.txt, too. When your container
  is running locally, it'll expose your app at http://localhost:8080.
* `docker-compose.yml` - This file defines how the Streamlit app (see
  `Dockerfile`) runs in concert with the CLIFF server. Docker Compose uses this
  to setup Docker containers for each, and to define their network interface.
* `app.yaml` - For Google App Engine. This file specifies how URL paths
  correspond to request handlers and static files. The `app.yaml` file also
  contains information about your app's code, such as the runtime and the latest
  version identifier.
* `README.md` - This file describes your app. Make sure to update this.


### Training the models

Right now, the trained models for classification are stored in Google Drive, see
`download_models.py`. Training the models is outside the scope of this app.

The code that was used for training the models can be found in the
`task-2-nlp-modeling/models` folder.


### Deploying to Google Cloud Platform

Inside the Google Cloud shell, go to this folder and run the following command
to deploy the app as a Docker image:
```
gcloud app deploy app.yaml
```
You can then access the application through following command:
```
gcloud app browse -s app
```
This will share a weblink to access application through a web browser.

Note that you still have to make the CLIFF server available to the app.
You can also run Docker Compose on GCP, which simplifies this step.

As part of the WEO-Water Omdena project, deploying the Streamlit app with the
fastai classifier on GCP was successfully tested. Deploying the CLIFF server on
GCP, or deploying it with the app using Docker Compose on GCP was **not**
tested.

### Upgrading dependencies

The required Python packagess are given in `requirements.txt`. Any pinned
version there can be upgraded manually, but breaking changes in the newer
version may reqiure fixing the code.

The Python runtime can be upgraded as well by editing the `Dockerfile`. We tested
the app with Python 3.7 and Python 3.8. Python 3.9 does not work at the moment,
because we use the Python library `pygooglenews`, which does not support
Python 3.9 yet. This may be fixed upstream, or by forking `pygooglenews` and
upgrading its `feedparser` dependency (see
[this issue](https://github.com/kurtmckee/feedparser/issues/201)).

