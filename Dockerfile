FROM python:3.9

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y redis-server
RUN pip install -r requirements.txt

CMD redis-server --daemonize yes