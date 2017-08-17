import socket
import threading

HOST = 'localhost'
PORT = 8888
CONNECTIONS = []



class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.s.listen(10)

    def start(self):
        while True:
            conn, addr = server.s.accept()
            threading.Thread(target=server.client_thread, args=(conn, addr), daemon=True).start()

    def client_thread(self, conn, addr):
        print(str(addr), ' joined the room')
        CONNECTIONS.append(conn)

        while True:
            data = conn.recv(4096)

            if not data:
                print("closing connection: ", addr)
                conn.close()
                CONNECTIONS.remove(conn)
                return  # exit from thread

            for client in CONNECTIONS:
                if client != conn:
                    client.sendall(data)

            print(addr, data.decode())


if __name__ == '__main__':
    server = Server()
    print('[OK] Server')
    server.start()
