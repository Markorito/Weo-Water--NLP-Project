from pathlib import Path
import requests

MODELS_DIR_FASTAI = Path("./models/FASTAI_Model")
MODELS_DIR_BiLSTM = Path("./models/BiLSTM_Model")
MODELS_DIR_LSTM = Path("./models/LSTM_Model")

FASTAI_MODELS = [
    dict(
        name="Newspaper_Flood",
        event_type="Flood",
        version="2021-07-09",
        gdrive_id="179Iyv2RVSz2qGny35Z5waoDuWdKtPym2",  # 20210709_NewspaperTitle_Flood.pkl
    ),
    dict(
        name="Newspaper_Drought",
        event_type="Drought",
        version="2021-07-09",
        gdrive_id="1rBXejqDDvRjr7i2qdk328nwIFhTY1zKX",  # 20210709_NewspaperTitle_Drought.pkl
    ),
    dict(
        name="Twitter_Flood",
        event_type="Flood",
        version="2021-07-09",
        gdrive_id="116wDwaOCM8BsN2ZsepthYOmyewGUGfO1",  # 2021-07-09_Twitter_Flood_Classifier.pkl
    ),
    dict(
        name="Twitter_Drought",
        event_type="Drought",
        version="2021-07-09",
        gdrive_id="1-8EG_jgoCyA8mQvemXTnVk3gUMNbDBOI",  # 2021-07-09_Twitter_Drought_Classifier
    ),
    dict(
        name="Instagram_Flood",
        event_type="Flood",
        version="2021-07-09",
        gdrive_id="1PhNylTwqPzHnczYnW-RD1U0fjkhHKhjW",  # 2021-07-09_Instagram_Flood_classifier
    ),
    dict(
        name="Instagram_Drought",
        event_type="Drought",
        version="2021-07-09",
        gdrive_id="1aRM3dl7_hXlPOlc1SqbdS_EtvnXij9sl",  # 2021-07-09_Instagram_Drought_classifier
    )
]

