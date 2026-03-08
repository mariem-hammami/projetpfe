import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db
import datetime

class DashboardUser:
    def __init__(self, username):
        self.root = tk.Tk()  
        self.root.title(f"Dashboard Utilisateur - {username}")
        self.root.geometry("900x500")

        # ----- Header -----
        header = tk.Frame(self.root, bg="#FF8C00", height=50)  # orange
        header.pack(fill="x")
        tk.Label(header, text=f"Bienvenue {username}", bg="#FF8C00", fg="black",
                 font=("Arial", 16, "bold")).pack(side="left", padx=10)
        tk.Button(header, text="Déconnexion", command=self.root.destroy,
                  bg="black", fg="white", font=("Arial", 12, "bold"),
                  activebackground="#333333", activeforeground="#FF8C00").pack(side="right", padx=10)

        # ----- Total Passagers -----
        self.total_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
        self.total_frame.place(x=10, y=60, width=400, height=100)
        tk.Label(self.total_frame, text="Total Passagers Aujourd'hui",
                 font=("Arial", 14, "bold"), fg="#FF8C00").pack()
        self.total_label = tk.Label(self.total_frame, text="Asc: 0  | Desc: 0",
                                    font=("Arial", 12), fg="#FF8C00")
        self.total_label.pack()

        # ----- Tableau Ligne/Station -----
        self.table_frame = tk.Frame(self.root)
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

        # ----- Style Treeview -----
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="black", foreground="#FF8C00",
                        fieldbackground="black", font=("Arial", 12))
        style.map("Treeview", background=[("selected", "#FF8C00")], foreground=[("selected", "black")])

        # ----- Footer -----
        footer = tk.Frame(self.root, bg="#D3D3D3", height=30)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text=f"Version 1.0 | {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}",
                 bg="#D3D3D3").pack()

        # Charger données initiales
        self.update_dashboard()

        # Refresh automatique toutes les 10 secondes
        self.root.after(10000, self.update_dashboard)

        self.root.mainloop()

    def update_dashboard(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Total passagers aujourd'hui
            today = datetime.date.today()
            cursor.execute("""
                SELECT SUM(nombre_ascendant), SUM(nombre_descendant)
                FROM comptage
                WHERE DATE(date_comptage)=%s
            """, (today,))
            result = cursor.fetchone()
            asc_total = result[0] if result[0] else 0
            desc_total = result[1] if result[1] else 0
            self.total_label.config(text=f"Asc: {asc_total}  | Desc: {desc_total}")

            # Tableau par ligne et station
            for row in self.tree.get_children():
                self.tree.delete(row)

            cursor.execute("""
                SELECT l.libelle_ligne, s.libelle_station,
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