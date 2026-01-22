import tkinter as tk
from tkinter import messagebox, ttk
from libmap import controller as ctrl, model


def add_person_window(parent_view):
    win = tk.Toplevel(parent_view)
    win.title("Add Person")
    win.geometry("350x450")

    tk.Label(win, text="Add New Person", font=("Arial", 12, "bold")).pack(pady=10)

    entries = {}
    fields = ["Name", "Surname", "City", "Street", "Building", "Apartment"]

    for field in fields:
        frame = tk.Frame(win)
        frame.pack(fill="x", padx=10, pady=2)
        tk.Label(frame, text=f"{field}:", width=10, anchor="w").pack(side="left")
        e = tk.Entry(frame)
        e.pack(side="left", fill="x", expand=True)
        entries[field.lower()] = e

    def save_person():
        success, message = ctrl.add_person(
            name=entries["name"].get().strip(),
            surname=entries["surname"].get().strip(),
            account_id=model.get_account(),
            city=entries["city"].get().strip(),
            street=entries["street"].get().strip(),
            building=entries["building"].get().strip(),
            apartment=entries["apartment"].get().strip(),
        )

        if success:
            model.refresh_people()
            if hasattr(parent_view, 'sidebar'):
                parent_view.sidebar.switch_mode("People")
            win.destroy()
        else:
            messagebox.showerror("Error", message)

    tk.Button(win, text="Save", command=save_person).pack(pady=15)


def edit_person_window(parent_view, person_id):
    person = model.people.get(person_id)
    if not person:
        return

    win = tk.Toplevel(parent_view)
    win.title(f"Edit: {person['name']}")
    win.geometry("350x450")

    tk.Label(win, text="Edit Person", font=("Arial", 12, "bold")).pack(pady=10)

    current_addr = ctrl.fetch_address(person['address_id'])

    entries = {}
    fields = [
        ("Name", person['name']),
        ("Surname", person['surname']),
        ("City", current_addr[0] if current_addr else ""),
        ("Street", current_addr[1] if current_addr else ""),
        ("Building", current_addr[2] if current_addr else ""),
        ("Apartment", current_addr[3] if current_addr else "")
    ]

    for label, value in fields:
        frame = tk.Frame(win)
        frame.pack(fill="x", padx=10, pady=2)
        tk.Label(frame, text=f"{label}:", width=10, anchor="w").pack(side="left")
        e = tk.Entry(frame)
        e.insert(0, str(value) if value else "")
        e.pack(side="left", fill="x", expand=True)
        entries[label.lower()] = e

    def update_person():
        success, message = ctrl.edit_person(
            person_id,
            name=entries["name"].get().strip(),
            surname=entries["surname"].get().strip(),
            city=entries["city"].get().strip(),
            street=entries["street"].get().strip(),
            building=entries["building"].get().strip(),
            apartment=entries["apartment"].get().strip()
        )

        if success:
            model.refresh_people()
            if hasattr(parent_view, 'sidebar'):
                parent_view.sidebar.refresh_list_people(
                    parent_view.sidebar.current_filter_val if hasattr(parent_view.sidebar,
                                                                      'current_filter_val') else "All")
            win.destroy()
        else:
            messagebox.showerror("Error", message)

    tk.Button(win, text="Update", command=update_person).pack(pady=15)


