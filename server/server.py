import socket
import logging
import sys
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from proj_logs.configs import server_log_conf
from common.utils import get_message, send_message
from decors import Log

sys.path.append('../')

SERVERS_LOGGER = logging.getLogger('server')

@Log()
def process_client_message(message):

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            SERVERS_LOGGER.critical(f'Попытка запуска с неверным номером порта')
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        SERVERS_LOGGER.critical('Не указан номер порта')
        sys.exit(1)
    except ValueError:
        SERVERS_LOGGER.critical('Неверный номер порта')
        print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        SERVERS_LOGGER.critical('Не указан адрес клиента')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    transport.listen(MAX_CONNECTIONS)
    SERVERS_LOGGER.info('Старт сервера')
    while True:
        client, client_address = transport.accept()
        SERVERS_LOGGER.info(f'Соединение с клиентом {listen_address} выполнено')
        try:
            message_from_cient = get_message(client)
            SERVERS_LOGGER.info(f'Получено сообщение от {client}')
            print(message_from_cient)
            response = process_client_message(message_from_cient)
            SERVERS_LOGGER.info(f'Ответ для {client} сформирован')
            send_message(client, response)
            SERVERS_LOGGER.info(f'Ответ для {client} успешно отправлен')
            SERVERS_LOGGER.debug(f'Соединение с {client} закрывается')
            client.close()
        except (ValueError, json.JSONDecodeError):
            SERVERS_LOGGER.warning(f'Сообщение от {client} прочитать не удалось')
            print('Принято некорретное сообщение от клиента.')
            client.close()
            SERVERS_LOGGER.debug(f'Соединение с {client} закрыто')



if __name__ == '__main__':
    main()