BiLSTM_MODELS = [
    dict(
        name="Newspaper_Flood.pt",
        scraper_type = "Newspaper",
        event_type="Flood",
        version="2021-07-13",
        gdrive_id="12d20j6DXwta0JwQ9Z0ncHTde31mi2MSZ",
    ),
    dict(
        name="Newspaper_embedding_matrix_Flood.npy",
        scraper_type = "Newspaper",
        event_type="Flood",
        version="2021-07-13",
        gdrive_id="1GMf_4dWXd-ntjGXyxP9u1GUsPkT94n6p",
    ),
    dict(
        name="Newspaper_tokenizer_Flood.pkl",
        scraper_type = "Newspaper",
        event_type="Flood",
        version="2021-07-13",
        gdrive_id="18_yvdakHmHfzXVIa1SbHO4lA46Upcwod",
    ),
    dict(
        name="Newspaper_Drought.pt",
        scraper_type = "Newspaper",
        event_type="Drought",
        version="2021-07-13",
        gdrive_id="1WghhsrDtd_wAbQI1vux8tLrmc79nZmHm",
    ),
    dict(
        name="Newspaper_embedding_matrix_Drought.npy",
        scraper_type = "Newspaper",
        event_type="Drought",
        version="2021-07-13",
        gdrive_id="1uLYAXWg9Uz1ewV0z_9LBncaxEjgvuXKG",
    ),
    dict(
        name="Newspaper_tokenizer_Drought.pkl",
        scraper_type = "Newspaper",
        event_type="Drought",
        version="2021-07-13",
        gdrive_id="1UW8S0DkyKa7htFig5ee1XXngOjycnxnz",
    ),
    dict(
        name="Instagram_Flood.pt",
        scraper_type = "Instagram",
        event_type="Flood",
        version="2021-07-13",
        gdrive_id="1mtk85_IpOF6XPEh4jZOfgE3xp2EJacQc",
    ),
    dict(
        name="Instagram_embedding_matrix_Flood.npy",
        scraper_type = "Instagram",
        event_type="Flood",
        version="2021-07-13",
        gdrive_id="1QfdJcJlYcpadtryC-_2ZlFWMQO9MnrnE",
    ),
    dict(
        name="Instagram_tokenizer_Flood.pkl",
        scraper_type = "Instagram",
        event_type="Flood",
        version="2021-07-13",
        gdrive_id="1yEpDLtxKu-SmPNegCp64s9QpCV67EDuV",
    ),
    dict(
        name="Instagram_Drought.pt",
        scraper_type = "Instagram",
        event_type="Drought",
        version="2021-07-13",
        gdrive_id="1iKbKJ0FlUhB2ap2LChlSwStXxi56G-DM",
    ),
    dict(
        name="Instagram_embedding_matrix_Drought.npy",
        scraper_type = "Instagram",
        event_type="Drought",
        version="2021-07-13",
        gdrive_id="1tqBS1wVFYpa4j4-2UfgDjYSTC6Q0dnIV",
    ),
    dict(
        name="Instagram_tokenizer_Drought.pkl",
        scraper_type = "Instagram",
        event_type="Drought",
        version="2021-07-13",
        gdrive_id="1D8J0Txd_3VeFabdgb2Piho-SpzvMsvNQ",
    ),
    dict(
        name="Twitter_Flood.pt",
        scraper_type = "Twitter",
        event_type="Flood",
        version="2021-07-13",
        gdrive_id="16o8Sn4Ftv9D_SiEJz0UsUburIlQKihgJ",
    ),
    dict(
        name="Twitter_embedding_matrix_Flood.npy",
        scraper_type = "Twitter",
        event_type="Flood",
        version="2021-07-13",
        gdrive_id="1zs771QRlsy7foY2gbYs2CaeeD9RSDgzJ",
    ),
    dict(
        name="Twitter_tokenizer_Flood.pkl",
        scraper_type = "Twitter",
        event_type="Flood",
        version="2021-07-13",
        gdrive_id="1SiqMletnDZiRyCP_7GEq2tsRr7tLLpC_",
    ),
    dict(
        name="Twitter_Drought.pt",
        scraper_type = "Twitter",
        event_type="Drought",
        version="2021-07-13",
        gdrive_id="1oCrkUtz2h0c0_prLgL2q25xO2ELqR8Vr",
    ),
    dict(
        name="Twitter_embedding_matrix_Drought.npy",
        scraper_type = "Twitter",
        event_type="Drought",
        version="2021-07-13",
        gdrive_id="1f86YqDxA7Wkh8K57QUua6eW-nyofXqXG",
    ),
    dict(
        name="Twitter_tokenizer_Drought.pkl",
        scraper_type = "Twitter",
        event_type="Drought",
        version="2021-07-13",
        gdrive_id="10a6fUHjiPLQ-CUj2sztgNQ0lRHgYwUPL",
    )
]

