import tkinter as tk
from tkinter import Frame

import tkintermapview
from libmap import controller as ctrl
from libmap.model import voivoideships

# ─── Window Directions ─────────────────────────────────────────────────────────

available_states = ("Disable", "Login", "Register", "Map")
app_state = available_states[1]

def change_app_state(window, state:int):
    global app_state
    if 0<=state<=len(available_states):
        app_state = available_states[state]
        window.destroy()
    else:
        raise Exception("Failed to change App State!")

def go_to_login(window):
    change_app_state(window, 1)
def go_to_registry(window):
    change_app_state(window, 2)
def go_to_map(window):
    change_app_state(window, 3)

# ─── Account Handlers ─────────────────────────────────────────────────────────

def reset_password():
    tk.messagebox.showwarning(title="Warning!", message="You currently cannot reset passwords.\nPlease contact an administrator.",)


def handle_register(root, **entries):
    success, message = ctrl.register_account(
        username=entries["username"].get().strip(),
        email=entries["email"].get().strip(),
        password=entries["password"].get().strip(),
        confirm_password=entries["confirm_password"].get().strip(),

        # kwargs
        phone=entries["phonenumber"].get().strip() if entries.get("phonenumber") else None,
        voivoideship=entries["voivoideship"].get().strip() if entries.get("voivoideship") else None,
        city=entries["city"].get().strip() if entries.get("city") else None,
        street=entries["street"].get().strip() if entries.get("street") else None,
        building=entries["building"].get().strip() if entries.get("building") else None,
        apartment=entries["apartment"].get().strip() if entries.get("apartment") else None,
    )

    if success:
        tk.messagebox.showinfo("Success", message)
        go_to_login(root)
    else:
        tk.messagebox.showerror("Error", message)

def handle_login(root, **entries):
    success, message = ctrl.login_account(
        username=entries["username"].get().strip(),
        password=entries["password"].get().strip(),
    )

    if success:
        tk.messagebox.showinfo("Success", message)
        go_to_map(root)
    else:
        tk.messagebox.showerror("Error", message)

# ─── Windows ───────────────────────────────────────────────────────────────

def login_window():
    global app_state
    app_state = available_states[0]
    root_log = tk.Tk()
    root_log.title("Mapbook - Login")
    root_log.geometry("300x300")

    frame_formularz = tk.Frame(root_log)
    frame_formularz.pack(pady=50)

    label_username = tk.Label(frame_formularz, text="Username: ")
    label_username.grid(row=0,column=0)
    entry_username = tk.Entry(frame_formularz)
    entry_username.grid(row=0, column=1)

    label_password = tk.Label(frame_formularz, text="Password: ")
    label_password.grid(row=1, column=0)
    entry_password = tk.Entry(frame_formularz, show="*")
    entry_password.grid(row=1, column=1)

    button_login = tk.Button(frame_formularz,
                             text="Login",
                             command=lambda: handle_login(
                                 root_log,
                                 username=entry_username,
                                 password=entry_password
                             ))
    button_login.grid(row=2, column=1, sticky="WE")

    button_reset_password = tk.Button(frame_formularz, text="Reset Password", command=lambda: reset_password())
    button_reset_password.grid(row=2, column=0, sticky="WE")

    button_register = tk.Button(frame_formularz, text="Register", command=lambda: go_to_registry(root_log))
    button_register.grid(row=2, column=2, sticky="WE")

    root_log.mainloop()
    print()

def register_window():
    global app_state
    app_state = available_states[0]
    root_register = tk.Tk()
    root_register.title("Mapbook - Register")
    root_register.geometry("400x400")

    frame_registry = tk.Frame(root_register)
    frame_registry.pack(pady=30)

    label_registry = tk.Label(frame_registry, text="Registry Form")
    label_registry.grid(row=0, column=0, columnspan=2)

    label_username = tk.Label(frame_registry, text="Username: ")
    label_username.grid(row=1, column=0, sticky=tk.W)
    entry_username = tk.Entry(frame_registry)
    entry_username.grid(row=1, column=1)

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

    button_cancel = tk.Button(frame_registry, text="Cancel", command=lambda: go_to_login(root_register))
    button_cancel.grid(row=12,column=0,sticky="WE",pady=10)
    button_register = tk.Button(frame_registry,
                                text="Register",
                                command=lambda: handle_register(
                                    root_register,
                                    username=entry_username,
                                    email=entry_email,
                                    password=entry_password,
                                    confirm_password=entry_confirm_password,

                                    phonenumber=entry_phonenumber,
                                    voivoideship=selected_voivoideship,
                                    city=entry_city,
                                    street=entry_street,
                                    building=entry_building,
                                    apartment=entry_apartment,
                                ))
    button_register.grid(row=12,column=1, sticky="WE",pady=10)

    root_register.mainloop()

def map_window():
    global app_state
    app_state = available_states[0]

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
        command=lambda: go_to_login(root_map))
    button_logout.grid(row=0, column=0, sticky="e", padx=10, pady=5)

    map_widget = tkintermapview.TkinterMapView(root_map)
    map_widget.grid(row=1, column=0, sticky="nsew")
    map_widget.set_position(52.229722, 21.011667 )
    map_widget.set_zoom(6)

    root_map.mainloop()



while app_state != available_states[0]:
    if app_state == available_states[1]:
        login_window()
    elif app_state == available_states[2]:
        register_window()
    elif app_state == available_states[3]:
        map_window()

