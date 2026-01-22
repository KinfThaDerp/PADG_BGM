import tkinter as tk
from tkinter import messagebox
from libmap import model, controller as ctrl
from libmap.views import LoginView, RegisterView, MapView


class MapBookApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mapbook by BGM")
        self.geometry("1280x720")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.current_user_id = None

        for F in (LoginView, RegisterView, MapView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        if hasattr(frame, 'on_show'):
            frame.on_show()

    def login(self, username, password):
        success, message, account_id = ctrl.login_account(username, password)
        if success:
            self.current_user_id = account_id
            model.set_account(account_id)
            self.show_frame("MapView")
        else:
            messagebox.showerror("Login Error", message)

    def logout(self):
        self.current_user_id = None
        model.set_account(None)
        self.show_frame("LoginView")