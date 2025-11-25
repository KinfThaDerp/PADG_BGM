import tkinter, tkintermapview
from libmap import controller as ctrl
from libmap import model

availableStates = ("Disable","Login", "Map")
appState = availableStates[1]

def logIn(window):
    window.destroy()


def loginWindow():
    root_log = tkinter.Tk()
    root_log.title("Okno Logowania")
    root_log.geometry("300x300")

    button_login = tkinter.Button(root_log, text="Login", command=lambda: print("Loggin in..."))
    button_login.pack()

    root_log.mainloop()
    global appState
    appState = availableStates[2]

def mapWindow():
    root_map = tkinter.Tk()
    root_map.title("Okno Map")
    root_map.geometry("1280x720")

    button_logot = tkinter.Button(root_map, text="Log out", command=lambda: print("Loggin out..."))
    button_logot.pack()

    root_map.mainloop()
    global appState
    appState = availableStates[1]

while True:
    if appState == availableStates[0]:
        break
    elif appState == availableStates[1]:
        loginWindow()
    elif appState == availableStates[2]:
        mapWindow()

