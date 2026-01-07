import tkinter as tk
from tkinter import Frame

import tkintermapview
from libmap import controller as ctrl
from libmap.model import voivoideships

availableStates = ("Disable","Login", "Register", "Map")
appState = availableStates[1]

def changeAppState(window, state:int):
    global appState
    if 0<=state<=len(availableStates):
        appState = availableStates[state]
        window.destroy()
    else:
        raise Exception("Failed to change App State!")

def logOut(window):
    changeAppState(window, 1)


def register(window):
    changeAppState(window, 2)

def logIn(window):
    changeAppState(window, 3)

def registerUser(username, email, password):
    return

def resetPassword(window):
    tk.messagebox.showwarning(title="Warning!", message="You currently cannot reset passwords.\nPlease contact an administrator.",)

def loginWindow():
    global appState
    appState = availableStates[0]
    root_log = tk.Tk()
    root_log.title("Mapbook - Login")
    root_log.geometry("300x300")

    frame_formularz = tk.Frame(root_log)
    frame_formularz.pack(pady=50)

    label_Username = tk.Label(frame_formularz, text="Username: ")
    label_Username.grid(row=0,column=0)
    entry_Username = tk.Entry(frame_formularz)
    entry_Username.grid(row=0, column=1)

    label_Password = tk.Label(frame_formularz, text="Password: ")
    label_Password.grid(row=1, column=0)
    entry_Password = tk.Entry(frame_formularz, show="*")
    entry_Password.grid(row=1, column=1)

    button_login = tk.Button(frame_formularz, text="Login", command=lambda: logIn(root_log))
    button_login.grid(row=2, column=1, sticky="WE")

    button_resetPassword = tk.Button(frame_formularz, text="Reset Password", command=lambda: resetPassword(root_log))
    button_resetPassword.grid(row=2, column=0, sticky="WE")

    button_register = tk.Button(frame_formularz, text="Register", command=lambda: register(root_log))
    button_register.grid(row=2, column=2, sticky="WE")

    root_log.mainloop()
    print()

def registerWindow():
    global appState
    appState = availableStates[0]
    root_register = tk.Tk()
    root_register.title("Mapbook - Register")
    root_register.geometry("400x400")

    frame_registry = tk.Frame(root_register)
    frame_registry.pack(pady=30)

    label_registry = tk.Label(frame_registry, text="Registry Form")
    label_registry.grid(row=0, column=0, columnspan=2)

    label_Username = tk.Label(frame_registry, text="Username: ")
    label_Username.grid(row=1, column=0, sticky=tk.W)
    entry_Username = tk.Entry(frame_registry)
    entry_Username.grid(row=1, column=1)

    label_email = tk.Label(frame_registry, text="Email: ")
    label_email.grid(row=2, column=0, sticky=tk.W)
    entry_email = tk.Entry(frame_registry)
    entry_email.grid(row=2, column=1)

    label_password = tk.Label(frame_registry, text="Password: ")
    label_password.grid(row=3, column=0, sticky=tk.W)
    entry_password = tk.Entry(frame_registry, show="*")
    entry_password.grid(row=3, column=1)

    label_confirm_password = tk.Label(frame_registry, text="Confirm Password: ")
    label_confirm_password.grid(row=4, column=0, sticky=tk.W)
    entry_confirm_password = tk.Entry(frame_registry, show="*")
    entry_confirm_password.grid(row=4, column=1)

    label_optional = tk.Label(frame_registry,text="Optional")
    label_optional.grid(row=5, column=0, columnspan=2,pady=10)

    label_phonenumber= tk.Label(frame_registry, text="Phone Number: ")
    label_phonenumber.grid(row=6, column=0, sticky=tk.W)
    entry_phonenumber= tk.Entry(frame_registry)
    entry_phonenumber.grid(row=6, column=1)

    label_voivoideship = tk.Label(frame_registry, text="Voivoideship: ")
    label_voivoideship.grid(row=7, column=0, sticky=tk.W)
    global voivoideships
    selected_voivoideship= tk.StringVar(value="Select")
    entry_voivoideship = tk.OptionMenu(frame_registry, selected_voivoideship, *voivoideships)
    entry_voivoideship.grid(row=7, column=0, sticky=tk.E, columnspan=2)

    label_city = tk.Label(frame_registry, text="City: ")
    label_city.grid(row=8, column=0, sticky=tk.W)
    entry_city = tk.Entry(frame_registry)
    entry_city.grid(row=8, column=1)

    label_street = tk.Label(frame_registry, text="Street: ")
    label_street.grid(row=9, column=0, sticky=tk.W)
    entry_street = tk.Entry(frame_registry)
    entry_street.grid(row=9, column=1)

    label_building = tk.Label(frame_registry, text="Building: ")
    label_building.grid(row=10, column=0, sticky=tk.W)
    entry_building = tk.Entry(frame_registry)
    entry_building.grid(row=10, column=1)

    label_apartment = tk.Label(frame_registry, text="Apartment: ")
    label_apartment.grid(row=11, column=0, sticky=tk.W)
    entry_apartment = tk.Entry(frame_registry)
    entry_apartment.grid(row=11, column=1)

    button_cancel = tk.Button(frame_registry, text="Cancel", command=lambda: logOut(root_register))
    button_cancel.grid(row=12,column=0,sticky="WE",pady=10)
    button_register = tk.Button(frame_registry, text="Register", command=lambda: registerUser(entry_Username,entry_email,entry_password))
    button_register.grid(row=12,column=1, sticky="WE",pady=10)

    root_register.mainloop()

def mapWindow():
    global appState
    appState = availableStates[0]

    root_map = tk.Tk()
    root_map.title("Mapbook")
    root_map.geometry("1280x720")

    root_map.grid_columnconfigure(0, weight=1)
    root_map.grid_rowconfigure(1, weight=1)

    toolbar_frame = Frame(root_map)
    toolbar_frame.grid(row=0,column=0, sticky="EW")
    toolbar_frame.grid_columnconfigure(0, weight=1)

    button_logout = tk.Button(
        toolbar_frame,
        text="Log out",
        command=lambda: logOut(root_map))
    button_logout.grid(row=0, column=0, sticky="e", padx=10, pady=5)

    map_widget = tkintermapview.TkinterMapView(root_map)
    map_widget.grid(row=1, column=0, sticky="nsew")
    map_widget.set_position(52.229722, 21.011667 )
    map_widget.set_zoom(6)

    root_map.mainloop()



while appState != availableStates[0]:
    if appState == availableStates[1]:
        loginWindow()
    elif appState == availableStates[2]:
        registerWindow()
    elif appState == availableStates[3]:
        mapWindow()

