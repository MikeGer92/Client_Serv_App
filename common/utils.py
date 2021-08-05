import json
from common.variables  import MAX_PACKAGE_LENGTH, ENCODING
import time


def get_message(sock):
    encoded_response = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock, message):
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)


def get_correct_time(num):
    time_format = time.strftime('%H:%M:%S %a %d %b %Y', time.gmtime(num))
    print("DateTime:",time_format)