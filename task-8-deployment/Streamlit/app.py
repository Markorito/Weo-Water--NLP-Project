import argparse
import streamlit as st
import datetime
import pandas as pd
import html
from collections import Counter

from download_button import download_button
from query import Scraper, Query
from src.nlp import FastaiModel, BiLSTM_Model, LSTM_Model
from src.utils import standard_date_format
from src.geoparser import GeoParser

@st.cache
def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the WEO-Water Ground Truth App"
    )
    parser.add_argument("--cliff", required=False,
        help="URL where the CLIFF server is running")
    args = parser.parse_args()
    return args

args = parse_args()

@st.cache
def read_csv_data():
    country_codes = pd.read_csv("data/country_codes.csv")
    language_codes = pd.read_csv("data/language_codes.csv")
    gn_data = pd.read_csv("data/gn_supported.csv", index_col=0)
    return country_codes, language_codes, gn_data

country_codes, language_codes, gn_data = read_csv_data()

# title of application
st.title("WEO-Water Ground Truth App")

# disaster type
event_type = st.selectbox("Enter disaster type", ("Flood", "Drought"))

# no. of texts to be scraped
number_of_articles = st.slider("Select the number of texts to be scraped",
    min_value=10, value=30, max_value=1000, step=10)

col1, col2 = st.beta_columns(2)
scraper_type = col1.selectbox("Select data source", ("Newspaper", "Instagram", "Twitter"))
Classification_Model = col2.selectbox("Select Classifier", ("BiLSTM", "Fastai", "LSTM"))

# country name
country_name = st.multiselect(
    "Select the countries", options=country_codes["Country"].to_list()
)

# language input
languages = st.multiselect(
    "Select language/s", options=language_codes["Language"].to_list(),
    default=["English"]
)

if languages != ["English"]:
    st.warning("Only **English** is supported by the classifier. Use other languages at your own risk!")

# Input The Date Inputs
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
# the accepted format for dates in pygooglenews is %Y-%m-%d https://github.com/kotartemiy/pygooglenews#quickstart
col1, col2 = st.beta_columns(2)
start_date = standard_date_format(col1.date_input("Start date:", today))
end_date = standard_date_format(col2.date_input("End date:", tomorrow))

# validate dates
if not (start_date <= end_date):
    st.error("Error: End date must fall after start date.")

@st.cache(show_spinner=False, allow_output_mutation=True)
def load_model():
    """Load the right model into memory."""
    try:
        if Classification_Model == "Fastai":
            model = FastaiModel(scraper_type + '_' + event_type, event_type)
        elif Classification_Model == "BiLSTM":
            model = BiLSTM_Model(scraper_type + '_' + event_type + '.pt', event_type, scraper_type)
        elif Classification_Model == "LSTM":
            model = LSTM_Model(scraper_type + '_' + event_type + '.h5', event_type, scraper_type)
    except AttributeError:
        # This happens if the model cannot be unpickled due to a version mismatch
        model = None
    except RuntimeError:
        # This happens if pytorch fails to read the zip archive
        model = None
    return model

model = load_model()

if model:
    st.write("Loaded classifier:", model.model_name)
else:
    st.write("Could not load classifier.")

query = Query(
    start_date=start_date,
    end_date=end_date,
    location=country_name,
    event_type=event_type,
    scraper_type=scraper_type,
    languages=languages,
    number_of_articles=number_of_articles,
)

# Initialize geoparsing
@st.cache(show_spinner=False)
def get_geoparser(args):
    if not args.cliff:
        return None

    geo = GeoParser(args.cliff)
    # Test geoparsing and disable it if it doesn't work

    try:
        geo.parse_text('New York City')
    except:
        geo = None
    return geo

geo = get_geoparser(args)

def get_scraped_data(query):
    scraper = Scraper(query)
    data = scraper.scrape()

    if data is None:
        return None

    # different scrapers return cols with different names for the same thing ..let's fix that
    if len(data) != 0:
        data.rename(
            columns=dict(
                source_URL='url',
                permalink='url',
                media_type='data_source',
                timestamp = 'time'
            ),
            inplace=True
        )

    # limit to the requested number of items
    if len(data) > number_of_articles:
        data = data.iloc[:number_of_articles]

    # Some models are trained on the title + body
    if scraper_type == "Newspaper":
        data['body_with_title'] = data['title'] + ' ' + data['body']
    else:
        data['body_with_title'] = data['body']

    return data

# Define column used by classifier
if scraper_type == "Newspaper" and Classification_Model == 'Fastai':
    text_col = 'title'
elif scraper_type == "Newspaper" and Classification_Model == 'BiLSTM':
    # BiLSTM model trained on article title and body both combined
    text_col = 'body_with_title'
else:
    text_col = 'body'

