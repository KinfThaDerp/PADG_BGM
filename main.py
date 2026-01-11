import tkinter as tk
from tkinter import Frame

import tkintermapview
from libmap import controller as ctrl, model

#  Window Directors

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
    model.set_account(None)
    change_app_state(window, 1)


def go_to_registry(window):
    change_app_state(window, 2)


def go_to_map(window):
    change_app_state(window, 3)



#  Account Handlers

def reset_password():
    tk.messagebox.showwarning(title="Warning!", message="You currently cannot reset passwords.\nPlease contact an administrator.",)


def handle_register(root, **entries):
    success, message = ctrl.register_account_person(
        username=entries["username"].get().strip(),
        email=entries["email"].get().strip(),
        password=entries["password"].get().strip(),
        confirm_password=entries["confirm_password"].get().strip(),

        # Personal Info
        name=entries["name"].get().strip() if entries.get("name") else None,
        surname=entries["surname"].get().strip() if entries.get("surname") else None,

        # Contact
        phone_number=entries["phonenumber"].get().strip() if entries.get("phonenumber") else None,

        # Location
        city=entries["city"].get().strip() if entries.get("city") else None,
        street=entries["street"].get().strip() if entries.get("street") else None,
        building=entries["building"].get().strip() if entries.get("building") else None,
        apartment=entries["apartment"].get().strip() if entries.get("apartment") else None,
        model=model
    )
    print(model.account_id)

    if success:
        go_to_login(root)
    else:
        tk.messagebox.showerror("Error", message)


def handle_login(root, **entries):
    success, message, account_id = ctrl.login_account(
        username=entries["username"].get().strip(),
        password=entries["password"].get().strip(),
    )

    if success:
        model.set_account(account_id)
        go_to_map(root)
    else:
        tk.messagebox.showerror("Error", message)


#  Windows


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
    root_register.geometry("400x450")

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

    label_optional = tk.Label(frame_registry)
    label_optional.grid(row=5, column=0, columnspan=2,pady=3)


    label_name = tk.Label(frame_registry, text="Name: ")
    label_name.grid(row=6, column=0, sticky=tk.W)
    entry_name = tk.Entry(frame_registry)
    entry_name.grid(row=6, column=0, sticky=tk.E, columnspan=2)

    label_surname = tk.Label(frame_registry, text="Surname: ")
    label_surname.grid(row=7, column=0, sticky=tk.W)
    entry_surname = tk.Entry(frame_registry)
    entry_surname.grid(row=7, column=0, sticky=tk.E, columnspan=2)

    label_phonenumber= tk.Label(frame_registry, text="Phone Number: ")
    label_phonenumber.grid(row=8, column=0, sticky=tk.W)
    entry_phonenumber= tk.Entry(frame_registry)
    entry_phonenumber.grid(row=8, column=1)


    frame_spacing = tk.Frame(frame_registry)
    frame_spacing.grid(row=9, column=0, columnspan=2, pady=3)

    label_city = tk.Label(frame_registry, text="City: ")
    label_city.grid(row=10, column=0, sticky=tk.W)
    entry_city = tk.Entry(frame_registry)
    entry_city.grid(row=10, column=1)

    label_street = tk.Label(frame_registry, text="Street: ")
    label_street.grid(row=11, column=0, sticky=tk.W)
    entry_street = tk.Entry(frame_registry)
    entry_street.grid(row=11, column=1)

    label_building = tk.Label(frame_registry, text="Building: ")
    label_building.grid(row=12, column=0, sticky=tk.W)
    entry_building = tk.Entry(frame_registry)
    entry_building.grid(row=12, column=1)

    label_apartment = tk.Label(frame_registry, text="Apartment: ")
    label_apartment.grid(row=13, column=0, sticky=tk.W)
    entry_apartment = tk.Entry(frame_registry)
    entry_apartment.grid(row=13, column=1)

    button_cancel = tk.Button(frame_registry, text="Cancel", command=lambda: go_to_login(root_register))
    button_cancel.grid(row=14,column=0,sticky="WE",pady=10)
    button_register = tk.Button(frame_registry,
                                text="Register",
                                command=lambda: handle_register(
                                    root_register,
                                    username=entry_username,
                                    email=entry_email,
                                    password=entry_password,
                                    confirm_password=entry_confirm_password,

                                    name=entry_name,
                                    surname=entry_surname,
                                    phonenumber=entry_phonenumber,

                                    city=entry_city,
                                    street=entry_street,
                                    building=entry_building,
                                    apartment=entry_apartment,
                                ))
    button_register.grid(row=14,column=1, sticky="WE",pady=10)

    root_register.mainloop()


