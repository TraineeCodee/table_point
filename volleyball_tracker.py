
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import os

# Constants and Style Setup
BG_COLOR = "#f0f8ff"
HEADER_BG = "#4682b4"
BTN_COLOR = "#1e90ff"
FONT_TITLE = ("Helvetica", 16, "bold")
FONT_LABEL = ("Helvetica", 12)
FONT_HEADER = ("Helvetica", 11, "bold")
KEYS = ("Matches Played", "Wins", "Loses", "Sets Won", "Points")
stored_data = {}
DATA_FILE = "teams_data.txt"

# --- Login and Registration ---

def register():
    global register_screen
    register_screen = tk.Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")
    register_screen.configure(bg=BG_COLOR)

    global username
    global password
    global username_entry
    global password_entry

    username = tk.StringVar()
    password = tk.StringVar()

    tk.Label(register_screen, text="Please enter details below", bg=HEADER_BG, fg="white", font=FONT_LABEL).pack(pady=5)
    tk.Label(register_screen, text="Username *", bg=BG_COLOR).pack()
    username_entry = tk.Entry(register_screen, textvariable=username)
    username_entry.pack()
    tk.Label(register_screen, text="Password *", bg=BG_COLOR).pack()
    password_entry = tk.Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    tk.Label(register_screen, text="", bg=BG_COLOR).pack()
    tk.Button(register_screen, text="Register", bg=BTN_COLOR, fg="white", width=12, command=register_user).pack()

def login():
    global login_screen
    login_screen = tk.Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    login_screen.configure(bg=BG_COLOR)

    global username_verify
    global password_verify
    global username_login_entry
    global password_login_entry

    username_verify = tk.StringVar()
    password_verify = tk.StringVar()

    tk.Label(login_screen, text="Login Below", bg=HEADER_BG, fg="white", font=FONT_LABEL).pack(pady=5)
    tk.Label(login_screen, text="Username *", bg=BG_COLOR).pack()
    username_login_entry = tk.Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    tk.Label(login_screen, text="Password *", bg=BG_COLOR).pack()
    password_login_entry = tk.Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    tk.Label(login_screen, text="", bg=BG_COLOR).pack()
    tk.Button(login_screen, text="Login", bg=BTN_COLOR, fg="white", width=12, command=login_verify).pack()

def register_user():
    username_info = username.get()
    password_info = password.get()
    if not username_info or not password_info:
        messagebox.showerror("Error", "Please enter both username and password.")
        return
    with open(username_info, "w") as file:
        file.write(username_info + "\n" + password_info)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Registration Successful!")
    register_screen.destroy()

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, tk.END)
    password_login_entry.delete(0, tk.END)

    if username1 in os.listdir():
        with open(username1, "r") as file:
            verify = file.read().splitlines()
        if password1 in verify:
            login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid Password")
    else:
        messagebox.showerror("Login Failed", "User Not Found")

def login_success():
    messagebox.showinfo("Success", "Login Successful!")
    #.destroy-remove display
    login_screen.destroy()
    main_screen.destroy()
    launch_tracker()

def main_account_screen():
    global main_screen
    main_screen = tk.Tk()
    main_screen.geometry("400x250")
    main_screen.title("Account Login")
    # BG_COLOR = "#ffffff"  # white, as an example
    main_screen.configure(bg=BG_COLOR)
    tk.Label(text="🏐 Volleyball Tracker 🏐", bg=HEADER_BG, fg="white", width="300", height="2", font=FONT_TITLE).pack()
    tk.Label(text="", bg=BG_COLOR).pack()
    tk.Button(text="Login", height="2", width="30", bg=BTN_COLOR, fg="white", command=login).pack(pady=5)
    tk.Button(text="Register", height="2", width="30", bg=BTN_COLOR, fg="white", command=register).pack(pady=5)
    main_screen.mainloop()

# --- Team Data Handling ---

