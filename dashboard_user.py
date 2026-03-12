import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db
import datetime


class DashboardUser:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title(f"Dashboard Utilisateur - {username}")
        self.root.geometry("900x500")
        self.root.configure(bg="white")

        # ----- Header -----
        header_bg = "#D35400"  # orange sombre pour le header
        header = tk.Frame(self.root, bg=header_bg, height=50)
        header.pack(fill="x")

        tk.Label(
            header,
            text=f"Bienvenue {username}",
            bg=header_bg,
            fg="white",
            font=("Arial", 16, "bold")
        ).pack(side="left", padx=10, pady=10)

        # ----- Bouton Déconnexion -----
        tk.Button(
            header,
            text="Déconnexion",
            command=self.logout,
            bg="#E67E22",               # bouton légèrement plus clair
            fg="white",
            font=("Arial", 12, "bold"),
            activebackground="#BA4A00", # survol un peu plus sombre
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=5
        ).pack(side="right", padx=10, pady=5)

        # ----- Total Passagers -----
        self.total_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10, bg="white")
        self.total_frame.place(x=10, y=60, width=400, height=100)

        # Texte "Total Passagers Aujourd'hui" en couleur sombre
        total_label_color = "#D35400"  # orange sombre

        tk.Label(
            self.total_frame,
            text="Total Passagers Aujourd'hui",
            font=("Arial", 14, "bold"),
            fg=total_label_color,
            bg="white"
        ).pack()

        self.total_label = tk.Label(
            self.total_frame,
            text="Asc: 0  | Desc: 0",
            font=("Arial", 12),
            fg="#FF8C00",
            bg="white"
        )
        self.total_label.pack()

        # ----- Tableau Ligne / Station -----
        self.table_frame = tk.Frame(self.root, bg="white")
        self.table_frame.place(x=10, y=180, width=880, height=250)

        columns = ("ligne", "station", "asc", "desc")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        self.tree.heading("ligne", text="Ligne")
        self.tree.heading("station", text="Station")
        self.tree.heading("asc", text="Ascendant")
        self.tree.heading("desc", text="Descendant")

        self.tree.column("ligne", width=150)
        self.tree.column("station", width=300)
        self.tree.column("asc", width=100)
        self.tree.column("desc", width=100)

        self.tree.pack(fill="both", expand=True)

        # ----- Style Tableau -----
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="white",
            foreground="#FF8C00",
            fieldbackground="white",
            font=("Arial", 12)
        )
        style.map(
            "Treeview",
            background=[("selected", "#FF8C00")],
            foreground=[("selected", "white")]
        )

        # ----- Footer -----
        footer = tk.Frame(self.root, bg="#D3D3D3", height=30)
        footer.pack(fill="x", side="bottom")

        tk.Label(
            footer,
            text=f"Version 1.0 | {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}",
            bg="#D3D3D3"
        ).pack()

        # Charger données
        self.update_dashboard()

        # Rafraîchissement automatique toutes les 10 secondes
        self.root.after(10000, self.update_dashboard)

        self.root.mainloop()

    # ---------------- Dashboard Data ----------------
    def update_dashboard(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            today = datetime.date.today()

            # ----- Total passagers -----
            cursor.execute("""
                SELECT SUM(nombre_ascendant), SUM(nombre_descendant)
                FROM comptage
                WHERE DATE(date_comptage) = %s
            """, (today,))

            result = cursor.fetchone()
            asc_total = result[0] if result[0] else 0
            desc_total = result[1] if result[1] else 0

            self.total_label.config(
                text=f"Asc: {asc_total}  | Desc: {desc_total}"
            )

            # ----- Tableau -----
            for row in self.tree.get_children():
                self.tree.delete(row)

            cursor.execute("""
                SELECT l.libelle_ligne,
                       s.libelle_station,
                       SUM(c.nombre_ascendant),
                       SUM(c.nombre_descendant)
                FROM comptage c
                JOIN station s ON c.id_station = s.id_station
                JOIN ligne_station ls ON s.id_station = ls.id_station
                JOIN ligne l ON ls.id_ligne = l.id_ligne
                WHERE DATE(c.date_comptage) = %s
                GROUP BY l.libelle_ligne, s.libelle_station, ls.ordre
                ORDER BY l.libelle_ligne, ls.ordre
            """, (today,))

            rows = cursor.fetchall()
            for r in rows:
                ligne, station, asc, desc = r
                asc = asc if asc else 0
                desc = desc if desc else 0
                self.tree.insert("", "end", values=(ligne, station, asc, desc))

            conn.close()

        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

        # Rafraîchissement auto
        self.root.after(10000, self.update_dashboard)

    # ---------------- Logout ----------------
    def logout(self):
        self.root.destroy()
        from login import LoginWindow
        LoginWindow()