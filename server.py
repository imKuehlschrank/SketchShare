import socket
import threading
import queue
import time

HOST = 'localhost'
PORT = 8888


class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.s.listen(10)

        self.connections = []
        self.history = []
        self.broadcast_queue = queue.Queue()

    def start(self):
        threading.Thread(target=server.accept_connection_and_spawn_thread, daemon=True).start()
        self.broadcast_forever()

    def accept_connection_and_spawn_thread(self):
        while True:
            conn, addr = self.s.accept()
            print(str(addr), ' joined the room')
            self.connections.append(conn)
            self.send_current_canvas(conn)
            threading.Thread(target=self.client_receive_forever, args=(conn, addr), daemon=True).start()

    def client_receive_forever(self, conn, addr):
        while True:
            data = conn.recv(4096)
            if not data:
                self.close_connection(conn, addr)
                return  # exit from thread

            elem = {'from': conn, 'data': data}
            self.broadcast_queue.put(elem)
            self.log_on_server(conn, addr, data)

    def log_on_server(self, conn, addr, data):
        self.history.append(data.decode())
        print(addr, data.decode())

    def broadcast_forever(self):
        while True:
            elem = self.broadcast_queue.get()
            conn = elem['from']
            data = elem['data']
            for client in self.connections:
                if client != conn:
                    client.sendall(data)

    def send_current_canvas(self, conn):
        for elem in self.history:
            conn.sendall(elem.encode())
            time.sleep(0.001)  # TODO: fix this for the love of god.

    def close_connection(self, conn, addr):
        conn.close()
        self.connections.remove(conn)
        print(addr, " disconnected")


    # -----
    def clear_history(self):
        self.history.clear()

    def kick_all_connected_users(self):
        for cc in self.connections:
            self.close_connection(cc)

if __name__ == '__main__':
    server = Server()
    print('[OK] Server')
    server.start()
