FROM python:3.10
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./app/ ./app
CMD python -m app.core_api; gunicorn -b 0.0.0.0:8050 app.app:server
