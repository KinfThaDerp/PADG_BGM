import tkinter as tk
from tkinter import messagebox, Frame
import tkintermapview
from libmap import controller as ctrl, model
from libmap.map_manager import MapManager
import libmap.views_popups as popup

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame_form = tk.Frame(self)
        frame_form.pack(pady=50)

        tk.Label(frame_form, text="Username: ").grid(row=0, column=0)
        self.entry_user = tk.Entry(frame_form)
        self.entry_user.grid(row=0, column=1)

        tk.Label(frame_form, text="Password: ").grid(row=1, column=0)
        self.entry_pass = tk.Entry(frame_form, show="*")
        self.entry_pass.grid(row=1, column=1)

        tk.Button(frame_form, text="Login",
                  command=lambda: controller.login(self.entry_user.get().strip(), self.entry_pass.get().strip())
                  ).grid(row=2, column=1, sticky="WE", pady=10)

        tk.Button(frame_form, text="Register",
                  command=lambda: controller.show_frame("RegisterView")
                  ).grid(row=2, column=2, sticky="WE", pady=10)  #


class RegisterView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame_reg = tk.Frame(self)
        frame_reg.pack(pady=30)

        tk.Label(frame_reg, text="Register", font=("Arial", 14, "bold")).grid(row=0, column=1, columnspan=2, pady=10, sticky="ew")
        tk.Label(frame_reg, text="Account Information").grid(row=1, column=0, columnspan=2, sticky="ew")

        tk.Label(frame_reg, text="Username: ").grid(row=2, column=0, sticky="e")
        self.entry_username = tk.Entry(frame_reg)
        self.entry_username.grid(row=2, column=1)

        tk.Label(frame_reg, text="Email: ").grid(row=3, column=0, sticky="e")
        self.entry_email = tk.Entry(frame_reg)
        self.entry_email.grid(row=3, column=1)

        tk.Label(frame_reg, text="Password: ").grid(row=4, column=0, sticky="e")
        self.entry_password = tk.Entry(frame_reg, show="*")
        self.entry_password.grid(row=4, column=1)

        tk.Label(frame_reg, text="Confirm Password: ").grid(row=5, column=0, sticky="e")
        self.entry_confirm_password = tk.Entry(frame_reg, show="*")
        self.entry_confirm_password.grid(row=5, column=1)

        tk.Label(frame_reg, text="Personal Information").grid(row=6, column=0, columnspan=2, sticky="ew")

        tk.Label(frame_reg, text="Name: ").grid(row=7, column=0, sticky="e")
        self.entry_name = tk.Entry(frame_reg)
        self.entry_name.grid(row=7, column=1)

        tk.Label(frame_reg, text="Surname: ").grid(row=8, column=0, sticky="e")
        self.entry_surname = tk.Entry(frame_reg)
        self.entry_surname.grid(row=8, column=1)

        tk.Label(frame_reg, text="City: ").grid(row=9, column=0, sticky="e")
        self.entry_city = tk.Entry(frame_reg)
        self.entry_city.grid(row=9, column=1)

        tk.Label(frame_reg, text="Street: ").grid(row=10, column=0, sticky="e")
        self.entry_street = tk.Entry(frame_reg)
        self.entry_street.grid(row=10, column=1)

        tk.Label(frame_reg, text="Building: ").grid(row=11, column=0, sticky="e")
        self.entry_building = tk.Entry(frame_reg)
        self.entry_building.grid(row=11, column=1)

        tk.Label(frame_reg, text="Apartment: ").grid(row=12, column=0, sticky="e")
        self.entry_apartment = tk.Entry(frame_reg)
        self.entry_apartment.grid(row=12, column=1)

        tk.Button(frame_reg, text="Register", command=self.handle_register).grid(row=13, column=1, pady=10)
        tk.Button(frame_reg, text="Cancel", command=lambda: controller.show_frame("LoginView")).grid(row=13, column=0)

        self.entries = {
            "username": self.entry_username,
            "email": self.entry_email,
            "password": self.entry_password,
            "confirm_password": self.entry_confirm_password,
            "name": self.entry_name,
            "surname": self.entry_surname,
            "city": self.entry_city,
            "street": self.entry_street,
            "building": self.entry_building,
            "apartment": self.entry_apartment
        }

    def handle_register(self):
        data = {key: widget.get().strip() for key, widget in self.entries.items()}

        success, message = ctrl.register_account_person(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            confirm_password=data["confirm_password"],
            name=data["name"],
            surname=data["surname"],
            phone_number=None,
            city=data["city"],
            street=data["street"],
            building=data["building"],
            apartment=data["apartment"]
        )

        if success:
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.controller.show_frame("LoginView")
        else:
            messagebox.showerror("Registration Error", message)


