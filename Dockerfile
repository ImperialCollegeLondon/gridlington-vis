FROM python:3.9-slim
COPY ./dash/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
CMD gunicorn --reload -b 0.0.0.0:8050 app.app:server
