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
        self.root.resizable(True, True)

        # ----- Charger l'image originale -----
        self.original_image = Image.open(r"C:\Users\MSI\Pictures\IMG_20260313_205909.jpg")
        self.original_image = self.original_image.filter(ImageFilter.GaussianBlur(radius=5))

        # ----- Canvas -----
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # ----- Image de fond -----
        self.bg_image = ImageTk.PhotoImage(self.original_image.resize((700, 500)))
        self.bg_canvas = self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # ----- Texte bienvenue -----
        self.welcome_text = self.canvas.create_text(0, 0, text=f"Bienvenue {username}",
                                                    font=("Arial", 22, "bold"), fill="white")

        # ----- Boutons principaux -----
        self.btn_lignes = self.create_card_button("🔗", "Gestion des Lignes", self.open_lignes)
        self.btn_bus = self.create_card_button("🚌", "Gestion des Bus", self.open_bus)
        self.btn_stations = self.create_card_button("📍", "Gestion des Stations", self.open_stations)
        self.btn_voyages = self.create_card_button("🗺", "Gestion des Voyages", self.open_voyages)
        self.btn_monitoring = self.create_card_button("🎯", "Monitoring Temps Réel", self.open_monitoring)

        # ----- Bouton Déconnexion simple -----
        self.btn_logout = tk.Button(
            self.root,
            text="Déconnexion",
            command=self.logout,
            bg="#E57C1F",  # rouge
            fg="white",
            font=("Arial", 12, "bold"),
            bd=0,
            relief="ridge",
            padx=10,
            pady=5
        )

        # ----- Ajouter boutons au Canvas -----
        self.win_lignes = self.canvas.create_window(0, 0, window=self.btn_lignes)
        self.win_bus = self.canvas.create_window(0, 0, window=self.btn_bus)
        self.win_stations = self.canvas.create_window(0, 0, window=self.btn_stations)
        self.win_voyages = self.canvas.create_window(0, 0, window=self.btn_voyages)
        self.win_monitoring = self.canvas.create_window(0, 0, window=self.btn_monitoring)
        self.win_logout = self.canvas.create_window(0, 0, window=self.btn_logout)

        # ----- Bind resize -----
        self.root.bind("<Configure>", self.on_resize)

        self.root.mainloop()

    def create_card_button(self, icon, text, command):
        frame = tk.Frame(self.root, bg="white", bd=3, relief="ridge")
        icon_label = tk.Label(frame, text=icon, font=("Arial", 18), bg="#FFE0C2", width=3, height=2)
        text_label = tk.Label(frame, text=text, font=("Arial", 12, "bold"), bg="#E57C1F", fg="white",
                              width=18, height=2)
        icon_label.pack(side="left", fill="y")
        text_label.pack(side="left", fill="both", expand=True)

        # Bind click
        frame.bind("<Button-1>", lambda e: command())
        icon_label.bind("<Button-1>", lambda e: command())
        text_label.bind("<Button-1>", lambda e: command())
        return frame

    # ----- Fonctions ouverture -----
    def open_lignes(self): GestionLignes()
    def open_bus(self): GestionBus()
    def open_stations(self): GestionStations()
    def open_voyages(self): GestionVoyages()
    def open_monitoring(self): DashboardMonitoringPRO()
    
    def logout(self):
        self.root.destroy()
        from login import LoginWindow
        LoginWindow()

    # ----- Resize automatique stable -----
    def on_resize(self, event):
        if event.width < 100 or event.height < 100:
            return  # éviter erreur si fenêtre trop petite

        # Redimensionner l'image
        resized = self.original_image.resize((event.width, event.height))
        self.bg_image = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_canvas, image=self.bg_image)

        # Repositionner texte et boutons
        self.canvas.coords(self.welcome_text, event.width // 2, 50)
        left_x = event.width // 4
        right_x = 3 * event.width // 4
        start_y = 140
        gap_y = 100
        self.canvas.coords(self.win_lignes, left_x, start_y)
        self.canvas.coords(self.win_stations, left_x, start_y + gap_y)
        self.canvas.coords(self.win_monitoring, left_x, start_y + 2 * gap_y)
        self.canvas.coords(self.win_bus, right_x, start_y)
        self.canvas.coords(self.win_voyages, right_x, start_y + gap_y)

        # Position Déconnexion en bas à droite
        self.canvas.coords(self.win_logout, event.width - 80, event.height - 50)


if __name__ == "__main__":
    DashboardAdmin("Admin")