def save_teams_to_file():
    #Saves team data to a text file (teams_data.txt).
    with open(DATA_FILE, "w") as f:
        for name, stats in stored_data.items():
            values = [str(stats[key].get()) for key in KEYS]
            f.write(f"{name}:{','.join(values)}\n")

def load_teams_from_file():
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r") as f:
        for line in f:
            #.strip access as one by one
            line = line.strip()
            if ":" in line:
                name, data = line.split(":")
                values = list(map(int, data.split(",")))
                create_player(name, *values)

def create_player(name, matches=0, wins=0, loses=0, sets=0, points=0):
    statistics = {}
    for key, val in zip(KEYS, (matches, wins, loses, sets, points)):
        statistics[key] = tk.IntVar(value=val)
    stored_data[name] = statistics

def edit_player(parent, name):
    def change(var, delta):
        value = var.get() + delta
        if value >= 0:
            var.set(value)

    def create_form(parent, key, var):
        f = tk.Frame(parent, bd=1, relief="ridge", bg=BG_COLOR)
        f.pack(side="left", padx=5)
        tk.Label(f, text=key, width=12, fg="white", bg=HEADER_BG).grid(row=0, column=0, columnspan=3)
        tk.Button(f, text="-", command=lambda: change(var, -1), bg="red", fg="white").grid(row=1, column=0, sticky="ew")
        tk.Label(f, textvariable=var, width=3, bg=BG_COLOR, fg="black").grid(row=1, column=1)
        tk.Button(f, text="+", command=lambda: change(var, 1), bg="green", fg="white").grid(row=1, column=2, sticky="ew")

    def on_close():
        save_teams_to_file()
        tp.destroy()

    tp = tk.Toplevel(parent)
    tp.title(f"Edit {name}'s Stats")
    tk.Label(tp, text=name, font=FONT_TITLE).pack(pady=5)
    frame = tk.Frame(tp, bg=BG_COLOR)
    frame.pack()
    statistics = stored_data[name]
    for key, var in statistics.items():
        create_form(frame, key, var)
    tp.protocol("WM_DELETE_WINDOW", on_close)
    tp.grab_set()
    tp.wait_window()

def add_player_row(parent, row, name):
    tk.Label(parent, text=name, anchor="w", width=20, bg="#e6f2ff").grid(row=row, column=0, sticky="ew")
    statistics = stored_data[name]
    for col, key in enumerate(KEYS, 1):
        tk.Label(parent, textvariable=statistics[key], bg="#e6f2ff", fg="black").grid(row=row, column=col)
    tk.Button(parent, text="Edit", command=lambda: edit_player(root, name), bg=BTN_COLOR, fg="white").grid(row=row, column=col+1)

def new_player(parent):
    name = askstring("New Team", "Enter Team Name:")
    if name and name not in stored_data:
        create_player(name)
        add_player_row(parent, len(stored_data), name)
        save_teams_to_file()

def launch_tracker():
    global root
    root = tk.Tk()
    root.title("Volleyball Point Tracker")
    root.configure(bg=BG_COLOR)

    load_teams_from_file()

    tk.Label(root, text="🏐 Baselios Volleyball Tracker 🏐", font=FONT_TITLE, fg="white", bg=HEADER_BG).pack(pady=10)

    table_frame = tk.Frame(root, bg=BG_COLOR)
    table_frame.pack()

    tk.Label(table_frame, text="Team Name", font=FONT_HEADER, bg=HEADER_BG, fg="white", width=20).grid(row=0, column=0, sticky="ew")
    for col, key in enumerate(KEYS, 1):
        tk.Label(table_frame, text=key, font=FONT_HEADER, bg=HEADER_BG, fg="white", width=12).grid(row=0, column=col)
    tk.Label(table_frame, bg=HEADER_BG, width=10).grid(row=0, column=col+1)

    for row, name in enumerate(stored_data, 1):
        add_player_row(table_frame, row, name)

    tk.Button(root, text="Add New Team", command=lambda: new_player(table_frame), bg="orange", fg="white").pack(pady=10)
    root.mainloop()

# Start the app
main_account_screen()