def classify(data, model):
    if model and Classification_Model == 'Fastai':
        df_preds = model.get_predictions_df(
            data[text_col], with_original_inputs=True
        )
        data["score"] = df_preds["1"]
        data.sort_values(by="score", ascending=False, inplace=True)
    elif model:
        df_preds = model.get_predictions_df(
            data[text_col], scraper_type, event_type, with_original_inputs=True
        )
        data["score"] = df_preds["score"]
        data.sort_values(by="score", ascending=False, inplace=True)
    else:
        data["score"] = float('nan')
    return data

def geoparse(data):
    if geo:
        # Get focus countries of text
        data["countries"] = data["body_with_title"].map(
            lambda b: list(map(
                lambda c: c['countryCode'],
                geo.parse_text(b, demonyms=True).get_countries()
            )) if b else None)
        # Get all locations mention in the text
        data["locations"] = data["body_with_title"].map(
            lambda b: list(map(
                lambda loc: (loc['name'], (loc['lat'], loc['lon'])),
                geo.parse_text(b, demonyms=True).get_locations()
            )) if b else None)
        # Count how often each location is mentioned
        data["locations"] = data["locations"].map(
            lambda loc: Counter(loc).most_common() if loc else None
        )
    else:
        data["countries"] = None
        data["locations"] = None
    return data

def find_ground_truths():
    with st.spinner("Scraping..."):
        data = get_scraped_data(query)

    if data is None or len(data) == 0:
        st.write("No results found.")
        return None

    with st.spinner("Classifying..."):
        data = classify(data, model)

    # Get geographic locations from `body_with_title`
    with st.spinner("Extracting geographic locations from text..."):
        data = geoparse(data)

    return data

if st.button("Find ground truths"):
    st.session_state.ground_truths = find_ground_truths()

def country_name_to_code(name):
    return country_codes[country_codes['Country'] == name]['Alpha-2 code'].iat[0]

def country_code_to_name(name):
    return country_codes[country_codes['Alpha-2 code'] == name]['Country'].iat[0]

if ('ground_truths' in st.session_state and
    st.session_state.ground_truths is not None and
    len(st.session_state.ground_truths) > 0):
    filtered_df = st.session_state.ground_truths.copy()

    col1, col2 = st.beta_columns(2)
    # Filter out texts predicted not to be about disasters
    if col1.checkbox("Filter texts with low scores", value=True):
        mask = filtered_df["score"] >= 0.5
        n_relevant = mask.sum()
        col1.write("Classification filtered out {} of {} results.".format(
            len(filtered_df) - n_relevant, len(filtered_df)
        ))
        filtered_df = filtered_df[mask]

    # Filter out texts not mentioning any of our target countries
    if geo and col2.checkbox("Filter texts not mentioning any target country", value=True):
        target_countries = set(map(country_name_to_code, country_name))
        mask = filtered_df["countries"].map(
            lambda c: bool(set(c).intersection(target_countries)))
        n_relevant = mask.sum()
        col2.write("Geoparsing filtered out {} of {} results.".format(
            len(filtered_df) - n_relevant, len(filtered_df)
        ))
        filtered_df = filtered_df[mask]

    st.write("**Output: ground truths**")
    # Streamlit's formatting options for `st.table` and `st.write` are
    # extremely limited. Therefore, we just create an HTML table instead.
    rows = [
        "<table>",
        "<tr><th>score</th><th>countries</th><th>time</th><th>source</th><th>text</th><th>locations</th></tr>",
    ]

    for i in range(len(filtered_df)):
        r = filtered_df.iloc[i]

        # Truncate text if it's too long
        text = r[text_col][:100] + ("..." if len(r[text_col]) > 100 else "")
        # Escape text to avoid issues with HTML
        text = html.escape(text)
        # Remove newlines to avoid breaking the HTML table
        text = text.replace("\n", "")

        # Create an anchor for the link
        anchor = r.get('data_source', query.event_type)

        # Format list of countries
        countries_str = (', '.join(country_code_to_name(c) for c in r.countries)
            if r.countries else '')

        # Show how often each location is mentioned
        cutoff = 2
        locations_str = (',<br>'.join(
                f"{count}× {name} ({lat}, {lon})"
                for (name, (lat, lon)), count
                in r.locations[:cutoff])
            if r.locations else '')
        if locations_str and len(r.locations) > 2:
            locations_str += ', ...'

        # create row
        rows.append(f"<tr><td>{r.score:.2}</td><td>{countries_str}</td><td>{r.time}</td><td><a href=\"{r.url}\">{anchor}</a></td><td>{text}</td><td>{locations_str}</td></tr>")
    rows.append("</table>")

    st.markdown("\n".join(rows), unsafe_allow_html=True)
    st.markdown(
        "<br>" + download_button(filtered_df, "ground_truths.csv", "Download results as CSV"),
        unsafe_allow_html=True
    )
