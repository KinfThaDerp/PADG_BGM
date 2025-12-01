import tkinter as tk
import tkintermapview
from libmap import controller as ctrl
from libmap import model

availableStates = ("Disable","Login", "Map")
appState = availableStates[1]



def logIn(window):
    global appState
    appstate = availableStates[2]
    window.destroy()

def logOut(window):
    global appState
    appstate = availableStates[1]
    window.destroy()

def loginWindow():
    root_log = tk.Tk()
    root_log.title("Okno Logowania")
    root_log.geometry("300x300")

    button_login = tk.Button(root_log, text="Login", command=lambda: logIn(root_log))
    button_login.pack()

    root_log.mainloop()
    global appState
    appState = availableStates[0]

def mapWindow():
    root_map = tk.Tk()
    root_map.title("Okno Map")
    root_map.geometry("1280x720")

    button_logot = tk.Button(root_map, text="Log out", command=lambda: logOut(root_map))
    button_logot.pack()

    root_map.mainloop()
    global appState
    appState = availableStates[0]

while True:
    if appState == availableStates[0]:
        break
    elif appState == availableStates[1]:
        loginWindow()
    elif appState == availableStates[2]:
        mapWindow()

