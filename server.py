import redis
import threading


def start_chat_server(session_id):
    r = redis.Redis()
    pubsub = r.pubsub()
    pubsub.subscribe(session_id)

    print(f"Chat server started for session: {session_id}")

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
        message = input("Enter your message: ")
        r.publish(session_id, message)


if __name__ == '__main__':
    session_id = input("Enter session ID: ")
    start_chat_server(session_id)
