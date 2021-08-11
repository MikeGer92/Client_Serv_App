import logging
import os
import sys
import logging.handlers


PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, '../logs/server.log')


SERVERS_LOGGER = logging.getLogger('server')

asctime = ('%(asctime)s')
levelname = ('%(levelname)s')
message = ('%(message)s')
filename = '%(filename)s'

SERVERS_FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')

SERVERS_FORMATTER = logging.Formatter(f'{asctime} - {levelname} - {filename} - {message}')
#FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

SERVERS_FILE_HANDLER.setFormatter(SERVERS_FORMATTER)

SERVERS_LOGGER.addHandler(SERVERS_FILE_HANDLER)
SERVERS_LOGGER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    PATH = os.path.join('../logs', 'server.log')
    SERVERS_LOGGER.critical('Критическая ошибка')
    SERVERS_LOGGER.error('Ошибка')
    SERVERS_LOGGER.debug('Отладочная информация')
    SERVERS_LOGGER.info('Информационное сообщение')
    STREAM_HANDLER = logging.StreamHandler()
    STREAM_HANDLER.setFormatter(SERVERS_FORMATTER)
    SERVERS_LOGGER.addHandler(STREAM_HANDLER)