def view_person_info_window(parent_view, person_id):
    person_data = ctrl.get_person_info(person_id)
    if not person_data:
        messagebox.showerror("Error", f"Person with ID {person_id} not found.")
        return

    win = tk.Toplevel(parent_view)
    win.title(f"Info: {person_data['name']} {person_data['surname']}")
    win.geometry("400x350")

    tk.Label(win, text=f"{person_data['name']} {person_data['surname']}", font=("Arial", 14, "bold")).pack(pady=10)

    info_frame = tk.Frame(win)
    info_frame.pack(pady=10)

    tk.Label(info_frame, text=f"Role: {person_data['role'].capitalize()}").pack(anchor="w")
    tk.Label(info_frame, text=f"City: {person_data['city'] or 'N/A'}").pack(anchor="w")
    tk.Label(info_frame, text=f"Address: {person_data.get('street', '')} {person_data.get('building', '')}").pack(
        anchor="w")

    lib_info = ctrl.fetch_employee_library_info(person_id)
    if lib_info:
        lib_id, lib_name = lib_info
        f = tk.Frame(win)
        f.pack(pady=10)
        tk.Label(f, text=f"Works at: {lib_name}", fg="blue").pack(side="left")
        tk.Button(f, text="View Lib", command=lambda: view_library_info_window(parent_view, lib_id)).pack(side="left",
                                                                                                          padx=5)

    button_frame = tk.Frame(win)
    button_frame.pack(side="bottom", pady=20)

    tk.Button(button_frame, text="Edit", command=lambda: edit_person_window(parent_view, person_id)).pack(side="left",
                                                                                                          padx=5)
    tk.Button(button_frame, text="Close", command=win.destroy).pack(side="left", padx=5)

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


def add_library_window(parent_view):
    win = tk.Toplevel(parent_view)
    win.title("Add Library")
    win.geometry("350x400")

    tk.Label(win, text="Add New Library", font=("Arial", 12, "bold")).pack(pady=10)

    entries = {}
    fields = ["Name", "City", "Street", "Building", "Apartment", "Phone", "Email"]

    for field in fields:
        frame = tk.Frame(win)
        frame.pack(fill="x", padx=10, pady=2)
        tk.Label(frame, text=f"{field}:", width=10, anchor="w").pack(side="left")
        e = tk.Entry(frame)
        e.pack(side="left", fill="x", expand=True)
        entries[field.lower()] = e

    def save_library():
        success, message = ctrl.add_library(
            name=entries["name"].get().strip(),
            city=entries["city"].get().strip(),
            street=entries["street"].get().strip(),
            building=entries["building"].get().strip(),
            apartment=entries["apartment"].get().strip(),
            phone_number=entries["phone"].get().strip(),
            email=entries["email"].get().strip()
        )

        if success:
            model.refresh_libraries()
            if hasattr(parent_view, 'sidebar'):
                parent_view.sidebar.switch_mode("Libraries")
            win.destroy()
        else:
            messagebox.showerror("Error", message)

    tk.Button(win, text="Save Library", command=save_library).pack(pady=15)

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


