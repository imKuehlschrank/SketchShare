import socket
import threading
import select

HOST = 'localhost'
PORT = 8888
CONNECTIONS = []


class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.s.listen(10)

    def client_thread(self, conn, addr):
        for client in CONNECTIONS:
            # msg = '%s joined the room\n' % str(addr)
            # client.sendall(msg.encode())
            pass

        while True:
            data = conn.recv(4096)
            # reply = '%s %s' % (addr, data.decode())
            reply = '%s' % (data.decode())

            print(reply)

            if not data:
                break

            for client in CONNECTIONS:
                if client != conn:
                        client.sendall(reply.encode())

    def run(self):
        while True:
            conn, addr = server.s.accept()
            msg = '%s joined the room' % str(addr)
            print(msg)
            CONNECTIONS.append(conn)
            t = threading.Thread(target=server.client_thread, args=(conn, addr))
            t.daemon = True
            t.start()
        server.s.close()


if __name__ == '__main__':
    server = Server()
    print('[OK] Server')
    server.run()
