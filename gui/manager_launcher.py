import tkinter as tk
from tkinter import ttk, messagebox
import requests

API = "http://127.0.0.1:5000"


def safe_get_json(url):
    try:
        r = requests.get(url)
        if r.ok:
            return r.json()
    except Exception:
        pass
    return []


class ManagerApp:
    def __init__(self, root):
        self.root = root
        root.title("GRC Manager")
        root.geometry("700x520")

        nb = ttk.Notebook(root)
        nb.pack(fill=tk.BOTH, expand=True)

        self.event_tab = ttk.Frame(nb)
        self.user_tab = ttk.Frame(nb)
        self.asset_tab = ttk.Frame(nb)
        self.policy_tab = ttk.Frame(nb)

        nb.add(self.event_tab, text="Events")
        nb.add(self.user_tab, text="Users")
        nb.add(self.asset_tab, text="Assets")
        nb.add(self.policy_tab, text="Policies")

        self.build_event_tab()
        self.build_user_tab()
        self.build_asset_tab()
        self.build_policy_tab()

    # Event tab
    def build_event_tab(self):
        f = self.event_tab
        tk.Label(f, text="User").pack()
        self.event_user = ttk.Combobox(f, values=[])
        self.event_user.pack()

        tk.Label(f, text="Asset").pack()
        self.event_asset = ttk.Combobox(f, values=[])
        self.event_asset.pack()

        tk.Label(f, text="Event Type").pack()
        self.event_type = ttk.Combobox(f, values=["USB_CONNECTED","LOGIN","PATCH_MISSING","LOGIN_FAILED","ACCESS_DENIED"]) 
        self.event_type.pack()

        tk.Label(f, text="Description").pack()
        self.event_desc = tk.Entry(f, width=80)
        self.event_desc.pack()

        btn_frame = tk.Frame(f)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Create Event", command=self.create_event).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Refresh", command=self.load_event_choices).pack(side=tk.LEFT, padx=4)

        self.event_status = tk.Label(f)
        self.event_status.pack()

        self.load_event_choices()

    def load_event_choices(self):
        users = safe_get_json(f"{API}/users")
        assets = safe_get_json(f"{API}/assets")
        self.user_map = {u['username']: u['id'] for u in users}
        self.asset_map = {a['name']: a['id'] for a in assets}
        self.event_user['values'] = [u['username'] for u in users]
        self.event_asset['values'] = [a['name'] for a in assets]

    def create_event(self):
        u = self.event_user.get()
        a = self.event_asset.get()
        if u not in self.user_map or a not in self.asset_map:
            messagebox.showerror("Error", "Select valid user and asset and refresh if needed")
            return
        payload = {
            'user_id': self.user_map[u],
            'asset_id': self.asset_map[a],
            'event_type': self.event_type.get(),
            'description': self.event_desc.get()
        }
        try:
            r = requests.post(f"{API}/events", json=payload)
            if r.ok:
                self.event_status.config(text="Created")
            else:
                self.event_status.config(text=f"Error: {r.status_code}")
        except Exception as e:
            self.event_status.config(text=f"Error: {e}")

    # User tab
    def build_user_tab(self):
        f = self.user_tab
        self.user_list = tk.Listbox(f, height=8)
        self.user_list.pack(fill=tk.X)

        tk.Label(f, text="Username").pack(anchor=tk.W)
        self.u_name = tk.Entry(f)
        self.u_name.pack(fill=tk.X)

        tk.Label(f, text="Role").pack(anchor=tk.W)
        self.u_role = tk.Entry(f)
        self.u_role.pack(fill=tk.X)

        tk.Label(f, text="Department").pack(anchor=tk.W)
        self.u_dept = tk.Entry(f)
        self.u_dept.pack(fill=tk.X)

        btn_frame = tk.Frame(f)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Create User", command=self.create_user).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Refresh", command=self.load_users).pack(side=tk.LEFT, padx=4)

        self.user_status = tk.Label(f)
        self.user_status.pack()

        self.load_users()

    def load_users(self):
        self.user_map = {}
        self.user_list.delete(0, tk.END)
        for u in safe_get_json(f"{API}/users"):
            disp = f"{u['username']} (id:{u['id']})"
            self.user_list.insert(tk.END, disp)
            self.user_map[disp] = u

    def create_user(self):
        payload = {
            'username': self.u_name.get().strip(),
            'role': self.u_role.get().strip() or 'user',
            'department': self.u_dept.get().strip() or 'unknown'
        }
        if not payload['username']:
            messagebox.showerror('Error', 'Username required')
            return
        try:
            r = requests.post(f"{API}/users", json=payload)
            if r.ok:
                self.user_status.config(text='User created')
                self.load_users()
            else:
                self.user_status.config(text=f'Error: {r.status_code}')
        except Exception as e:
            self.user_status.config(text=f'Error: {e}')

    # Asset tab
    def build_asset_tab(self):
        f = self.asset_tab
        self.asset_list = tk.Listbox(f, height=8)
        self.asset_list.pack(fill=tk.X)

        tk.Label(f, text="Name").pack(anchor=tk.W)
        self.a_name = tk.Entry(f)
        self.a_name.pack(fill=tk.X)

        tk.Label(f, text="Type").pack(anchor=tk.W)
        self.a_type = tk.Entry(f)
        self.a_type.pack(fill=tk.X)

        tk.Label(f, text="Department").pack(anchor=tk.W)
        self.a_dept = tk.Entry(f)
        self.a_dept.pack(fill=tk.X)

        tk.Label(f, text="Criticality").pack(anchor=tk.W)
        self.a_crit = ttk.Combobox(f, values=["low","medium","high","critical"])
        self.a_crit.pack(fill=tk.X)

        tk.Label(f, text="Owner").pack(anchor=tk.W)
        self.a_owner = tk.Entry(f)
        self.a_owner.pack(fill=tk.X)

        btn_frame = tk.Frame(f)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Create Asset", command=self.create_asset).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Refresh", command=self.load_assets).pack(side=tk.LEFT, padx=4)

        self.asset_status = tk.Label(f)
        self.asset_status.pack()

        self.load_assets()

    def load_assets(self):
        self.asset_map = {}
        self.asset_list.delete(0, tk.END)
        for a in safe_get_json(f"{API}/assets"):
            disp = f"{a.get('name')} (id:{a.get('id')})"
            self.asset_list.insert(tk.END, disp)
            self.asset_map[disp] = a

    def create_asset(self):
        payload = {
            'name': self.a_name.get().strip(),
            'asset_type': self.a_type.get().strip() or 'unknown',
            'department': self.a_dept.get().strip() or None,
            'criticality': self.a_crit.get().strip() or 'medium',
            'owner': self.a_owner.get().strip() or None
        }
        if not payload['name']:
            messagebox.showerror('Error', 'Name required')
            return
        try:
            r = requests.post(f"{API}/assets", json=payload)
            if r.ok:
                self.asset_status.config(text='Asset created')
                self.load_assets()
            else:
                self.asset_status.config(text=f'Error: {r.status_code}')
        except Exception as e:
            self.asset_status.config(text=f'Error: {e}')

    # Policy tab
    def build_policy_tab(self):
        f = self.policy_tab
        self.policy_list = tk.Listbox(f, height=8)
        self.policy_list.pack(fill=tk.X)

        tk.Label(f, text="Name").pack(anchor=tk.W)
        self.p_name = tk.Entry(f)
        self.p_name.pack(fill=tk.X)

        tk.Label(f, text="Event Type").pack(anchor=tk.W)
        self.p_event = ttk.Combobox(f, values=["USB_CONNECTED","LOGIN","PATCH_MISSING","LOGIN_FAILED","ACCESS_DENIED"]) 
        self.p_event.pack(fill=tk.X)

        tk.Label(f, text="Description").pack(anchor=tk.W)
        self.p_desc = tk.Entry(f)
        self.p_desc.pack(fill=tk.X)

        scores = tk.Frame(f)
        scores.pack(fill=tk.X, pady=4)
        tk.Label(scores, text="Prob").pack(side=tk.LEFT)
        self.p_prob = tk.Entry(scores, width=5)
        self.p_prob.pack(side=tk.LEFT, padx=4)
        tk.Label(scores, text="Impact").pack(side=tk.LEFT)
        self.p_impact = tk.Entry(scores, width=5)
        self.p_impact.pack(side=tk.LEFT, padx=4)
        tk.Label(scores, text="Conf").pack(side=tk.LEFT)
        self.p_conf = tk.Entry(scores, width=5)
        self.p_conf.pack(side=tk.LEFT, padx=4)
        tk.Label(scores, text="Integ").pack(side=tk.LEFT)
        self.p_integ = tk.Entry(scores, width=5)
        self.p_integ.pack(side=tk.LEFT, padx=4)
        tk.Label(scores, text="Avail").pack(side=tk.LEFT)
        self.p_avail = tk.Entry(scores, width=5)
        self.p_avail.pack(side=tk.LEFT, padx=4)

        btn_frame = tk.Frame(f)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Create Policy", command=self.create_policy).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Refresh", command=self.load_policies).pack(side=tk.LEFT, padx=4)

        self.policy_status = tk.Label(f)
        self.policy_status.pack()

        self.load_policies()

    def load_policies(self):
        self.policy_list.delete(0, tk.END)
        for p in safe_get_json(f"{API}/policies"):
            disp = f"{p.get('event_type')} - {p.get('description') or ''} (id:{p.get('id')})"
            self.policy_list.insert(tk.END, disp)

    def create_policy(self):
        def to_int(v):
            try:
                return int(v.get())
            except Exception:
                return 0

        payload = {
            'name': self.p_name.get().strip(),
            'description': self.p_desc.get().strip(),
            'event_type': self.p_event.get().strip(),
            'probability': to_int(self.p_prob),
            'impact': to_int(self.p_impact),
            'confidentiality': to_int(self.p_conf),
            'integrity': to_int(self.p_integ),
            'availability': to_int(self.p_avail)
        }
        if not payload['name'] or not payload['event_type']:
            messagebox.showerror('Error', 'Name and event type required')
            return
        try:
            r = requests.post(f"{API}/policies", json=payload)
            if r.ok:
                self.policy_status.config(text='Policy created')
                self.load_policies()
            else:
                self.policy_status.config(text=f'Error: {r.status_code}')
        except Exception as e:
            self.policy_status.config(text=f'Error: {e}')


def main():
    root = tk.Tk()
    app = ManagerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()