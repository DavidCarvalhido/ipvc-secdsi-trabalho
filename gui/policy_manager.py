import tkinter as tk
from tkinter import ttk, messagebox
import requests

API = "http://127.0.0.1:5000"


def load_policies(listbox, policies_map):
    try:
        r = requests.get(f"{API}/policies")
        listbox.delete(0, tk.END)
        policies_map.clear()
        if r.ok:
            for p in r.json():
                display = f"{p.get('event_type')} - {p.get('description') or ''} (id:{p.get('id')})"
                listbox.insert(tk.END, display)
                policies_map[display] = p
    except Exception:
        pass


def create_policy(name_var, event_var, prob_var, impact_var, conf_var, integ_var, avail_var, desc_var, listbox, policies_map, status):
    name = name_var.get().strip()
    event_type = event_var.get().strip()

    if not name or not event_type:
        messagebox.showerror("Error", "Name and Event Type are required")
        return

    def to_int(v, default=0):
        try:
            return int(v.get())
        except Exception:
            return default

    payload = {
        "name": name,
        "description": desc_var.get().strip(),
        "event_type": event_type,
        "probability": to_int(prob_var, 0),
        "impact": to_int(impact_var, 0),
        "confidentiality": to_int(conf_var, 0),
        "integrity": to_int(integ_var, 0),
        "availability": to_int(avail_var, 0)
    }

    try:
        r = requests.post(f"{API}/policies", json=payload)
        if r.ok:
            status.config(text="Policy created")
            load_policies(listbox, policies_map)
        else:
            status.config(text=f"Error: {r.status_code}")
    except Exception as e:
        status.config(text=f"Error: {e}")


def main():
    root = tk.Tk()
    root.title("Policy Manager")
    root.geometry("600x500")

    policies_map = {}

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    listbox = tk.Listbox(frame, height=8)
    listbox.pack(fill=tk.X)

    tk.Label(frame, text="Name").pack(anchor=tk.W)
    name_var = tk.StringVar()
    tk.Entry(frame, textvariable=name_var).pack(fill=tk.X)

    tk.Label(frame, text="Event Type").pack(anchor=tk.W)
    event_var = tk.StringVar()
    event_combo = ttk.Combobox(frame, textvariable=event_var, values=["USB_CONNECTED","LOGIN","PATCH_MISSING","LOGIN_FAILED","ACCESS_DENIED"]) 
    event_combo.pack(fill=tk.X)

    tk.Label(frame, text="Description").pack(anchor=tk.W)
    desc_var = tk.StringVar()
    tk.Entry(frame, textvariable=desc_var).pack(fill=tk.X)

    # numeric scores
    row = tk.Frame(frame)
    row.pack(fill=tk.X, pady=4)
    tk.Label(row, text="Probability").pack(side=tk.LEFT)
    prob_var = tk.StringVar(value="0")
    tk.Entry(row, textvariable=prob_var, width=5).pack(side=tk.LEFT, padx=4)
    tk.Label(row, text="Impact").pack(side=tk.LEFT)
    impact_var = tk.StringVar(value="0")
    tk.Entry(row, textvariable=impact_var, width=5).pack(side=tk.LEFT, padx=4)

    row2 = tk.Frame(frame)
    row2.pack(fill=tk.X, pady=4)
    tk.Label(row2, text="Confidentiality").pack(side=tk.LEFT)
    conf_var = tk.StringVar(value="0")
    tk.Entry(row2, textvariable=conf_var, width=5).pack(side=tk.LEFT, padx=4)
    tk.Label(row2, text="Integrity").pack(side=tk.LEFT)
    integ_var = tk.StringVar(value="0")
    tk.Entry(row2, textvariable=integ_var, width=5).pack(side=tk.LEFT, padx=4)
    tk.Label(row2, text="Availability").pack(side=tk.LEFT)
    avail_var = tk.StringVar(value="0")
    tk.Entry(row2, textvariable=avail_var, width=5).pack(side=tk.LEFT, padx=4)

    status = tk.Label(root)
    status.pack()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=8)

    tk.Button(btn_frame, text="Create Policy", command=lambda: create_policy(name_var, event_var, prob_var, impact_var, conf_var, integ_var, avail_var, desc_var, listbox, policies_map, status)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Refresh", command=lambda: load_policies(listbox, policies_map)).pack(side=tk.LEFT, padx=4)

    load_policies(listbox, policies_map)

    root.mainloop()


if __name__ == '__main__':
    main()