LSTM_MODELS = [
    dict(
        name = "Newspaper_Flood.h5",
        scraper_type = "Newspaper",
        event_type = "Flood",
        version = "2021-07-15",
        gdrive_id = "1ofrgClRDcn2OIoUwbU6aZ-fkOKMU5RJi",
    ),
    dict(
        name = "Newspaper_tokenizer_Flood.pkl",
        scraper_type = "Newspaper",
        event_type = "Flood",
        version = "2021-07-15",
        gdrive_id = "1lh0UoC4eLE_0vDjLvKI0RMIW9vBNCNQS",
    ),
    dict(
        name = "Newspaper_Drought.h5",
        scraper_type = "Newspaper",
        event_type = "Drought",
        version = "2021-07-15",
        gdrive_id = "1Jdlcj2yD2oeKPhTTH-KBlzF2IGoIzveY",
    ),
    dict(
        name = "Newspaper_tokenizer_Drought.pkl",
        scraper_type = "Newspaper",
        event_type = "Drought",
        version = "2021-07-15",
        gdrive_id = "123Zjk5YGIC1I-tz0V0RVNh6hMh0oIRi_",
    ),
    dict(
        name = "Instagram_Flood.h5",
        scraper_type = "Instagram",
        event_type = "Flood",
        version = "2021-07-15",
        gdrive_id = "1xbAmuiEPYadWjm9jyoDWwuTyb2Qcv__Y",
    ),
    dict(
        name = "Instagram_tokenizer_Flood.pkl",
        scraper_type = "Instagram",
        event_type = "Flood",
        version = "2021-07-15",
        gdrive_id = "12_LVHLCJdpTHq3RE4xgY7oo-i3ohigRS",
    ),
    dict(
        name = "Instagram_Drought.h5",
        scraper_type = "Instagram",
        event_type = "Drought",
        version = "2021-07-15",
        gdrive_id = "1qnXH1Rxn7C_CPN0zodF4EciLianAdCdo",
    ),
    dict(
        name = "Instagram_tokenizer_Drought.pkl",
        scraper_type = "Instagram",
        event_type = "Drought",
        version = "2021-07-15",
        gdrive_id = "1hU4MkwqNQbLou82WFZQwZ3VHMLcY2mmy",
    ),
    dict(
        name = "Twitter_Flood.h5",
        scraper_type = "Twitter",
        event_type = "Flood",
        version = "2021-07-27",
        gdrive_id = "1yJU-1vleP_FKr98UvbRlTYs8qqEbqp2a",
    ),
    dict(
        name = "Twitter_tokenizer_Flood.pkl",
        scraper_type = "Twitter",
        event_type = "Flood",
        version = "2021-07-15",
        gdrive_id = "1JNSSfrptFTPdvXRbCN-ULVHXTJv4MqNA",
    ),
    dict(
        name = "Twitter_Drought.h5",
        scraper_type = "Twitter",
        event_type = "Drought",
        version = "2021-07-27",
        gdrive_id = "14HnOnsWWTrACbnkbcqulzS7g856-ZRtO",
    ),
    dict(
        name = "Twitter_tokenizer_Drought.pkl",
        scraper_type = "Twitter",
        event_type = "Drought",
        version = "2021-07-15",
        gdrive_id = "1IUqr7AOBNCy_VA9dffCLb571MqiCMB_D",
    )
]

def download_file_from_google_drive(id: str, destination: str):
    """
    Downloads a publicly-accessible file from Google Drive
    See https://bit.ly/3gliBne

    id: the id fo the file (eg from the sharable link)
    destination: path where to store the downloaded file
    """

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={"id": id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)
    save_response_content(response, destination)


def download_model(gdrive_id: str, save_dest: Path):
    """
    Downloads model stored in google drive.

    gdrive_id: the id fo the file (eg from the sharable link)
    save_dest: path (dir/filename.extension) where to store the downloaded file
    """
    save_dest.parent.mkdir(exist_ok=True, parents=True)
    if not save_dest.exists():
        download_file_from_google_drive(gdrive_id, save_dest)

def download_classifiers_from_gdrive() -> None:
    """
    Downloads all fastai models from GDrive.
    """
    for model in FASTAI_MODELS:
        # download to file
        save_dest = MODELS_DIR_FASTAI / model["name"]
        download_model(model["gdrive_id"], save_dest)

    for model in BiLSTM_MODELS:
        # download to file
        save_dest = MODELS_DIR_BiLSTM / model["name"]
        download_model(model["gdrive_id"], save_dest)
        
    for model in LSTM_MODELS:
        # download to file
        save_dest = MODELS_DIR_LSTM / model["name"]
        download_model(model["gdrive_id"], save_dest)

if __name__ == '__main__':
    download_classifiers_from_gdrive()
