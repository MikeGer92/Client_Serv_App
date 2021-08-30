import argparse
import json
import logging
import sys
import socket
import time
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from proj_logs.configs import client_log_conf
from common.utils import get_message, send_message, get_correct_time
from decors import log, Log

sys.path.append('../')

CLIENTS_LOGGER = logging.getLogger('client')


@Log()
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: get_correct_time(time.time()),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


@log
def process_ans(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError

#Получение параметров с помощью парсера параметров
Log()
def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('address', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, nargs='?')
    return parser


def main():
    # client.py 192.168.1.185 8020
    # client_work.py  192.168.82.108 8050
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_adr = namespace.address
    server_port = namespace.port

    try:
        # server_address = sys.argv[1]
        server_address = server_adr
        # server_port = int(sys.argv[2])
        server_port = int(server_port)
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        CLIENTS_LOGGER.critical(f'Запуск клиента с неверным номером порта')
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        CLIENTS_LOGGER.debug('Выход из приложения')
        sys.exit(1)

    CLIENTS_LOGGER.info('Старт клиента')
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))

    message_to_server = create_presence()
    CLIENTS_LOGGER.info(f'Сформировано сообщение для {server_address}')
    send_message(transport, message_to_server)
    CLIENTS_LOGGER.info(f'Сообщение для {server_address} успешно отправлено')
    try:
        answer = process_ans(get_message(transport))
        CLIENTS_LOGGER.info(f'Получен ответ от {server_address}')
        print(answer)
    except (ValueError, json.JSONDecodeError):
        CLIENTS_LOGGER.critical('Ошибка декодирования сообщения')
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
