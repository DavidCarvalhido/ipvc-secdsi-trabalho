import tkinter as tk
from tkinter import ttk, messagebox
import requests

API = "http://127.0.0.1:5000"

# mappings nome -> id
user_map = {}
asset_map = {}


def load_choices():
    global user_map, asset_map
    try:
        r = requests.get(f"{API}/users")
        if r.ok:
            users = r.json()
            names = [u['username'] for u in users]
            user_map = {u['username']: u['id'] for u in users}
            user['values'] = names
    except Exception:
        pass

    try:
        r = requests.get(f"{API}/assets")
        if r.ok:
            assets = r.json()
            names = [a['name'] for a in assets]
            asset_map = {a['name']: a['id'] for a in assets}
            asset['values'] = names
    except Exception:
        pass


def submit():
    selected_user = user.get()
    selected_asset = asset.get()

    if selected_user not in user_map:
        messagebox.showerror("Error", "User not recognised. Refresh and try again.")
        return

    if selected_asset not in asset_map:
        messagebox.showerror("Error", "Asset not recognised. Refresh and try again.")
        return

    payload = {
        "user_id": user_map[selected_user],
        "asset_id": asset_map[selected_asset],
        "event_type": event_type.get(),
        "description": description.get(),
    }

    try:
        r = requests.post(f"{API}/events", json=payload)

        if r.ok:
            status.config(text="Created")
        else:
            status.config(text=f"Error: {r.status_code}")
    except Exception as e:
        status.config(text=f"Error: {e}")


root = tk.Tk()
root.title("GRC Event Creator")
root.geometry("500x400")

# USER
tk.Label(root, text="User").pack()
user = ttk.Combobox(root, values=[])
user.pack()

# ASSET
tk.Label(root, text="Asset").pack()
asset = ttk.Combobox(root, values=[])
asset.pack()

# EVENT TYPE (alinhado com backend)
tk.Label(root, text="Event Type").pack()
event_type = ttk.Combobox(
    root,
    values=[
        "USB_CONNECTED",
        "LOGIN",
        "PATCH_MISSING",
        "LOGIN_FAILED",
        "ACCESS_DENIED",
    ],
)
event_type.pack()

# DESCRIPTION
tk.Label(root, text="Description").pack()
description = tk.Entry(root, width=50)
description.pack()

tk.Button(root, text="Create Event", command=submit).pack(pady=20)

status = tk.Label(root)
status.pack()

# carregar choices do backend (se disponível)
load_choices()

root.mainloop()