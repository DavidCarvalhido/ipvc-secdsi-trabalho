import tkinter as tk
from tkinter import ttk, messagebox
import requests

API = "http://127.0.0.1:5000"


def load_users(listbox, users_map):
    try:
        r = requests.get(f"{API}/users")
        listbox.delete(0, tk.END)
        users_map.clear()
        if r.ok:
            for u in r.json():
                display = f"{u['username']} (id:{u['id']})"
                listbox.insert(tk.END, display)
                users_map[display] = u
    except Exception:
        pass


def create_user(username_var, role_var, dept_var, listbox, users_map, status):
    username = username_var.get().strip()
    if not username:
        messagebox.showerror("Error", "Username required")
        return

    payload = {
        "username": username,
        "role": role_var.get().strip() or "user",
        "department": dept_var.get().strip() or "unknown"
    }

    try:
        r = requests.post(f"{API}/users", json=payload)
        if r.ok:
            status.config(text="User created")
            load_users(listbox, users_map)
        else:
            status.config(text=f"Error: {r.status_code}")
    except Exception as e:
        status.config(text=f"Error: {e}")


def main():
    root = tk.Tk()
    root.title("User Manager")
    root.geometry("500x400")

    users_map = {}

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    listbox = tk.Listbox(frame, height=8)
    listbox.pack(fill=tk.X)

    tk.Label(frame, text="Username").pack(anchor=tk.W)
    username_var = tk.StringVar()
    tk.Entry(frame, textvariable=username_var).pack(fill=tk.X)

    tk.Label(frame, text="Role").pack(anchor=tk.W)
    role_var = tk.StringVar()
    tk.Entry(frame, textvariable=role_var).pack(fill=tk.X)

    tk.Label(frame, text="Department").pack(anchor=tk.W)
    dept_var = tk.StringVar()
    tk.Entry(frame, textvariable=dept_var).pack(fill=tk.X)

    status = tk.Label(root)
    status.pack()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=8)

    tk.Button(btn_frame, text="Create User", command=lambda: create_user(username_var, role_var, dept_var, listbox, users_map, status)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Refresh", command=lambda: load_users(listbox, users_map)).pack(side=tk.LEFT, padx=4)

    load_users(listbox, users_map)

    root.mainloop()


if __name__ == '__main__':
    main()