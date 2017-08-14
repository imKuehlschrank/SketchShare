import os
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import pickle
import ConnectDialog as connectDialog
import SimpleDropbox as DropboxWrapper


class Sketch(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # self.resizable(False, False)  # set the connect window to be non - resizable
        self.remote_storage = DropboxWrapper.SimpleDropbox('qvT2K9jz3CsAAAAAAAAGM128w_rmQFr6MUstpTnpVE99I6vzqzLpzEUFVqeXFdzn')

        # Data
        self.username = "fil"
        self.partner = "ana"

        self.history = []
        self.undo_list = []
        self.redo_list = []

        self.line_width = 5
        self.color = 'black'
        self.background_color = 'white'
        self.bg_img = None
        self.brush_color = self.color
        self.eraser_color = self.background_color
        self.cwd = os.getcwd()

        self.old_x = None
        self.old_y = None

        # self.overrideredirect(True)   # remove the window border

        # row 0
        self.menubar = tk.Menu(self, relief='flat')

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="Open (Ctrl+o)", command=self.open_pkl)
        menu.add_command(label="Save (Ctrl+s)", command=self.save_pkl)
        menu.add_command(label="Export as PostScript", command=self.save_to_pdf)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menu)
        menu.add_command(label="Undo (Ctrl+z)", command=self.undo)
        menu.add_command(label="Redo (Ctrl+r)", command=self.redo)
        menu.add_command(label="Clear Canvas", command=self.clear_canvas)
        menu.add_command(label="Add Background Image", command=self.bg_image_dialog)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Toolbox", menu=menu)
        menu.add_command(label="Use Brush (b)", command=self.use_brush)
        menu.add_command(label="Use Eraser (e)", command=self.use_eraser)
        menu.add_command(label="Change Brush Color (c)", command=self.choose_color)
        menu.add_command(label="Change Brush/Eraser Size (s)", command=self.choose_size)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Network", menu=menu)
        menu.add_command(label="Join", command=self.setup_connection)
        menu.add_command(label="Exit", command=self.setup_connection)
        menu.add_command(label="Push", command=lambda: self.push(str('/' + self.username + '.pkl')))
        menu.add_command(label="Pull partner", command=lambda: self.pull(str('/' + self.partner + '.pkl')))
        menu.add_command(label="Pull mine", command=lambda: self.pull(str('/' + self.username + '.pkl')))
        self.tk.call(self, "config", "-menu", self.menubar)

        # row 1
        self.canvas = tk.Canvas(self, cursor="pencil", bg=self.background_color, width=500, height=600)
        self.canvas.grid(row=1, columnspan=4)

        # row 2
        self.label_me = tk.Label(self, text="Not Connected")
        self.label_me.grid(row=2, column=3, sticky=tk.E)

        self.setup_event_listeners()

    # ---------------------- Draw on canvas ----------------------
    def press(self, event):
        self.old_x = event.x
        self.old_y = event.y

    def drag(self, event):
        obj = Line(self.old_x, self.old_y, event.x, event.y)
        obj.draw_on_canvas(self.canvas, self.line_width, self.color)

        self.history.extend([self.old_x, self.old_y, event.x, event.y, self.line_width, self.color])
        self.old_x = event.x
        self.old_y = event.y

    def release(self, event):
        self.old_x = None
        self.old_y = None

    def draw_on_canvas(self, data, is_show_strokes=False):
        for x1, y1, x2, y2, width, color in zip(*[iter(data)]*6):
            self.history.extend([x1, y1, x2, y2, width, color])
            Line(x1, y1, x2, y2).draw_on_canvas(self.canvas, width, color)
            if is_show_strokes:
                self.canvas.update()

    # ---------------------- File ----------------------
    def save_to_pdf(self):
        filename = asksaveasfilename(defaultextension='.ps')
        self.canvas.postscript(file=filename, colormode='color')

    def save_pkl(self):
        filename = asksaveasfilename()
        with open(filename, 'wb') as f:
            pickle.dump(self.history, f)

    def open_pkl(self):
        filename = askopenfilename()
        dat = pickle.load(open(filename, 'rb'))
        self.clear_canvas()
        self.history.clear()
        self.draw_on_canvas(dat, is_show_strokes=False)

    # ---------------------- Edit ----------------------
    def undo(self):
        for i in range(1, 10):  # un/redo in blocks of 10
            l = self.canvas.find_all()
            self.canvas.delete(l[-1:])
            to_undo = self.history[-6:]
            del self.history[-6:]  # 6 ... number of elements that describe one stroke element(x1,y1,x2,y2,color,width)
            self.undo_list.extend(to_undo)

    def redo(self):
        for i in range(1, 10):  # un/redo in blocks of 10
            to_redo = self.undo_list[-6:]
            del self.undo_list[-6:]
            self.draw_on_canvas(to_redo)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.history.clear()

    def bg_image_dialog(self):
        filename = askopenfilename()
        self.set_bg_image(filename)

    def update_line_width(self, val):
        self.line_width = val

    # ---------------------- Toolbox ----------------------
    def choose_size(self):
        dialog = tk.Toplevel(self)
        line_width_button = tk.Scale(dialog, from_=1, to=50, orient=tk.HORIZONTAL,
                                     label="Brush Size", command=self.update_line_width)
        line_width_button.set(self.line_width)
        ok_button = tk.Button(dialog, text='OK', command=dialog.destroy)
        line_width_button.grid(row=0, column=0)
        ok_button.grid(row=1)

    def choose_color(self):
        self.brush_color = askcolor(color=self.color)[1]
        self.color = self.brush_color

    def use_eraser(self):
        self.color = self.eraser_color
        self.canvas.config(cursor='rtl_logo')

    def use_brush(self):
        self.color = self.brush_color
        self.canvas.config(cursor='pencil')

    # ---------------------- Dropbox stuff ----------------------
    def pull(self, filename):
        self.remote_storage.download_file_to_machine(self.cwd + filename, filename)
        dat = pickle.load(open(self.cwd + filename, 'rb'))
        self.clear_canvas()
        self.history.clear()
        self.draw_on_canvas(dat, is_show_strokes=True)

    def push(self, filename):
        with open(self.cwd + filename, 'wb') as f:
            pickle.dump(self.history, f)
        self.remote_storage.upload_file(self.cwd + filename, filename)
        os.remove(self.cwd + filename)

    def set_bg_image(self, path_to_img):
        self.bg_img = tk.PhotoImage(file=path_to_img)
        self.canvas.create_image(250, 250, image=self.bg_img)

    def setup_connection(self):
        connectDialog.ConnectDialog()

    def setup_event_listeners(self):
        # Draw on Canvas
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<ButtonPress-1>', self.press)
        self.canvas.bind('<ButtonRelease-1>', self.release)

        # Shortcuts
        self.bind("<Control-z>", lambda _: self.undo())
        self.bind("<Control-r>", lambda _: self.redo())
        self.bind("<Control-o>", lambda _: self.open_pkl())
        self.bind("<Control-s>", lambda _: self.save_pkl())
        self.bind("s", lambda _: self.choose_size())
        self.bind("c", lambda _: self.choose_color())
        self.bind("b", lambda _: self.use_brush())
        self.bind("e", lambda _: self.use_eraser())


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw_on_canvas(self, canvas, line_width, color):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=line_width, fill=color,
                           capstyle=tk.ROUND, joinstyle=tk.ROUND, smooth=True, splinesteps=200)


if __name__ == "__main__":
    app = Sketch()
    app.wm_title("Sketching")
    app.mainloop()
