import socket
import pickle
import threading

class Server:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.clients = {}

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.port}")
        while True:
            client_sock, client_addr = self.sock.accept()
            print(f"Conexão estabelecida com {client_addr}")
            threading.Thread(target=self.handle_client, args=(client_sock,)).start()

    def handle_client(self, client_sock):
        try:
            # Recebe os dados do cliente
            data = client_sock.recv(4096)
            if not data:
                print("Nenhum dado recebido")
                return

            # Desserializa os dados
            try:
                client_data = pickle.loads(data)
            except pickle.PickleError as e:
                print(f"Erro ao dados do cliente: {e}")
                client_sock.send(pickle.dumps("Dados inválidos"))
                return

            # Verifica se os dados contêm as chaves esperadas
            if not all(key in client_data for key in ['id', 'cpu', 'ram', 'disk']):
                print(f"Dados incompletos ou inválidos recebidos de {client_data.get('id', 'Desconhecido')}")
                client_sock.send(pickle.dumps("Dados incompletos ou inválidos."))
                return

            # Armazena os dados do cliente
            self.clients[client_data['id']] = client_data
            print(f"Dados recebidos de {client_data['id']}: {client_data}")

            # Envia uma confirmação de volta ao cliente
            client_sock.send(pickle.dumps("Dados recebidos com sucesso!"))
        except Exception as e:
            print(f"Erro ao processar dados do cliente: {e}")
        finally:
            client_sock.close()

    def list_clients(self):
        return self.clients

    def get_client_details(self, client_id):
        return self.clients.get(client_id, None)

    def calculate_averages(self):
        if not self.clients:
            return None
        cpu_avg = sum(client['cpu'] for client in self.clients.values()) / len(self.clients)
        ram_avg = sum(client['ram'] for client in self.clients.values()) / len(self.clients)
        disk_avg = sum(client['disk'] for client in self.clients.values()) / len(self.clients)
        return {
            'cpu_avg': cpu_avg,
            'ram_avg': ram_avg,
            'disk_avg': disk_avg,
        }

if __name__ == "__main__":
    server = Server()
    server.start()