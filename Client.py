import socket

# inspiration from
# http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php

HOST = 'localhost'
PORT = 8888


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        self.data = None

    def run(self):
        while True:
            data = self.s.recv(4096)
            if not data:
                break
            else:
                print(data.decode())

    def write_from_queue(self, q):
        a = q.get()
        self.s.send(a.encode())


if __name__ == "__main__":
    client = Client()
    print('[OK] Client')
    client.run()
