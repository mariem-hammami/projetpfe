import tkinter as tk
from PIL import Image, ImageTk, ImageFilter

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
        self.root.resizable(False, False)

        # ----- Charger et flouter l'image -----
        image = Image.open(r"C:\Users\MSI\Pictures\IMG_20260313_205909.jpg")
        image = image.resize((700, 500))
        image = image.filter(ImageFilter.GaussianBlur(radius=5))
        self.bg_image = ImageTk.PhotoImage(image)

        # ----- Canvas -----
        self.canvas = tk.Canvas(self.root, width=700, height=500, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # ----- Texte bienvenue -----
        self.canvas.create_text(
            350, 50,
            text=f"Bienvenue {username}",
            font=("Arial", 22, "bold"),
            fill="white"
        )

        # ----- Boutons -----
        btn_lignes = self.create_card_button("🔗", "Gestion des Lignes", self.open_lignes)
        btn_bus = self.create_card_button("🚌", "Gestion des Bus", self.open_bus)
        btn_stations = self.create_card_button("📍", "Gestion des Stations", self.open_stations)
        btn_voyages = self.create_card_button("🗺", "Gestion des Voyages", self.open_voyages)
        btn_monitoring = self.create_card_button("🎯", "Monitoring Temps Réel", self.open_monitoring)

        # ----- Placement des boutons -----

        # colonne gauche
        self.canvas.create_window(170, 140, window=btn_lignes)
        self.canvas.create_window(170, 240, window=btn_stations)
        self.canvas.create_window(170, 340, window=btn_monitoring)

        # colonne droite
        self.canvas.create_window(530, 140, window=btn_bus)
        self.canvas.create_window(530, 240, window=btn_voyages)

        # ----- Bouton déconnexion -----
        self.btn_logout = tk.Button(
            self.root,
            text="➤",
            command=self.logout,
            bg="#D32F2F",
            fg="white",
            font=("Arial", 18, "bold"),
            width=3,
            height=1,
            bd=0
        )

        self.canvas.create_window(650, 450, window=self.btn_logout)

        self.root.mainloop()

    # ---------- Bouton style carte ----------
    def create_card_button(self, icon, text, command):

        frame = tk.Frame(
            self.root,
            bg="white",
            bd=3,
            relief="ridge"
        )

        icon_label = tk.Label(
            frame,
            text=icon,
            font=("Arial", 18),
            bg="#FFE0C2",
            width=3,
            height=2
        )

        text_label = tk.Label(
            frame,
            text=text,
            font=("Arial", 12, "bold"),
            bg="#E57C1F",
            fg="white",
            width=18,
            height=2
        )

        icon_label.pack(side="left", fill="y")
        text_label.pack(side="left", fill="both", expand=True)

        # rendre cliquable
        frame.bind("<Button-1>", lambda e: command())
        icon_label.bind("<Button-1>", lambda e: command())
        text_label.bind("<Button-1>", lambda e: command())

        return frame

    # ---------- Fonctions ouverture ----------

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

    # ---------- Déconnexion ----------

    def logout(self):
        self.root.destroy()
        from login import LoginWindow
        LoginWindow()
