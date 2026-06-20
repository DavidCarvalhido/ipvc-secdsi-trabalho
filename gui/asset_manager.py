import tkinter as tk
from tkinter import ttk, messagebox
import requests

API = "http://127.0.0.1:5000"


def load_assets(listbox, assets_map):
    try:
        r = requests.get(f"{API}/assets")
        listbox.delete(0, tk.END)
        assets_map.clear()
        if r.ok:
            for a in r.json():
                display = f"{a.get('name')} (id:{a.get('id')})"
                listbox.insert(tk.END, display)
                assets_map[display] = a
    except Exception:
        pass


def create_asset(name_var, type_var, dept_var, crit_var, owner_var, listbox, assets_map, status):
    name = name_var.get().strip()
    if not name:
        messagebox.showerror("Error", "Name required")
        return

    payload = {
        "name": name,
        "asset_type": type_var.get().strip() or "unknown",
        "department": dept_var.get().strip(),
        "criticality": crit_var.get().strip() or "medium",
        "owner": owner_var.get().strip() or None
    }

    try:
        r = requests.post(f"{API}/assets", json=payload)
        if r.ok:
            status.config(text="Asset created")
            load_assets(listbox, assets_map)
        else:
            status.config(text=f"Error: {r.status_code}")
    except Exception as e:
        status.config(text=f"Error: {e}")


def main():
    root = tk.Tk()
    root.title("Asset Manager")
    root.geometry("500x450")

    assets_map = {}

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    listbox = tk.Listbox(frame, height=8)
    listbox.pack(fill=tk.X)

    tk.Label(frame, text="Name").pack(anchor=tk.W)
    name_var = tk.StringVar()
    tk.Entry(frame, textvariable=name_var).pack(fill=tk.X)

    tk.Label(frame, text="Type").pack(anchor=tk.W)
    type_var = tk.StringVar()
    tk.Entry(frame, textvariable=type_var).pack(fill=tk.X)

    tk.Label(frame, text="Department").pack(anchor=tk.W)
    dept_var = tk.StringVar()
    tk.Entry(frame, textvariable=dept_var).pack(fill=tk.X)

    tk.Label(frame, text="Criticality").pack(anchor=tk.W)
    crit_var = tk.StringVar()
    crit_combo = ttk.Combobox(frame, textvariable=crit_var, values=["low", "medium", "high", "critical"]) 
    crit_combo.pack(fill=tk.X)

    tk.Label(frame, text="Owner").pack(anchor=tk.W)
    owner_var = tk.StringVar()
    tk.Entry(frame, textvariable=owner_var).pack(fill=tk.X)

    status = tk.Label(root)
    status.pack()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=8)

    tk.Button(btn_frame, text="Create Asset", command=lambda: create_asset(name_var, type_var, dept_var, crit_var, owner_var, listbox, assets_map, status)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Refresh", command=lambda: load_assets(listbox, assets_map)).pack(side=tk.LEFT, padx=4)

    load_assets(listbox, assets_map)

    root.mainloop()


if __name__ == '__main__':
    main()