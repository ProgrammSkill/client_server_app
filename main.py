import json
import threading
from client_upd import UDPClient
from server_upd import UDPServer


if __name__ == "__main__":
    # Запуск UDP-сервера
    server = UDPServer()
    server_thread = threading.Thread(target=server.listen)
    server_thread.start()

    # ЗапускUDP-клиента
    client = UDPClient()

    # Пример данных
    data = {
        "location": {"latitude": 55.7558, "longitude": 37.6173},
        "movement": {"speed": 50, "direction": "north"}
    }
    json_data = json.dumps(data)
    client.send_data(json_data)

    # Закрываем клиента
    client.close()