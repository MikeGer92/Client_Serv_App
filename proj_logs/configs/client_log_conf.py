import logging
import os
import sys
import logging.handlers

sys.path.append('../')

PATH = os.path.dirname(os.path.abspath(__file__))

PATH = os.path.join(PATH, '../logs/client.log')

CLIENTS_LOGGER = logging.getLogger('client')

asctime = '%(asctime)s'
levelname = '%(levelname)s'
message = '%(message)s'
filename = '%(filename)s'

CLIENTS_FILE_HANDLER = logging.FileHandler(PATH, encoding='utf8')

CLIENTS_FORMATTER = logging.Formatter(f'{asctime} - {levelname} - {filename} - {message}')
# FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

CLIENTS_FILE_HANDLER.setFormatter(CLIENTS_FORMATTER)

CLIENTS_LOGGER.addHandler(CLIENTS_FILE_HANDLER)
CLIENTS_LOGGER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    CLIENTS_LOGGER.critical('Критическая ошибка')
    CLIENTS_LOGGER.error('Ошибка')
    CLIENTS_LOGGER.debug('Отладочная информация')
    CLIENTS_LOGGER.info('Информационное сообщение')
    STREAM_HANDLER = logging.StreamHandler()
    STREAM_HANDLER.setFormatter(CLIENTS_FORMATTER)
    CLIENTS_LOGGER.addHandler(STREAM_HANDLER)
