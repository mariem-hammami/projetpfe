import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db
import datetime

class DashboardUser:
    def __init__(self, username):
        self.root = tk.Toplevel()   # IMPORTANT (pas Tk)
        self.root.title(f"Dashboard Utilisateur - {username}")
        self.root.geometry("850x500")

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
        tk.Label(self.total_frame, text="Total Passagers Aujourd'hui", font=("Arial", 14, "bold"),
         bg="black", fg="#FF8C00").pack()
        self.total_label = tk.Label(self.total_frame, text="Asc: 0  | Desc: 0", font=("Arial", 12,),
                            bg="black", fg="#FF8C00")
        self.total_label.pack()

        # ----- Tableau Passagers par Station -----
        self.table_frame = tk.Frame(self.root)
        self.table_frame.place(x=10, y=180, width=830, height=250)
        self.tree = ttk.Treeview(self.table_frame, columns=("station", "asc", "desc"), show="headings")
        self.tree.heading("station", text="Station")
        self.tree.heading("asc", text="Ascendant")
        self.tree.heading("desc", text="Descendant")
        self.tree.column("station", width=400)
        self.tree.column("asc", width=100)
        self.tree.column("desc", width=100)
        self.tree.pack(fill="both", expand=True)
        # ----- Style du Treeview (couleurs orange/noir) -----
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="black", foreground="#FF8C00", fieldbackground="black",
                font=("Arial", 12))
        style.map("Treeview", background=[("selected", "#FF8C00")], foreground=[("selected", "black")])

        
        # ----- Footer -----
        footer = tk.Frame(self.root, bg="#D3D3D3", height=30)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text=f"Version 1.0 | {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", bg="#D3D3D3").pack()

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
            asc = result[0] if result[0] else 0
            desc = result[1] if result[1] else 0
            self.total_label.config(text=f"Asc: {asc}  | Desc: {desc}")

            # Tableau passagers par station
            for row in self.tree.get_children():
                self.tree.delete(row)
            cursor.execute("""
                SELECT s.libelle_station, SUM(c.nombre_ascendant), SUM(c.nombre_descendant)
                FROM comptage c
                JOIN station s ON c.id_station=s.id_station
                WHERE DATE(c.date_comptage)=%s
                GROUP BY c.id_station
            """, (today,))
            rows = cursor.fetchall()
            for r in rows:
                self.tree.insert("", "end", values=r)

            conn.close()
        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    