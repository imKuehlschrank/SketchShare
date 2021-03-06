import socket
import threading

HOST = 'localhost'
PORT = 8888


class Client:
    def __init__(self, send_q, receive_q):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.send_queue = send_q
        self.receive_queue = receive_q

    def start(self):
        self.s.connect((HOST, PORT))
        threading.Thread(target=self.send, daemon=True).start()
        threading.Thread(target=self.receive, daemon=True).start()

    def stop(self):
        self.s.shutdown(socket.SHUT_RDWR)

    def send(self):
        while True:
            self.s.send(self.send_queue.get().encode())

    def receive(self):
        while True:
            data = self.s.recv(4096)
            if not data:
                print("Disconnected")
                break
            else:
                self.receive_queue.put(data.decode())
