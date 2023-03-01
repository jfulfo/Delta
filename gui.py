import tkinter as tk 

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("My App")
        self.geometry("400x400")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Hello World")
        self.label.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