def view_library_info_window(parent_view, library_id, map_widget=None):
    lib_data = model.get_libraries_dict().get(library_id)
    if not lib_data:
        messagebox.showerror("Error", "Library data not found.")
        return

    win = tk.Toplevel(parent_view)
    win.title(f"Library: {lib_data['name']}")
    win.geometry("600x550")

    tk.Label(win, text=lib_data['name'], font=("Arial", 16, "bold")).pack(pady=10)

    address = ctrl.fetch_address(lib_data["address_id"])
    if address:
        addr_str = f"{address[1]} {address[2]}"
        if address[3]: addr_str += f"/{address[3]}"
        addr_str += f", {address[0]}"
        tk.Label(win, text=addr_str).pack()

    tab_control = ttk.Notebook(win)
    tab_employees = tk.Frame(tab_control)
    tab_clients = tk.Frame(tab_control)

    tab_control.add(tab_employees, text='Employees')
    tab_control.add(tab_clients, text='Clients')
    tab_control.pack(expand=1, fill="both", padx=10, pady=10)

    lb_emp = tk.Listbox(tab_employees)
    lb_emp.pack(side="left", fill="both", expand=True)
    sb_emp = tk.Scrollbar(tab_employees, orient="vertical", command=lb_emp.yview)
    sb_emp.pack(side="right", fill="y")
    lb_emp.config(yscrollcommand=sb_emp.set)

    emp_ids = ctrl.fetch_library_employee_ids(library_id)
    employees = ctrl.fetch_people_details_by_ids(emp_ids)

    current_emp_ids = []

    for emp in employees:
        current_emp_ids.append(emp['id'])
        name = emp.get('name', 'Unknown')
        surname = emp.get('surname', '')
        role = emp.get('role')
        lb_emp.insert(tk.END, f"{name} {surname}")

    lb_cli = tk.Listbox(tab_clients)
    lb_cli.pack(side="left", fill="both", expand=True)
    sb_cli = tk.Scrollbar(tab_clients, orient="vertical", command=lb_cli.yview)
    sb_cli.pack(side="right", fill="y")
    lb_cli.config(yscrollcommand=sb_cli.set)

    client_ids = ctrl.fetch_library_client_ids(library_id)
    clients = ctrl.fetch_people_details_by_ids(client_ids)

    current_cli_ids = []

    for cli in clients:
        current_cli_ids.append(cli['id'])
        name = cli.get('name', 'Unknown')
        surname = cli.get('surname', '')
        lb_cli.insert(tk.END, f"{name} {surname}")

    def toggle_role():
        current_tab_index = tab_control.index(tab_control.select())

        person_id = None
        target_role = ""
        action_func = None

        if current_tab_index == 0:
            selection = lb_emp.curselection()
            if not selection:
                messagebox.showwarning("Selection", "Please select an employee to reassign.")
                return
            person_id = current_emp_ids[selection[0]]
            target_role = "client"
            action_func = ctrl.assign_client_to_library

        elif current_tab_index == 1:
            selection = lb_cli.curselection()
            if not selection:
                messagebox.showwarning("Selection", "Please select a client to reassign.")
                return
            person_id = current_cli_ids[selection[0]]
            target_role = "employee"
            action_func = ctrl.assign_employee_to_library

        confirm = messagebox.askyesno(
            "Confirm Role Change",
            f"Are you sure you want to switch this person's role to {target_role.upper()}?"
        )

        if confirm:
            success, msg = action_func(person_id, library_id)
            if success:
                messagebox.showinfo("Success", f"Person reassigned as {target_role}.")
                win.destroy()
                view_library_info_window(parent_view, library_id, map_widget)
            else:
                messagebox.showerror("Error", msg)

    button_frame = tk.Frame(win)
    button_frame.pack(pady=10)


    tk.Button(button_frame, text="Switch Role (Selected)", command=toggle_role, bg="#ffecb3").pack(side="left", padx=5)

    if map_widget:
        pass

    tk.Button(button_frame, text="Close", command=win.destroy).pack(side="right", padx=5)


def add_book_window(parent_view):
    win = tk.Toplevel(parent_view)
    win.title("Add Book")
    win.geometry("350x400")

    tk.Label(win, text="Add New Book", font=("Arial", 12, "bold")).pack(pady=10)

    entries = {}
    fields = ["Title", "Author", "ISBN", "Publisher", "Genre"]

    for field in fields:
        frame = tk.Frame(win)
        frame.pack(fill="x", padx=10, pady=2)
        tk.Label(frame, text=f"{field}:", width=10, anchor="w").pack(side="left")
        e = tk.Entry(frame)
        e.pack(side="left", fill="x", expand=True)
        entries[field.lower()] = e

    def save_book():
        isbn = entries["isbn"].get().strip()
        if not isbn.isdigit() or len(isbn) != 13:
            messagebox.showerror("Error", "ISBN must be 13 digits.")
            return

        success, message = ctrl.add_book(
            title=entries["title"].get().strip(),
            author=entries["author"].get().strip(),
            isbn_13=isbn,
            publisher=entries["publisher"].get().strip(),
            genre=entries["genre"].get().strip()
        )

        if success:
            model.refresh_books()
            if hasattr(parent_view, 'sidebar'):
                parent_view.sidebar.switch_mode("Books")
            win.destroy()
        else:
            messagebox.showerror("Error", message)

    tk.Button(win, text="Save Book", command=save_book).pack(pady=15)