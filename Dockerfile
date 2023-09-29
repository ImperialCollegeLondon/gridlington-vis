FROM python:3.10
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./app/ ./app
CMD python app/core_api.py; gunicorn --reload -b 0.0.0.0:8050 app.app:server
