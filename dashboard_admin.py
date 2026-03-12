import tkinter as tk
from gestion_lignes import GestionLignes
from gestion_bus import GestionBus
from gestion_stations import GestionStations
from gestion_voyages import GestionVoyages
from dashboard_monitoring import DashboardMonitoringPRO

class DashboardAdmin:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title(f"Dashboard Admin - {username}")
        self.root.geometry("700x500")
        self.root.configure(bg="white")

        # ----- Header -----
        header = tk.Frame(self.root, bg="#EBCEB0", height=70)
        header.pack(fill="x")
        tk.Label(
            header,
            text=f"Bienvenue {username}",
            font=("Arial", 20, "bold"),
            bg="#EBCEB0",
            fg="white"
        ).pack(pady=20)

        # ----- Container cartes / boutons -----
        card_frame = tk.Frame(self.root, bg="white")
        card_frame.pack(pady=20, padx=20, fill="both", expand=True)

        card_style = {
            "width": 25,
            "height": 3,
            "font": ("Arial", 12, "bold"),
            "bg": "#CC7000",
            "fg": "white",
            "bd": 0,
            "activebackground": "#D96F00",
            "activeforeground": "white"
        }

        tk.Button(card_frame, text="Gestion des Lignes", command=self.open_lignes, **card_style).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(card_frame, text="Gestion des Bus", command=self.open_bus, **card_style).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(card_frame, text="Gestion des Stations", command=self.open_stations, **card_style).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(card_frame, text="Gestion des Voyages", command=self.open_voyages, **card_style).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(card_frame, text="Monitoring Temps Réel", command=self.open_monitoring, **card_style).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.grid_columnconfigure(1, weight=1)

        # ----- Déconnexion (flèche moderne à droite) -----
        deco_frame = tk.Frame(self.root, bg="white")
        deco_frame.pack(side="bottom", fill="x", pady=15, padx=20)

        logout_btn = tk.Button(
            deco_frame,
            text="⮞",  # flèche moderne
            command=self.logout,
            bg="#D32F2F",  # cadre rouge
            fg="white",
            font=("Arial", 16, "bold"),
            width=3,
            height=1,
            bd=0,
            activebackground="#B71C1C",
            activeforeground="white"
        )
        logout_btn.pack(side="right")

        self.root.mainloop()

    # ----- Fonctions ouverture -----
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

    # ----- Déconnexion -----
    def logout(self):
        self.root.destroy()
        from login import LoginWindow
        LoginWindow()