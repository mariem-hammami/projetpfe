import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

# ----- Fenêtres secondaires simulées -----
from gestion_lignes import GestionLignes
from gestion_bus import GestionBus
from gestion_stations import GestionStations
from gestion_voyages import GestionVoyages
from dashboard_monitoring import DashboardMonitoringPRO

# ----- Dashboard Monitoring simulé -----
class DashboardMonitoringSRTB:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Monitoring Temps Réel - SRTB")
        self.root.geometry("750x500")
        self.root.configure(bg="white")

        tk.Label(self.root, text="Monitoring Passagers – Temps Réel",
                 font=("Arial", 16, "bold"), bg="white", fg="#228B22").pack(pady=10)

        # Total Passagers
        self.total_label = tk.Label(self.root, text="Total Passagers: 0 (A/D: 0/0)",
                                    font=("Arial", 14, "bold"), bg="white")
        self.total_label.pack(pady=5)

        # Tableau Passagers par station
        columns = ("station", "ascendant", "descendant")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Alertes
        self.alertes_text = tk.Text(self.root, height=5, bg="#F5F5F5")
        self.alertes_text.pack(fill="x", padx=10, pady=5)
        self.alertes_text.insert("end", "Alertes: Aucune pour le moment...\n")
        self.alertes_text.config(state="disabled")

        # Rafraîchir
        tk.Button(self.root, text="Rafraîchir", bg="#228B22", fg="white",
                  command=self.update_dashboard).pack(pady=5)

        # Stations simulées
        self.stations = ["Corniche", "Manzel Abed Rahmen", "Tunis"]
        self.data = {s: {"asc": 0, "desc": 0} for s in self.stations}
        self.total_asc = 0
        self.total_desc = 0

        self.update_dashboard()
        self.root.mainloop()

    def update_dashboard(self):
        for s in self.stations:
            new_asc = random.randint(0, 5)
            new_desc = random.randint(0, 3)
            self.data[s]["asc"] += new_asc
            self.data[s]["desc"] += new_desc
            self.total_asc += new_asc
            self.total_desc += new_desc

        total = self.total_asc - self.total_desc
        self.total_label.config(text=f"Total Passagers: {total} (A/D: {self.total_asc}/{self.total_desc})")

        # Tableau
        for row in self.tree.get_children():
            self.tree.delete(row)
        for s in self.stations:
            self.tree.insert("", "end", values=(s, self.data[s]["asc"], self.data[s]["desc"]))

        # Alertes aléatoires
        self.alertes_text.config(state="normal")
        self.alertes_text.delete("1.0", "end")
        if random.choice([True, False]):
            self.alertes_text.insert("end",
                                     f"[{datetime.now().strftime('%H:%M:%S')}] Bus en retard à {random.choice(self.stations)}\n")
        else:
            self.alertes_text.insert("end", "Aucune alerte pour le moment...\n")
        self.alertes_text.config(state="disabled")

        # Auto-refresh
        self.root.after(10000, self.update_dashboard)


class DashboardAdmin:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title(f"Dashboard Admin - {username}")
        self.root.geometry("550x500")
        self.root.configure(bg="black")  # fond noir comme login

        # ----- Header -----
        header = tk.Frame(self.root, bg="#FF8C00", height=60)
        header.pack(fill="x")
        tk.Label(header, text=f"Bienvenue {username}", font=("Arial", 18, "bold"),
                 bg="#FF8C00", fg="black").pack(pady=15)

        # ----- Frame des boutons -----
        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(pady=20)

        # Style bouton commun
        button_style = {"width": 30, "bg": "#FF8C00", "fg": "black", 
                        "font": ("Arial", 12, "bold"), "bd": 0, 
                        "activebackground": "#FFA500", "activeforeground": "black"}

        tk.Button(btn_frame, text="Gestion des Lignes", command=self.open_lignes, **button_style).pack(pady=5)
        tk.Button(btn_frame, text="Gestion des Bus", command=self.open_bus, **button_style).pack(pady=5)
        tk.Button(btn_frame, text="Gestion des Stations", command=self.open_stations, **button_style).pack(pady=5)
        tk.Button(btn_frame, text="Gestion des Voyages", command=self.open_voyages, **button_style).pack(pady=5)
        tk.Button(btn_frame, text="Monitoring Temps Réel", command=self.open_monitoring, **button_style).pack(pady=5)
        
        # ----- Déconnexion -----
        # Déconnexion en bas
        deco_frame = tk.Frame(self.root, bg="white")
        deco_frame.pack(side="bottom", fill="x", pady=10)

        tk.Button(deco_frame, text="Déconnexion", command=self.root.destroy,
          bg="gray", fg="white", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        self.root.mainloop()

    def open_lignes(self):
        GestionLignes()

    def open_bus(self):
        GestionBus()

    def open_stations(self):
        GestionStations()

    def open_voyages(self):
        GestionVoyages()

    def open_monitoring(self):
        DashboardMonitoringPRO()

    