class LeftToolbar(tk.Frame):
    def __init__(self, parent, map_manager, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.map_manager = map_manager
        self.configure(width=250, bg='lightgray')
        self.grid_propagate(False)

        self.current_mode = "People"
        self.listbox = None
        self.listbox_ids = []

        self.mode_frame = tk.Frame(self, bg='lightgray')
        self.mode_frame.pack(fill="x", padx=5, pady=5)

        for mode in ["People", "Libraries", "Books"]:
            tk.Button(self.mode_frame, text=mode, command=lambda m=mode: self.switch_mode(m)).pack(side="left", padx=2)

        tk.Button(self.mode_frame, text="Refresh",
                  command=lambda: [model.refresh_all(), self.switch_mode(self.current_mode)]).pack(side="right")

        self.filter_frame = tk.Frame(self, bg='lightgray')
        self.filter_frame.pack(fill="x", padx=5)

        self.list_frame = tk.Frame(self, bg='lightgray')
        self.list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.listbox = tk.Listbox(self.list_frame)
        self.listbox.pack(fill="both", expand=True)

        self.button_frame = tk.Frame(self, bg='lightgray')
        self.button_frame.pack(fill="x", padx=5, pady=5)

        self.create_mode_buttons(self.current_mode)

    def switch_mode(self, mode):
        self.current_mode = mode
        self.listbox.delete(0, tk.END)
        self.listbox_ids = []

        for widget in self.filter_frame.winfo_children():
            widget.destroy()

        if mode == "People":
            self.setup_people_mode()
        elif mode == "Libraries":
            self.setup_libraries_mode()
        elif mode == "Books":
            self.setup_books_mode()

        self.create_mode_buttons(mode)

    def clear_listbox(self):
        self.listbox.delete(0, tk.END)
        self.listbox_ids = []

    def setup_people_mode(self):
        tk.Label(self.filter_frame, text="Role:", bg="lightgray").pack(side="left")
        role_filter = tk.StringVar(value="All")
        opt = tk.OptionMenu(self.filter_frame, role_filter, "All", "client", "employee",
                            command=lambda _: self.refresh_list_people(role_filter.get()))
        opt.pack(side="left")

        self.refresh_list_people("All")

    def refresh_list_people(self, role):
        self.clear_listbox()
        people_data = model.get_people_list()

        for p in people_data:
            if role == "All" or p['role'] == role.lower():
                self.listbox.insert(tk.END, f"{p['name']} {p['surname']} ({p['role']})")
                self.listbox_ids.append(p['id'])

        self.map_manager.draw_people(model.people, role.lower())

    def setup_libraries_mode(self):
        tk.Label(self.filter_frame, text="City:", bg="lightgray").pack(side="left")
        cities = ctrl.fetch_all_city_names()
        var = tk.StringVar(value="All Cities")
        opt = tk.OptionMenu(self.filter_frame, var, "All Cities", *cities,
                            command=lambda _: self.refresh_list_libraries(var.get()))
        opt.pack(side="left")

        self.refresh_list_libraries("All Cities")

    def refresh_list_libraries(self, city_filter):
        self.listbox.delete(0, tk.END)
        self.listbox_ids = []
        lib_data = model.get_libraries_list()

        for lib in lib_data:
            city_name = ctrl.fetch_city_name(lib['city_id'])
            if city_filter == "All Cities" or city_name == city_filter:
                self.listbox.insert(tk.END, lib['name'])
                self.listbox_ids.append(lib['id'])

        self.map_manager.draw_libraries(model.libraries, city_filter)

    def setup_books_mode(self):
        self.clear_listbox()
        books_data = model.get_books_list()

        for book in books_data:
            self.listbox.insert(tk.END, f"{book['title']} by {book['author']}")
            self.listbox_ids.append(book['id'])

    def create_mode_buttons(self, mode):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        for action in ("Add", "Edit", "View Info", "Delete"):
            tk.Button(
                self.button_frame,
                text=action,
                command=lambda a=action, m=mode: self.handle_action(m, a)
            ).pack(fill="x", pady=2)

        if mode == "Libraries":
            tk.Frame(self.button_frame, height=5, bg="lightgray").pack()  # Spacer
            tk.Button(
                self.button_frame,
                text="Show All Employees of City",
                bg="#e1f5fe",
                command= lambda: print("City Employees")
            ).pack(fill="x", pady=2)

    def handle_action(self, mode, action):
        selected_id = None
        if self.listbox and self.listbox.curselection():
            selected_index = self.listbox.curselection()[0]
            selected_id = self.listbox_ids[selected_index]
        else:
            if action != "Add":
                tk.messagebox.showwarning("Selection", "Please select an item first.")
                return

        if mode == "People":
            if action == "Add":
                popup.add_person_window(self)
            elif action == "Edit":
                popup.edit_person_window(self, selected_id)
            elif action == "View Info":
                popup.view_person_info_window(self, selected_id)
            elif action == "Delete":
                popup.delete_person_window(self, selected_id)
        elif mode == "Libraries":
            if action == "Add":
                popup.add_library_window(self)
            elif action == "Edit":
                popup.edit_library_window(self, selected_id)
            elif action == "View Info":
                popup.view_library_info_window(self, selected_id, self.map_manager.widget)
            elif action == "Delete":
                popup.delete_library_window(self, selected_id)
        elif mode == "Books":
            if action == "Add":
                popup.add_book_window(self)
            elif action == "Edit":
                popup.edit_book_window(self, selected_id)
            elif action == "View Info":
                popup.view_book_info_window(self, selected_id)
            elif action == "Delete":
                popup.delete_book_window(self, selected_id)

class MapView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = tk.Frame(self)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        tk.Button(self.top_bar, text="Logout", command=controller.logout).pack(side="right", padx=10)

        self.map_widget = tkintermapview.TkinterMapView(self)
        self.map_widget.grid(row=1, column=1, sticky="nsew")
        self.map_widget.set_position(52.229722, 21.011667)
        self.map_widget.set_zoom(6)  #

        self.map_manager = MapManager(self.map_widget, parent_view=self)

        self.sidebar = LeftToolbar(self, self.map_manager)
        self.sidebar.grid(row=1, column=0, sticky="ns")

        tk.Button(self.top_bar, text="Toggle Sidebar",
                  command=lambda: self.sidebar.grid_remove() if self.sidebar.winfo_viewable() else self.sidebar.grid()
                  ).pack(side="left", padx=10)

    def on_show(self):
        model.refresh_all()
        self.sidebar.switch_mode("People")