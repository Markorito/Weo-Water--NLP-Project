# Streamlit app

## Running the app

To run the app locally, make sure the to install the dependencies listed in `requirements.txt`
and run the `streamlit` command:

```
pip install -r requirements.txt
streamlit run app.py
```

Alternatively, you can run the app in a Docker container, using the following commands:

```
docker build -t app .
docker run -p 8080:8080 app
```

Either way, the streamlit app should be accessible via http://localhost:8080.
# Uploaing Image at Google cloud 

Add following line code to deploy docker image at cloud
```
gcloud app deploy app.yaml
```
Access the applictaion through following command 

```
gcloud app browse -s app
```
This above line of code will share weblink to access application through web browser
