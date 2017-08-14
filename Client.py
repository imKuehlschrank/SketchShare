import sys
import socket
import select

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
            socket_list = [sys.stdin, self.s]

            # Get the list sockets which are readable
            ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

            for sock in ready_to_read:
                # incoming message from remote server, s
                if sock == self.s:
                    data = sock.recv(4096)
                    if not data:
                        break
                    else:
                        print(data.decode(), end='')

                # user entered a message
                else:
                    msg = sys.stdin.readline()
                    self.s.send(str(msg).encode())
                    self.data = None
                    sys.stdout.flush()


if __name__ == "__main__":
    client = Client()
    client.run()
