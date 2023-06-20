import redis
import threading


def start_chat_client(session_id, username):
    r = redis.Redis()
    pubsub = r.pubsub()
    pubsub.subscribe(session_id)

    def handle_messages():
        for message in pubsub.listen():
            if message['type'] == 'message':
                print(f"{message['data'].decode()}")

    threading.Thread(target=handle_messages).start()

    while True:
        message = input("")
        message = f"{username}: {message}"
        r.publish(session_id, message)


if __name__ == '__main__':
    session_id = input("Enter session ID: ")
    username = input("Enter your username: ")
    start_chat_client(session_id, username)
