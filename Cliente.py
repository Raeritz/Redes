import socket
import pickle
import psutil
import platform
import time

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.id = platform.node()

    def get_system_info(self):
        cpu_count = psutil.cpu_count(logical=True)
        ram = psutil.virtual_memory().available / (1024 ** 3)
        disk = psutil.disk_usage('/').free / (1024 ** 3) 

        # Tratamento de erro para temperatura

        return {
            'id': self.id,
            'cpu': cpu_count,
            'ram': ram,
            'disk': disk,
        }

    def send_data(self):
        while True:
            try:
                data = self.get_system_info()
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((self.server_ip, self.server_port))
                    sock.send(pickle.dumps(data))
                    response = sock.recv(4096)
                    print(pickle.loads(response))
            except Exception as e:
                print(f"Erro ao enviar dados: {e}")
            time.sleep(10000)  # Envia dados a cada 10 segundos

if __name__ == "__main__":
    client = Client('10.25.3.23', 5000) 
    client.send_data()