FROM python:alpine as dependencies

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

FROM dependencies as main

RUN pip install gunicorn

COPY app ./app

ENV FLASK_APP app
ENV FLASK_ENV production

CMD gunicorn --bind "0.0.0.0:$PORT" "app:create_app()"
