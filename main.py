import tkinter as tk
import tkintermapview
from libmap import controller as ctrl
from libmap import model

availableStates = ("Disable","Login", "Map")
appState = availableStates[1]



def logIn(window):
    global appState
    appState = availableStates[2]
    window.destroy()

def logOut(window):
    global appState
    appState = availableStates[1]
    window.destroy()

def loginWindow():
    global appState
    appState = availableStates[0]
    root_log = tk.Tk()
    root_log.title("Okno Logowania")
    root_log.geometry("300x300")

    frame_formularz = tk.Frame(root_log)
    frame_formularz.pack(pady=50)

    button_login = tk.Button(root_log, text="Login", command=lambda: logIn(root_log))
    button_login.pack()

    label_Username = tk.Label(frame_formularz, text="Username: ")
    label_Username.grid(row=0,column=0)
    entry_Username = tk.Entry(frame_formularz)
    entry_Username.grid(row=0, column=1)

    label_Password = tk.Label(frame_formularz, text="Password: ")
    label_Password.grid(row=1, column=0)
    entry_Password = tk.Entry(frame_formularz)
    entry_Password.grid(row=1, column=1)


    root_log.mainloop()


def mapWindow():
    global appState
    appState = availableStates[0]
    root_map = tk.Tk()
    root_map.title("Okno Map")
    root_map.geometry("1280x720")

    button_logot = tk.Button(root_map, text="Log out", command=lambda: logOut(root_map))
    button_logot.pack()

    root_map.mainloop()


while appState != availableStates[0]:
    if appState == availableStates[1]:
        loginWindow()
    elif appState == availableStates[2]:
        mapWindow()

