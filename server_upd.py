# Класс UDP-сервера
import json
import socket
from collections import defaultdict
import struct
from config import MESSAGE_HEADER_SIZE


def parse_message(message):
    """Парсит информационное сообщение."""
    header = message[:MESSAGE_HEADER_SIZE]
    data = message[MESSAGE_HEADER_SIZE:]
    marker, message_id, data_size = struct.unpack('!HII', header)
    return message_id, data_size, data


class UDPServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.data_buffer = defaultdict(list)  # Словарь для хранения частей сообщений

    def listen(self):
        """Слушает входящие сообщения."""
        print(f'UDP-сервер запущен на {self.host}:{self.port}')
        while True:
            data, addr = self.sock.recvfrom(1024)
            message_id, data_size, payload = parse_message(data)
            self.data_buffer[message_id].append(payload)

            # Проверка, пришли ли все части сообщения
            if len(self.data_buffer[message_id]) == data_size:
                json_data = ''.join(self.data_buffer[message_id])
                try:
                    data = json.loads(json_data)
                    print(f'Получены данные: {data}')
                except json.JSONDecodeError:
                    print(f'Ошибка декодирования JSON: {json_data}')
                del self.data_buffer[message_id]