# Класс UDP-клиента
import socket
import struct
from config import MARKER, MAX_DATA_SIZE


# Функции для работы с сообщениями
def create_message_header(message_id, data_size):
    """Создает заголовок сообщения."""
    header = struct.pack('!HII', MARKER, message_id, data_size)
    return header


def create_message(message_id, data):
    """Создает информационное сообщение."""
    data_size = len(data)
    header = create_message_header(message_id, data_size)
    message = header + data
    return message

# Функция для разделения JSON-строки на части
def split_json_data(json_data, max_data_size):
    """Разделяет JSON-строку на части заданного размера."""
    parts = []
    offset = 0
    while offset < len(json_data):
        part = json_data[offset:offset + max_data_size]
        parts.append(part)
        offset += max_data_size
    return parts

class UDPClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.message_id = 1

    def send_data(self, json_data):
        """Отправляет JSON-данные на сервер."""
        data_parts = split_json_data(json_data, MAX_DATA_SIZE)
        for part in data_parts:
            message = create_message(self.message_id, part.encode())
            self.sock.sendto(message, (self.host, self.port))
            self.message_id += 1

    def close(self):
        """Закрывает соединение."""
        self.sock.close()