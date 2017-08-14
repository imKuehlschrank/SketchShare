import socket
import threading

# inspiration from
# http://www.binarytides.com/python-socket-server-code-example/

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
            msg = '%s joined the room\n' % str(addr)
            client.sendall(msg.encode())

        while True:
            data = conn.recv(4096)

            reply = '%s %s' % (addr, data.decode())
            print(reply, end='')  # log everything on server

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
            threading.Thread(target=server.client_thread, args=(conn, addr)).start()
        server.s.close()


if __name__ == '__main__':
    server = Server()
    print('[OK] Server')
    server.run()
