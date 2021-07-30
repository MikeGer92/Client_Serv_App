import json
import sys
import socket
from common.utils import *


# CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
# CLIENT_SOCK.connect(('localhost', 8010))
# MSG = "Привет, Сервер! Это я Клиент! Как слышно? Прием..."
# CLIENT_SOCK.send(MSG.encode('utf-8'))
# DATA = CLIENT_SOCK.recv(4096)
# print(f"Сообщение от Сервера: {DATA.decode('utf-8')}. Длинна сообщения: {len(DATA)} байт")
# CLIENT_SOCK.close()


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {RESPONSE: 400, ERROR: 'Bad Request'}




def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p')+1])
        else:
            listen_port = DEFAULT_PORT
        if 1024 < listen_port or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра порта - \'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print('В качестве порта может быть указано только целое число в диапазоне от 1024 до 65535')
        sys.exit(1)
    try:
        if '-a' in sys.argv:
            listen_address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            listen_address = ''
    except IndexError:
        print('После параметра порта - \'a\' необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))


    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорректное сообщение от клиента')
            client.close()


if __name__ == '__main':
    main()