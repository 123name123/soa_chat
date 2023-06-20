
FROM python:3.9

RUN pip install -r requirements.txt

COPY chat_server.py /app/chat_server.py
COPY chat_client.py /app/chat_client.py

WORKDIR /app

CMD redis-server --daemonize yes && python chat_server.py