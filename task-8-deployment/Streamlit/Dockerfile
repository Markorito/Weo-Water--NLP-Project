FROM python:3.8

WORKDIR /app
EXPOSE 8080

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN python -m nltk.downloader punkt stopwords

COPY src/download_models.py .
RUN ["python", "download_models.py"]

COPY . .

# Run the application on port 8080
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0", "--"]
