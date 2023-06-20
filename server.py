import redis
import threading


def start_chat_server(session_id):
    r = redis.Redis()
    pubsub = r.pubsub()
    pubsub.subscribe(session_id)

    def handle_messages():
        for message in pubsub.listen():
            if message['type'] == 'message':
                # Отправляем сообщение всем клиентам, кроме отправителя
                sender = message['data'].decode().split(':')[0]
                clients = r.smembers(session_id)
                for client in clients:
                    if client.decode() != sender:
                        r.publish(client, message['data'])

    threading.Thread(target=handle_messages).start()

    while True:
        message = "Empty"
        r.publish(session_id, message)


if __name__ == '__main__':
    start_chat_server(0)
