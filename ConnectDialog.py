import tkinter as tk


class ConnectDialog(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.wm_title("Connect")

        self.resizable(False, False)  # set the connect window to be non - resizable

        self.user_label = tk.Label(self, text="Username: ")
        self.user_entry = tk.Entry(self)
        self.user_label.grid(column=0, row=0, sticky=tk.W)
        self.user_entry.grid(column=1, row=0)

        self.room_label = tk.Label(self, text="Room: ")
        self.room_entry = tk.Entry(self)
        self.room_label.grid(column=0, row=1, sticky=tk.W)
        self.room_entry.grid(column=1, row=1)

        self.join_button = tk.Button(self, text="Join", command=self.connect)
        self.join_button.grid(row=2, columnspan=2)

    def connect(self):
        print("something")
        return False
