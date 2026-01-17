import tkinter as tk
from tkinter import Frame
import tkintermapview
from libmap import controller as ctrl, model


#  Window Directors

available_states = ("Disable", "Login", "Register", "Map")
app_state = available_states[1]


def change_app_state(window, state:int) -> None:
    global app_state
    if 0<=state<=len(available_states):
        app_state = available_states[state]
        window.destroy()
    else:
        raise Exception("Failed to change App State!")


def go_to_login(window) -> None:
    model.set_account(None)
    change_app_state(window, 1)


def go_to_registry(window) -> None:
    change_app_state(window, 2)


def go_to_map(window) -> None:
    change_app_state(window, 3)


def reset_password() -> None:
    tk.messagebox.showwarning(title="Warning!", message="You currently cannot reset passwords.\nPlease contact an administrator.",)


def handle_register(root, **entries) -> None:
    success, message = ctrl.register_account_person(
        username=entries["username"].get().strip(),
        email=entries["email"].get().strip(),
        password=entries["password"].get().strip(),
        confirm_password=entries["confirm_password"].get().strip(),
        name=entries["name"].get().strip() if entries.get("name") else None,
        surname=entries["surname"].get().strip() if entries.get("surname") else None,
        phone_number=entries["phonenumber"].get().strip() if entries.get("phonenumber") else None,
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


def handle_login(root, **entries) -> None:
    success, message, account_id = ctrl.login_account(
        username=entries["username"].get().strip(),
        password=entries["password"].get().strip(),
    )
    if success:
        model.set_account(account_id)
        go_to_map(root)
    else:
        tk.messagebox.showerror("Error", message)


def login_window() -> None:
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


def register_window() -> None:
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


def map_window() -> None:
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

    map_widget = tkintermapview.TkinterMapView(root_map)
    sidebar = LeftToolbar(root_map)
    sidebar.set_map_widget(map_widget)
    sidebar.toggle_visibility()

    model.refresh_all()

    toggle_button = tk.Button(
        toolbar_frame,
        text="Show Sidebar",
        command=lambda: [sidebar.toggle_visibility(),
            toggle_button.config(text="Show Toolbar" if not sidebar.is_visible else "Hide Toolbar")])
    toggle_button.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    button_logout = tk.Button(
        toolbar_frame,
        text="Log out",
        command=lambda: go_to_login(root_map))
    button_logout.grid(row=0, column=3, sticky="e", padx=10, pady=5)

    map_widget.grid(row=1, column=1, sticky="nsew")
    map_widget.set_position(52.229722, 21.011667)
    map_widget.set_zoom(6)

    libraries_toggle = ToggleButton(toolbar_frame, map_widget, "libraries")
    libraries_toggle.grid(row=0, column=2, sticky="e", padx=10, pady=5)

    people_toggle = ToggleButton(toolbar_frame, map_widget, "people")
    people_toggle.grid(row=0, column=1, sticky="e", padx=10, pady=5)
    sidebar.people_toggle = people_toggle

    root_map.mainloop()

class ToggleButton(Frame):
    def __init__(self, parent, map_widget: tkintermapview.TkinterMapView, marker_type: str, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.map_widget = map_widget
        self.marker_type = marker_type
        self.markers_drawn = False

        self.button = tk.Button(self, text=f"Show {marker_type}", command=self.toggle)
        self.button.pack(fill="x")

    def toggle(self):
        if self.markers_drawn:
            self.remove_markers()
            self.button.config(text=f"Show {self.marker_type}")
        else:
            self.draw_markers()
            self.button.config(text=f"Hide {self.marker_type}")
        self.markers_drawn = not self.markers_drawn

    def draw_markers(self):
        self.remove_markers()

        if self.marker_type == "people":
            data_dict = model.people
        elif self.marker_type == "libraries":
            data_dict = model.libraries
        else:
            return

        sidebar = self.master.master.children.get('!lefttoolbar')
        selected_role = "all"
        if sidebar and hasattr(sidebar, 'role_filter_var'):
            selected_role = sidebar.role_filter_var.get().lower()

        for id_, info in data_dict.items():
            if self.marker_type == "people":
                person_role = info.get('role', '').lower()
                if selected_role != "all" and person_role != selected_role:
                    continue

            coords = ctrl.fetch_address(info["address_id"])[-1]
            if not coords:
                continue
            lat, lon = coords

            text = f"{info.get('name', '')} {info.get('surname', '')}" if self.marker_type == "people" else info.get(
                "name", "")

            marker = self.map_widget.set_marker(
                lat, lon,
                text=text,
                command=lambda _=None, i=id_: self.on_marker_click(i)
            )
            model.map_markers[self.marker_type][id_] = marker

    def remove_markers(self):
        if model.map_markers[self.marker_type]:
            for marker in model.map_markers[self.marker_type].values():
                marker.delete()
            model.map_markers[self.marker_type] = {}

    def on_marker_click(self, id_, *_):
        if self.marker_type == "people":
            view_person_info_window(self, id_)
        else:
            view_library_info_window(self, id_, self.map_widget)

class LeftToolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.configure(width=250, bg='lightgray')
        self.grid(row=1, column=0, sticky="ns")
        self.grid_propagate(False)



        self.is_visible = True
        self.current_mode = "People"
        self.listbox = None
        self.map_widget = None

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mode_frame = tk.Frame(self, bg='lightgray')
        self.mode_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        tk.Button(self.mode_frame, text="People", command=lambda: self.switch_mode("People")).pack(side="left", padx=2)
        tk.Button(self.mode_frame, text="Books", command=lambda: self.switch_mode("Books")).pack(side="left", padx=2)
        tk.Button(self.mode_frame, text="Libraries", command=lambda: self.switch_mode("Libraries")).pack(side="left", padx=2)

        self.info_frame = tk.Frame(self, bg='lightgray')
        self.info_frame.grid(row=1, column=0, sticky="ew", padx=5)


        self.current_mode_label = tk.Label(self.info_frame, text=self.current_mode, bg='lightgray')
        self.current_mode_label.pack(side="left")


        tk.Button(self.info_frame, text="Refresh", command=lambda: model.refresh_all()).pack(side="right", padx=2)


        self.role_filter_var = tk.StringVar(value="All")
        self.role_filter_dropdown = tk.OptionMenu(
            self.info_frame,
            self.role_filter_var,
            "All", "Client", "Employee",
            command=lambda _: self.apply_role_filter()
        )
        self.role_filter_dropdown.config(width=8) #
        self.role_filter_dropdown.pack(side="right", padx=2)


        self.list_frame = tk.Frame(self, bg='lightgray')
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.create_list([])

        self.buttons_frame = tk.Frame(self, bg='lightgray')
        self.buttons_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

    def set_map_widget(self, map_widget):
        self.map_widget = map_widget

    def switch_mode(self, mode):
        self.current_mode = mode
        self.current_mode_label.config(text=mode)
        self.items = []
        display_items = []
        ids = []

        if mode == "People":self.role_filter_dropdown.pack(side="right", padx=2)
        else: self.role_filter_dropdown.pack_forget()

        if mode == "People":
            self.items = model.get_people_list()
            selected_role = self.role_filter_var.get().lower()
            for p in self.items:
                if selected_role == "all" or p['role'] == selected_role:
                    display_items.append(f"{p['name']} {p['surname']} ({p['role']})")
                    ids.append(p['id'])

        elif mode == "Books":
            self.items = model.get_books_list()
            display_items = [f"{p['title']} by {p['author']}" for p in self.items]
            ids = [p['id'] for p in self.items]

        elif mode == "Libraries":
            self.items = model.get_libraries_list()
            display_items = [p['name'] for p in self.items]
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
                view_library_info_window(self, selected_id, self.map_widget)
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

    def apply_role_filter(self):
        if self.current_mode == "People":
            self.switch_mode("People")

            if hasattr(self, 'people_toggle') and self.people_toggle.markers_drawn:
                self.people_toggle.draw_markers()

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

    tk.Button(win, text="Save", command=save_changes).pack(pady=15)
    tk.Button(win, text="Cancel", command=win.destroy).pack()


def view_person_info_window(parent, person_id):
    person_data = ctrl.get_person_info(person_id)
    if not person_data:
        tk.messagebox.showerror("Error", f"Person with ID {person_id} not found.")
        return

    win = tk.Toplevel(parent)
    win.title(f"Info: {person_data['name']} {person_data['surname']}")
    win.geometry("400x300")

    tk.Label(win, text=f"{person_data['name']} {person_data['surname']}", font=("Arial", 14, "bold")
             ).pack(pady=10)
    tk.Label(win, text=f"City: {person_data['city'] or 'N/A'}"
             ).pack(padx=10, pady=2)
    tk.Label(win, text=f"Street: {person_data['street'] or 'N/A'}"
             ).pack(padx=10, pady=2)
    tk.Label(win, text=f"Building: {person_data['building'] or 'N/A'}"
             ).pack(padx=10, pady=2)
    tk.Label(win, text=f"Apartment: {person_data['apartment'] or 'N/A'}"
             ).pack(padx=10, pady=2)
    tk.Label(win, text=f"Role: {person_data['role'].capitalize()}").pack()

    lib_info = ctrl.fetch_employee_library_info(person_id)
    if lib_info:
        lib_id, lib_name = lib_info
        lib_frame = tk.Frame(win)
        lib_frame.pack(pady=10)
        tk.Label(lib_frame, text=f"Works at: {lib_name}", fg="blue").pack(side="left")
        tk.Button(lib_frame, text="View Library", command=lambda: view_library_info_window(parent, lib_id, getattr(parent, 'map_widget', None))
                  ).pack(side="left", padx=5)

    contact = ctrl.fetch_contact(person_data["contact_id"])
    if contact:
        tk.Label(win, text=f"Email: {contact[1]}").pack()
        tk.Label(win, text=f"Phone: {contact[0]}").pack()

    button_frame = tk.Frame(win)
    button_frame.pack(pady=20, fill="x", padx=20)
    tk.Button(button_frame, text="Add New", command=lambda: add_person_window(parent)
              ).pack(side="left", expand=True, padx=2)
    tk.Button(button_frame, text="Edit", command=lambda: [win.destroy(), edit_person_window(parent, person_id)]
              ).pack(side="left", expand=True, padx=2)
    tk.Button(button_frame, text="Delete",command=lambda: [win.destroy(), delete_person_window(parent, person_id)]
              ).pack(side="left", expand=True,padx=2)
    tk.Button(button_frame, text="Close", command=win.destroy
              ).pack(side="left", expand=True,padx=2)


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


def view_library_info_window(parent, library_id, map_widget=None):
    lib_data = model.get_libraries_dict().get(library_id)
    if not lib_data:
        tk.messagebox.showerror("Error", "Library data not found.")
        return

    win = tk.Toplevel(parent)
    win.title(f"Library: {lib_data['name']}")
    win.geometry("750x500")
    win.resizable(False, False)

    left_frame = tk.Frame(win, padx=20, pady=20)
    left_frame.pack(side="left", fill="both", expand=True)

    tk.Frame(win, width=2, bd=1, relief="sunken", bg="gray").pack(side="left", fill="y", pady=10)

    right_frame = tk.Frame(win, padx=20, pady=20, bg="#f8f9fa")
    right_frame.pack(side="right", fill="both", expand=True)

    tk.Label(left_frame, text=lib_data['name'], font=("Arial", 16, "bold"), wraplength=300, justify="left").pack(
        anchor="w", pady=(0, 10))

    address = ctrl.fetch_address(lib_data["address_id"])
    if address:
        tk.Label(left_frame, text="Address:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 0))
        tk.Label(left_frame, text=f"{address[1]} {address[2]}").pack(anchor="w")
        tk.Label(left_frame, text=f"{address[3]}, {address[0]}").pack(anchor="w")

    contact = ctrl.fetch_contact(lib_data["contact_id"])
    if contact:
        tk.Label(left_frame, text="Contact Info:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(15, 0))
        tk.Label(left_frame, text=f"📞 {contact[0]}").pack(anchor="w")
        tk.Label(left_frame, text=f"✉ {contact[1]}").pack(anchor="w")

    tk.Button(left_frame, text="Close", width=15, command=win.destroy).pack(side="bottom", pady=10)

    current_role_var = tk.StringVar(value="Employee")
    list_label = tk.Label(right_frame, text="Library Employees", font=("Arial", 11, "bold"), bg="#f8f9fa")
    list_label.pack(pady=(0, 5))

    listbox = tk.Listbox(right_frame, font=("Arial", 10), selectmode="single", height=15)
    listbox.pack(fill="both", expand=True, pady=5)

    displayed_person_ids = []

    toggle_button = tk.Button(
        right_frame,
        text="Switch to Clients",
        command=lambda: update_listbox("Client" if current_role_var.get() == "Employee" else "Employee")
    )
    toggle_button.pack(fill="x", pady=2)

    def update_listbox(role):
        nonlocal displayed_person_ids
        listbox.delete(0, tk.END)
        displayed_person_ids = []

        list_label.config(text=f"Library {role}s")
        toggle_button.config(text=f"Switch to {'Clients' if role == 'Employee' else 'Employees'}")
        current_role_var.set(role)

        if role == "Employee":
            ids = ctrl.fetch_library_employee_ids(library_id)
        else:
            ids = ctrl.fetch_library_client_ids(library_id)
        people_details = ctrl.fetch_people_details_by_ids(ids)

        for person in people_details:
            listbox.insert(tk.END, f"{person['name']}")
            displayed_person_ids.append(person['id'])

    def handle_view_person():
        selection = listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("Selection Required", "Please select a person from the list.")
            return

        person_id = displayed_person_ids[selection[0]]
        view_person_info_window(win, person_id)



    tk.Button(right_frame,text="View Person Details",command=handle_view_person).pack(fill="x", pady=5)

    if map_widget:
         tk.Button(
            right_frame,
            text="Show Group on Map",
            command=lambda: show_filtered_people_on_map(map_widget, library_id, current_role_var.get().lower())
        ).pack(fill="x", pady=5)

    update_listbox("Employee")


def delete_library_window(parent, library_id) -> None:
    library_data = ctrl.get_library_info(library_id)
    if not library_data:
        tk.messagebox.showerror("Error", f"Library with ID {library_id} not found.")
        return

    win = tk.Toplevel(parent)
    win.title("Delete Library")
    win.geometry("250x150")
    tk.Label(win, text=f"Delete {library_data['name']}?").pack(pady=20)

    def confirm_delete() -> None:
        success, message = ctrl.delete_library(library_id)
        if success:
            model.refresh_libraries()
            parent.switch_mode("Libraries")
            win.destroy()
        else:
            tk.messagebox.showerror("Error", message)

    tk.Button(win, text="Confirm", command=confirm_delete).pack(pady=5)
    tk.Button(win, text="Cancel", command=win.destroy).pack(pady=5)


def add_book_window(parent) -> None:
    win = tk.Toplevel(parent)
    win.title("Add Book")
    win.geometry("300x350")

    tk.Label(win, text="Add New Book", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(win, text="Title:").pack(anchor="w", padx=10)
    entry_title = tk.Entry(win)
    entry_title.pack(fill="x", padx=10, pady=2)

    tk.Label(win, text="Author:").pack(anchor="w", padx=10)
    entry_author = tk.Entry(win)
    entry_author.pack(fill="x", padx=10, pady=2)

    tk.Label(win, text="ISBN-13:").pack(anchor="w", padx=10)
    entry_isbn = tk.Entry(win)
    entry_isbn.pack(fill="x", padx=10, pady=2)

    tk.Label(win, text="Publisher:").pack(anchor="w", padx=10)
    entry_publisher = tk.Entry(win)
    entry_publisher.pack(fill="x", padx=10, pady=2)

    tk.Label(win, text="Genre:").pack(anchor="w", padx=10)
    entry_genre = tk.Entry(win)
    entry_genre.pack(fill="x", padx=10, pady=2)

    def save_book() -> None:
        success, message = ctrl.add_book(
            title=entry_title.get().strip(),
            author=entry_author.get().strip(),
            isbn_13=entry_isbn.get().strip() or None,
            publisher=entry_publisher.get().strip() or None,
            genre=entry_genre.get().strip() or None
        )
        if success:
            model.refresh_books()
            parent.switch_mode("Books")
            win.destroy()
        else:
            tk.messagebox.showerror("Error", message)

    tk.Button(win, text="Save", command=save_book).pack(pady=15)
    tk.Button(win, text="Cancel", command=win.destroy).pack()


def edit_book_window(parent, book_id) -> None:
    book_data = ctrl.get_book_info(book_id)
    if not book_data:
        tk.messagebox.showerror("Error", f"Book with ID {book_id} not found.")
        return

    win = tk.Toplevel(parent)
    win.title("Edit Book")
    win.geometry("300x350")

    tk.Label(win, text="Edit Book", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(win, text="Title:").pack(anchor="w", padx=10)
    entry_title = tk.Entry(win)
    entry_title.pack(fill="x", padx=10, pady=2)
    entry_title.insert(0, book_data["title"])

    tk.Label(win, text="Author:").pack(anchor="w", padx=10)
    entry_author = tk.Entry(win)
    entry_author.pack(fill="x", padx=10, pady=2)
    entry_author.insert(0, book_data["author"])

    tk.Label(win, text="ISBN-13:").pack(anchor="w", padx=10)
    entry_isbn = tk.Entry(win)
    entry_isbn.pack(fill="x", padx=10, pady=2)
    entry_isbn.insert(0, book_data["isbn_13"] or "")

    tk.Label(win, text="Publisher:").pack(anchor="w", padx=10)
    entry_publisher = tk.Entry(win)
    entry_publisher.pack(fill="x", padx=10, pady=2)
    entry_publisher.insert(0, book_data["publisher"] or "")

    tk.Label(win, text="Genre:").pack(anchor="w", padx=10)
    entry_genre = tk.Entry(win)
    entry_genre.pack(fill="x", padx=10, pady=2)
    entry_genre.insert(0, book_data["genre"] or "")

    def save_changes() -> None:
        success, message = ctrl.edit_book(
            book_id=book_id,
            title=entry_title.get().strip(),
            author=entry_author.get().strip(),
            isbn_13=entry_isbn.get().strip() or None,
            publisher=entry_publisher.get().strip() or None,
            genre=entry_genre.get().strip() or None
        )
        if success:
            model.refresh_books()
            parent.switch_mode("Books")
            win.destroy()
        else:
            tk.messagebox.showerror("Error", message)

    tk.Button(win, text="Save", command=save_changes).pack(pady=15)
    tk.Button(win, text="Cancel", command=win.destroy).pack()


def view_book_info_window(parent, book_id) -> None:
    book_data = ctrl.get_book_info(book_id)
    if not book_data:
        tk.messagebox.showerror("Error", f"Book with ID {book_id} not found.")
        return

    win = tk.Toplevel(parent)
    win.title(f"View Book Info (ID: {book_id})")
    win.geometry("350x250")

    tk.Label(win, text="Book Info", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(win, text=f"Title: {book_data['title']}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Author: {book_data['author']}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"ISBN-13: {book_data['isbn_13'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Publisher: {book_data['publisher'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)
    tk.Label(win, text=f"Genre: {book_data['genre'] or 'N/A'}").pack(anchor="w", padx=10, pady=2)

    tk.Button(win, text="Close", command=win.destroy).pack(pady=15)


def delete_book_window(parent, book_id) -> None:
    book_data = ctrl.get_book_info(book_id)
    if not book_data:
        tk.messagebox.showerror("Error", f"Book with ID {book_id} not found.")
        return

    win = tk.Toplevel(parent)
    win.title("Delete Book")
    win.geometry("250x150")
    tk.Label(win, text=f"Delete '{book_data['title']}'?").pack(pady=20)

    def confirm_delete() -> None:
        success, message = ctrl.handler_delete_book(book_id)
        if success:
            model.refresh_books()
            parent.switch_mode("Books")
            win.destroy()
        else:
            tk.messagebox.showerror("Error", message)

    tk.Button(win, text="Confirm", command=confirm_delete).pack(pady=5)
    tk.Button(win, text="Cancel", command=win.destroy).pack(pady=5)


def register_at_library_window(parent, library_id) -> None:
    win = tk.Toplevel(parent)
    win.title("Library Staff & Client Management")
    win.geometry("600x450")

    all_people = model.get_people_list()

    clients_data = [p for p in all_people if p['role'] == 'client']
    employees_data = [p for p in all_people if p['role'] == 'employee']

    main_frame = tk.Frame(win)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)


    client_frame = tk.Frame(main_frame)
    client_frame.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(client_frame, text="Current Clients", font=("Arial", 10, "bold")).pack()
    client_lb = tk.Listbox(client_frame, exportselection=False)
    client_lb.pack(fill="both", expand=True)

    for p in clients_data:
        client_lb.insert(tk.END, f"{p['name']} {p['surname']} (ID: {p['id']})")


    emp_frame = tk.Frame(main_frame)
    emp_frame.pack(side="right", fill="both", expand=True, padx=5)

    tk.Label(emp_frame, text="Current Employees", font=("Arial", 10, "bold")).pack()
    emp_lb = tk.Listbox(emp_frame, exportselection=False)
    emp_lb.pack(fill="both", expand=True)

    for p in employees_data:
        emp_lb.insert(tk.END, f"{p['name']} {p['surname']} (ID: {p['id']})")

    def handle_promotion(listbox, data_source, role_to_assign):
        selection = listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("Selection Required", "Please select a person from the list.")
            return

        person = data_source[selection[0]]
        person_id = person['id']

        if role_to_assign == "employee":
            success, message = ctrl.assign_employee_to_library(person_id, library_id)
        else:
            success, message = ctrl.assign_client_to_library(person_id, library_id)

        if success:
            tk.messagebox.showinfo("Success", f"Successfully assigned {person['name']} as {role_to_assign}.")
            model.refresh_people()
            win.destroy()
        else:
            tk.messagebox.showerror("Error", message)

    button_frame = tk.Frame(win)
    button_frame.pack(fill="x", pady=10)

    tk.Button(
        button_frame, text="↑ Assign Client as Employee",
        bg="#e1f5fe",
        command=lambda: handle_promotion(client_lb, clients_data, "employee")
    ).pack(side="left", expand=True, padx=10)


    tk.Button(
        button_frame, text="↓ Assign Employee as Client",
        bg="#fff3e0",
        command=lambda: handle_promotion(emp_lb, employees_data, "client")
    ).pack(side="right", expand=True, padx=10)


def show_filtered_people_on_map(map_widget, library_id, role_type):
    for marker in model.map_markers["people"].values():
        marker.delete()
    model.map_markers["people"].clear()

    for marker in model.map_markers["libraries"].values():
        marker.delete()
    model.map_markers["libraries"].clear()

    if role_type == "client":
        person_ids = ctrl.fetch_library_client_ids(library_id)
    else:
        person_ids = ctrl.fetch_library_employee_ids(library_id)

    if not person_ids:
        tk.messagebox.showinfo("Info", f"No {role_type}s registered at this library.")
        return

    for p_id in person_ids:
        p_info = ctrl.get_person_info(p_id)
        if not p_info or not p_info.get("coords"):
            continue

        lat, lon = p_info["coords"]
        marker = map_widget.set_marker(
            lat, lon,
            text=f"{p_info['name']} {p_info['surname']} ({role_type})"
        )

        model.map_markers["people"][p_id] = marker

while app_state != available_states[0]:
    if app_state == available_states[1]:
        login_window()
    elif app_state == available_states[2]:
        register_window()
    elif app_state == available_states[3]:
        map_window()

