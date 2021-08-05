import sys
import json
from socket import AF_INET, SOCK_STREAM, socket
import time

CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
CLIENT_SOCK.connect(('localhost', 8010))
MSG = "Привет, Сервер! Это я Клиент! Как слышно? Прием..."
CLIENT_SOCK.send(MSG.encode('utf-8'))
DATA = CLIENT_SOCK.recv(4096)
print(f"Сообщение от Сервера: {DATA.decode('utf-8')}. Длинна сообщения: {len(DATA)} байт")
CLIENT_SOCK.close()
