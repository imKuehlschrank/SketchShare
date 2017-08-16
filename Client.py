import socket
import queue

HOST = 'localhost'
PORT = 8888


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        self.data = None
        self.draw_queue = queue.Queue(maxsize=0)


    def run(self):
        while True:
            data = self.s.recv(4096)
            if not data:
                break
            else:
                self.draw_queue.put(data.decode())

    def write_from_queue(self, q):
        a = q.get()
        self.s.send(a.encode())

    def put_in_draw_queue(self,q):
        while True:
           q.put(self.draw_queue.get())


if __name__ == "__main__":
    client = Client()
    print('[OK] Client')
    client.run()