def map_window():
    global app_state
    app_state = available_states[0]

    root_map = tk.Tk()
    root_map.title("Mapbook")
    root_map.geometry("1280x720")

    root_map.grid_columnconfigure(1, weight=1)
    root_map.grid_rowconfigure(1, weight=1)

    toolbar_frame = Frame(root_map)
    toolbar_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
    toolbar_frame.grid_columnconfigure(1, weight=1)


    sidebar = LeftToolbar(root_map)
    sidebar.toggle_visibility()

    model.refresh_all()

    toggle_button = tk.Button(
        toolbar_frame,
        text="Show Sidebar",
        command=lambda: [
            sidebar.toggle_visibility(),
            toggle_button.config(text="Show Toolbar" if not sidebar.is_visible else "Hide Toolbar")
        ]
    )
    toggle_button.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    button_logout = tk.Button(
        toolbar_frame,
        text="Log out",
        command=lambda: go_to_login(root_map))
    button_logout.grid(row=0, column=1, sticky="e", padx=10, pady=5)

    map_widget = tkintermapview.TkinterMapView(root_map)
    map_widget.grid(row=1, column=1, sticky="nsew")
    map_widget.set_position(52.229722, 21.011667)
    map_widget.set_zoom(6)

    root_map.mainloop()


class LeftToolbar(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(width=200, bg='lightgray')
        self.grid(row=1, column=0, sticky="ns")
        self.grid_propagate(False)

        self.is_visible = True
        self.current_mode = "Select Mode"
        self.listbox = None

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mode_frame = tk.Frame(self, bg='lightgray')
        self.mode_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        tk.Button(self.mode_frame, text="People", command=lambda: self.switch_mode("People")).pack(side="left", padx=2)
        tk.Button(self.mode_frame, text="Books", command=lambda: self.switch_mode("Books")).pack(side="left", padx=2)
        tk.Button(self.mode_frame, text="Libraries", command=lambda: self.switch_mode("Libraries")).pack(side="left", padx=2)

        self.info_frame = tk.Frame(self, bg='lightgray')
        self.info_frame.grid(row=1, column=0, sticky="ew", padx=5)

        self.current_mode_label = tk.Label(self.info_frame, text=self.current_mode)
        self.current_mode_label.pack(side="left")

        tk.Button(self.info_frame, text="Refresh", command=lambda: model.refresh_all()).pack(side="right")

        self.list_frame = tk.Frame(self, bg='lightgray')
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        self.create_list([])

        self.buttons_frame = tk.Frame(self, bg='lightgray')
        self.buttons_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.items = []


    def switch_mode(self, mode):
        self.current_mode = mode
        self.current_mode_label.config(text=mode)

        self.items = []
        display_items = []
        ids = []

        if mode == "People":
            self.items = model.get_people_list()
            display_items = [
                f"{p['name']} {p['surname']} ({p['role']})"
                for p in self.items
            ]
            ids = [p['id'] for p in self.items]

        elif mode == "Books":
            self.items = model.get_books_list()
            display_items = [
                f"{p['title']} by {p['author']}" for p in self.items
            ]
            ids = [p['id'] for p in self.items]

        elif mode == "Libraries":
            self.items = model.get_libraries_list()
            display_items = [
                f"{p['name']}" for p in self.items
            ]
            ids = [p['id'] for p in self.items]

        self.create_list(display_items, ids)
        self.create_mode_buttons(mode)

    def create_mode_buttons(self, mode):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        for action in ("Add", "Edit", "View Info", "Delete"):
            tk.Button(
                self.buttons_frame,
                text=action,
                command=lambda a=action, m=mode: self.handle_action(m, a)
            ).pack(fill="x", pady=2)

    def handle_action(self, mode, action):
        selected_id = None
        if self.listbox and self.listbox.curselection():
            selected_index = self.listbox.curselection()[0]
            selected_id = self.listbox_ids[selected_index]

        if mode == "People":
            if action == "Add":
                add_person_window(self)
            elif action == "Edit":
                edit_person_window(self, selected_id)
            elif action == "View Info":
                view_person_info_window(self, selected_id)
            elif action == "Delete":
                delete_person_window(self, selected_id)
        elif mode == "Libraries":
            if action == "Add":
                add_library_window(self)
            elif action == "Edit":
                edit_library_window(self, selected_id)
            elif action == "View Info":
                view_library_info_window(self, selected_id)
            elif action == "Delete":
                delete_library_window(self, selected_id)
        elif mode == "Books":
            if action == "Add":
                add_book_window(self)
            elif action == "Edit":
                edit_book_window(self, selected_id)
            elif action == "View Info":
                view_book_info_window(self, selected_id)
            elif action == "Delete":
                delete_book_window(self, selected_id)

    def create_list(self, items, ids=None):
        if self.listbox:
            self.listbox.destroy()

        self.listbox = tk.Listbox(self.list_frame)
        self.listbox.pack(fill="both", expand=True)

        self.listbox_ids = ids or []

        for item in items:
            self.listbox.insert(tk.END, item)

    def toggle_visibility(self):
        if self.is_visible:
            self.grid_remove()
        else:
            self.grid()
        self.is_visible = not self.is_visible

# CRUD Windows

def add_person_window(parent):
    win = tk.Toplevel(parent)
    win.title("Add Person")
    win.geometry("300x400")

    tk.Label(win, text="Add New Person", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(win, text="Name:").pack(anchor="w", padx=10)
    entry_name = tk.Entry(win)
    entry_name.pack(fill="x", padx=10, pady=2)

    tk.Label(win, text="Surname:").pack(anchor="w", padx=10)
    entry_surname = tk.Entry(win)
    entry_surname.pack(fill="x", padx=10, pady=2)

    tk.Label(win, text="City:").pack(anchor="w", padx=10)
    entry_city = tk.Entry(win)
    entry_city.pack(fill="x", padx=10, pady=2)

    address_frame = tk.Frame(win)
    address_frame.pack(fill="x", padx=10, pady=10)

    address_frame.grid_columnconfigure(0, weight=1)
    address_frame.grid_columnconfigure(1, weight=1)
    address_frame.grid_columnconfigure(2, weight=1)

    tk.Label(address_frame, text="Street:").grid(row=0, column=0, padx=5)
    entry_street = tk.Entry(address_frame)
    entry_street.grid(row=1, column=0, padx=5, pady=2, sticky="ew")

    tk.Label(address_frame, text="Building:").grid(row=0, column=1, padx=5)
    entry_building = tk.Entry(address_frame)
    entry_building.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

    tk.Label(address_frame, text="Apartment:").grid(row=0, column=2, padx=5)
    entry_apartment = tk.Entry(address_frame)
    entry_apartment.grid(row=1, column=2, padx=5, pady=2, sticky="ew")

    def save_person():
        success, message = ctrl.add_person(
            name=entry_name.get().strip(),
            surname=entry_surname.get().strip(),
            account_id=model.get_account(),
            phone_number=None,
            email=None,
            city=entry_city.get().strip(),
            street=entry_street.get().strip(),
            building=entry_building.get().strip(),
            apartment=entry_apartment.get().strip(),
        )

        if success:
            model.refresh_people()
            parent.switch_mode("People")
            win.destroy()
        else:
            tk.messagebox.showerror("Error", message)

    tk.Button(win, text="Save", command=save_person).pack(pady=15)
    tk.Button(win, text="Cancel", command=win.destroy).pack()


def edit_person_window(parent, person_id):
    people_dict = model.get_people_dict()
    person_data = people_dict.get(person_id)

    if not person_data:
        tk.messagebox.showerror("Error", f"Person with ID {person_id} not found.")
        return
    win = tk.Toplevel(parent)
    win.title("Edit Person")
    win.geometry("300x400")

    tk.Label(win, text="Edit Person", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(win, text="Name:").pack(anchor="w", padx=10)
    entry_name = tk.Entry(win)
    entry_name.pack(fill="x", padx=10, pady=2)
    entry_name.insert(0, person_data.get("name", ""))

    tk.Label(win, text="Surname:").pack(anchor="w", padx=10)
    entry_surname = tk.Entry(win)
    entry_surname.pack(fill="x", padx=10, pady=2)
    entry_surname.insert(0, person_data.get("surname", ""))

    tk.Label(win, text="City:").pack(anchor="w", padx=10)
    entry_city = tk.Entry(win)
    entry_city.pack(fill="x", padx=10, pady=2)

    address_id = person_data.get("address_id")
    if address_id:
        city_name = ctrl.fetch_city(person_id)
        entry_city.insert(0, city_name or "")

    address_frame = tk.Frame(win)
    address_frame.pack(fill="x", padx=10, pady=10)

    address_frame.grid_columnconfigure(0, weight=1)
    address_frame.grid_columnconfigure(1, weight=1)
    address_frame.grid_columnconfigure(2, weight=1)

    address = ctrl.fetch_address(person_data.get("address_id"))

    tk.Label(address_frame, text="Street:").grid(row=0, column=0, padx=5)
    entry_street = tk.Entry(address_frame)
    entry_street.grid(row=1, column=0, padx=5, pady=2, sticky="ew")
    if address_id:
        street_name = address[1]
        entry_street.insert(0, street_name or "")

    tk.Label(address_frame, text="Building:").grid(row=0, column=1, padx=5)
    entry_building = tk.Entry(address_frame)
    entry_building.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
    if address_id:
        building_nr = address[2]
        entry_building.insert(0, building_nr or "")

    tk.Label(address_frame, text="Apartment:").grid(row=0, column=2, padx=5)
    entry_apartment = tk.Entry(address_frame)
    entry_apartment.grid(row=1, column=2, padx=5, pady=2, sticky="ew")
    if  address_id:
        apartment_nr = address[3]
        entry_apartment.insert(0, apartment_nr or "")

    def save_changes():
        success, message = ctrl.edit_person(
            person_id=person_id,
            name=entry_name.get().strip(),
            surname=entry_surname.get().strip(),
            phone_number=None,  # could fetch old value if not changed
            email=None,  # same here
            city=entry_city.get().strip(),
            street=entry_street.get().strip(),
            building=entry_building.get().strip(),
            apartment=entry_apartment.get().strip(),
        )

        if success:
            model.refresh_people()
            parent.switch_mode("People")
            win.destroy()
        else:
            tk.messagebox.showerror("Error", message)

    tk.Button(win, text="Save", command=save_changes).pack(pady=15)
    tk.Button(win, text="Cancel", command=win.destroy).pack()


def view_person_info_window(parent, person_id):
    person_data = ctrl.get_person_info(person_id)
    if not person_data:
        tk.messagebox.showerror("Error", f"Person with ID {person_id} not found.")
        return

    win = tk.Toplevel(parent)
    win.title(f"View Person Info (ID: {person_id})")
    win.geometry("350x300")

    tk.Label(win, text=f"Person Info", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(win, text=f"Name: {person_data['name']}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Surname: {person_data['surname']}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Role: {person_data['role']}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Phone: {person_data['phone_number'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Email: {person_data['email'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"City: {person_data['city'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Street: {person_data['street'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Building: {person_data['building'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Apartment: {person_data['apartment'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)

    tk.Button(win, text="Close", command=win.destroy).pack(pady=15)


def delete_person_window(parent, person_id):
    person_data = ctrl.get_person_info(person_id)
    if not person_data:
        tk.messagebox.showerror("Error", f"Person with ID {person_id} not found.")
        return

    win = tk.Toplevel(parent)
    win.title("Delete Person")
    win.geometry("250x150")
    tk.Label(win, text=f"Delete {person_data['name']} {person_data['surname']}?").pack(pady=20)

    def confirm_delete():
        success, message = ctrl.delete_person(person_id)
        if success:
            model.refresh_people()
            parent.switch_mode("People")
            win.destroy()
        else:
            tk.messagebox.showerror("Error", message)

    tk.Button(win, text="Confirm", command=confirm_delete).pack(pady=5)
    tk.Button(win, text="Cancel", command=win.destroy).pack(pady=5)


def add_library_window(parent):
    win = tk.Toplevel(parent)
    win.title("Add Library")
    win.geometry("300x400")

    tk.Label(win, text="Add New Library", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(win, text="Name:").pack(anchor="w", padx=10)
    entry_name = tk.Entry(win)
    entry_name.pack(fill="x", padx=10, pady=2)

    tk.Label(win, text="Phone Number:").pack(anchor="w", padx=10)
    entry_phone_number = tk.Entry(win)
    entry_phone_number.pack(fill="x", padx=10, pady=2)

    tk.Label(win, text="E-mail:").pack(anchor="w", padx=10)
    entry_email = tk.Entry(win)
    entry_email.pack(fill="x", padx=10, pady=2)

    tk.Label(win, text="City:").pack(anchor="w", padx=10)
    entry_city = tk.Entry(win)
    entry_city.pack(fill="x", padx=10, pady=2)

    address_frame = tk.Frame(win)
    address_frame.pack(fill="x", padx=10, pady=10)

    address_frame.grid_columnconfigure(0, weight=1)
    address_frame.grid_columnconfigure(1, weight=1)
    address_frame.grid_columnconfigure(2, weight=1)

    tk.Label(address_frame, text="Street:").grid(row=0, column=0, padx=5)
    entry_street = tk.Entry(address_frame)
    entry_street.grid(row=1, column=0, padx=5, pady=2, sticky="ew")

    tk.Label(address_frame, text="Building:").grid(row=0, column=1, padx=5)
    entry_building = tk.Entry(address_frame)
    entry_building.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

    tk.Label(address_frame, text="Apartment:").grid(row=0, column=2, padx=5)
    entry_apartment = tk.Entry(address_frame)
    entry_apartment.grid(row=1, column=2, padx=5, pady=2, sticky="ew")

    def save_library():
        success, message = ctrl.add_library(
            name=entry_name.get().strip(),
            city=entry_city.get().strip(),
            street=entry_street.get().strip(),
            building=entry_building.get().strip(),
            apartment=entry_apartment.get().strip(),
            phone_number=entry_phone_number.get().strip(),
            email=entry_email.get().strip(),
        )

        if success:
            model.refresh_libraries()
            parent.switch_mode("Libraries")
            win.destroy()
        else:
            tk.messagebox.showerror("Error", message)

    tk.Button(win, text="Save", command=save_library).pack(pady=15)
    tk.Button(win, text="Cancel", command=win.destroy).pack()

def edit_library_window(parent, library_id):
    library_dict = model.get_libraries_dict()
    library_data = library_dict.get(library_id)

    if not library_data:
        tk.messagebox.showerror("Error", f"Library with ID {library_id} not found.")
        return

    win = tk.Toplevel(parent)
    win.title("Edit Library")
    win.geometry("300x400")

    tk.Label(win, text="Edit Library", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(win, text="Name:").pack(anchor="w", padx=10)
    entry_name = tk.Entry(win)
    entry_name.pack(fill="x", padx=10, pady=2)
    entry_name.insert(0, library_data.get("name", ""))


    tk.Label(win, text="Phone Number:").pack(anchor="w", padx=10)
    entry_phone_number = tk.Entry(win)
    entry_phone_number.pack(fill="x", padx=10, pady=2)

    tk.Label(win, text="E-mail:").pack(anchor="w", padx=10)
    entry_email = tk.Entry(win)
    entry_email.pack(fill="x", padx=10, pady=2)

    contact_id = library_data.get("contact_id")
    if contact_id:
        phone_number, email = ctrl.fetch_contact(contact_id)
        entry_phone_number.insert(0, phone_number or "")
        entry_email.insert(0, email or "")

    tk.Label(win, text="City:").pack(anchor="w", padx=10)
    entry_city = tk.Entry(win)
    entry_city.pack(fill="x", padx=10, pady=2)

    address_id = library_data.get("address_id")
    if address_id:
        address = ctrl.fetch_address(address_id)
        entry_city.insert(0, address[0] or "")

    address_frame = tk.Frame(win)
    address_frame.pack(fill="x", padx=10, pady=10)

    address_frame.grid_columnconfigure(0, weight=1)
    address_frame.grid_columnconfigure(1, weight=1)
    address_frame.grid_columnconfigure(2, weight=1)

    address = ctrl.fetch_address(library_data.get("address_id"))

    tk.Label(address_frame, text="Street:").grid(row=0, column=0, padx=5)
    entry_street = tk.Entry(address_frame)
    entry_street.grid(row=1, column=0, padx=5, pady=2, sticky="ew")
    if address_id:
        street_name = address[1]
        entry_street.insert(0, street_name or "")

    tk.Label(address_frame, text="Building:").grid(row=0, column=1, padx=5)
    entry_building = tk.Entry(address_frame)
    entry_building.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
    if address_id:
        building_nr = address[2]
        entry_building.insert(0, building_nr or "")

    tk.Label(address_frame, text="Apartment:").grid(row=0, column=2, padx=5)
    entry_apartment = tk.Entry(address_frame)
    entry_apartment.grid(row=1, column=2, padx=5, pady=2, sticky="ew")
    if  address_id:
        apartment_nr = address[3]
        entry_apartment.insert(0, apartment_nr or "")

    def save_changes():
        success, message = ctrl.edit_library(
            library_id=library_id,
            name=entry_name.get().strip(),
            city=entry_city.get().strip(),
            street=entry_street.get().strip(),
            building=entry_building.get().strip(),
            apartment=entry_apartment.get().strip(),
            phone_number=None,
            email=None,
        )

        if success:
            model.refresh_libraries()
            parent.switch_mode("Libraries")
            win.destroy()
        else:
            tk.messagebox.showerror("Error", message)

    tk.Button(win, text="Save", command=save_changes).pack(pady=15)
    tk.Button(win, text="Cancel", command=win.destroy).pack()


def view_library_info_window(parent, library_id):
    library_data = ctrl.get_library_info(library_id)
    if not library_data:
        tk.messagebox.showerror("Error", f"Library with ID {library_id} not found.")
        return

    win = tk.Toplevel(parent)
    win.title(f"View Library Info (ID: {library_id})")
    win.geometry("350x300")

    tk.Label(win, text="Library Info", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(win, text=f"Name: {library_data['name']}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Phone: {library_data['phone_number'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Email: {library_data['email'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"City: {library_data['city'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Street: {library_data['street'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Building: {library_data['building'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Apartment: {library_data['apartment'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)

    tk.Button(win, text="Close", command=win.destroy).pack(pady=15)


def delete_library_window(parent, library_id):
    library_data = ctrl.get_library_info(library_id)
    if not library_data:
        tk.messagebox.showerror("Error", f"Library with ID {library_id} not found.")
        return

    win = tk.Toplevel(parent)
    win.title("Delete Library")
    win.geometry("250x150")
    tk.Label(win, text=f"Delete {library_data['name']}?").pack(pady=20)

    def confirm_delete():
        success, message = ctrl.delete_library(library_id)
        if success:
            model.refresh_libraries()
            parent.switch_mode("Libraries")
            win.destroy()
        else:
            tk.messagebox.showerror("Error", message)

    tk.Button(win, text="Confirm", command=confirm_delete).pack(pady=5)
    tk.Button(win, text="Cancel", command=win.destroy).pack(pady=5)

def add_book_window(parent):
    win = tk.Toplevel(parent)
    win.title("Add Book")
    win.geometry("300x350")


def edit_book_window(parent, book_id, selected_index):
    win = tk.Toplevel(parent)
    win.title("Edit Book")


def view_book_info_window(parent, book_id=None):
    pass


def delete_book_window(parent, book_id=None):
    pass


while app_state != available_states[0]:
    if app_state == available_states[1]:
        login_window()
    elif app_state == available_states[2]:
        register_window()
    elif app_state == available_states[3]:
        map_window()

