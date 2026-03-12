import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import verify_login
from dashboard_admin import DashboardAdmin
from dashboard_user import DashboardUser

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Transport App - Login")
        self.geometry("350x400")
        self.configure(bg="white")  # fond blanc

        # ----- Logo SRTB -----
        try:
            logo_image = Image.open("srtb_logo.png")
            logo_image = logo_image.resize((150, 150))
            self.logo = ImageTk.PhotoImage(logo_image)
            tk.Label(self, image=self.logo, bg="white").pack(pady=10)
        except:
            tk.Label(
                self, text="SRTB", font=("Arial", 24, "bold"), fg="#FF8C00", bg="white"
            ).pack(pady=10)

        # ----- Champs login -----
        tk.Label(self, text="Nom d'utilisateur", fg="black", bg="white").pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 12), bd=2, relief="solid")
        self.username_entry.pack(pady=5, ipady=5)

        tk.Label(self, text="Mot de passe", fg="black", bg="white").pack(pady=5)
        self.password_entry = tk.Entry(
            self, font=("Arial", 12), show="*", bd=2, relief="solid"
        )
        self.password_entry.pack(pady=5, ipady=5)

        # ----- Bouton login -----
        tk.Button(
            self,
            text="Se connecter",
            bg="#FF8C00",
            fg="black",
            font=("Arial", 14, "bold"),
            width=20,
            command=self.login
        ).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            result = verify_login(username, password)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de connexion à la base : {e}")
            return

        if result:
            role = result[0]
            self.destroy()
            if role == "admin":
                DashboardAdmin(username)
            elif role == "user":
                DashboardUser(username)
            else:
                messagebox.showerror("Erreur", "Identifiants incorrects")
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")