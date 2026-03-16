import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db


class GestionStations:

    def __init__(self):

        self.root = tk.Toplevel()
        self.root.title("Gestion des Stations")
        self.root.geometry("900x520")
        self.root.configure(bg="#f4f6f9")

        # ---------- STYLE ----------
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        font=("Segoe UI", 11),
                        rowheight=28)

        style.configure("Treeview.Heading",
                        font=("Segoe UI", 12, "bold"),
                        background="#34495e",
                        foreground="white")

        # ---------- TITRE ----------
        title = tk.Label(self.root,
                         text="Gestion des Stations",
                         font=("Segoe UI", 20, "bold"),
                         bg="#f4f6f9",
                         fg="#2c3e50")
        title.pack(pady=15)

        # ---------- TABLE FRAME ----------
        table_frame = tk.Frame(self.root, bg="#f4f6f9")
        table_frame.pack(fill="both", expand=True, padx=20)

        scroll_y = tk.Scrollbar(table_frame)
        scroll_y.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "libelle", "latitude", "longitude", "ligne", "ordre"),
            show="headings",
            yscrollcommand=scroll_y.set
        )

        scroll_y.config(command=self.tree.yview)

        self.tree.heading("id", text="ID Station")
        self.tree.heading("libelle", text="Libellé")
        self.tree.heading("latitude", text="Latitude")
        self.tree.heading("longitude", text="Longitude")
        self.tree.heading("ligne", text="Ligne")
        self.tree.heading("ordre", text="Ordre")

        self.tree.column("id", width=100, anchor="w")
        self.tree.column("libelle", width=250, anchor="w")
        self.tree.column("latitude", width=120, anchor="w")
        self.tree.column("longitude", width=120, anchor="w")
        self.tree.column("ligne", width=200, anchor="w")
        self.tree.column("ordre", width=80, anchor="w")

        self.tree.pack(fill="both", expand=True)

        # ---------- BOUTONS ----------
        btn_frame = tk.Frame(self.root, bg="#f4f6f9")
        btn_frame.pack(pady=15)

        btn_style = {
            "font": ("Segoe UI", 11, "bold"),
            "width": 14,
            "bd": 0,
            "cursor": "hand2"
        }

        tk.Button(btn_frame, text="Ajouter", bg="#2ecc71", fg="white",
                  command=self.ajouter_station, **btn_style).grid(row=0, column=0, padx=6)

        tk.Button(btn_frame, text="Modifier", bg="#3498db", fg="white",
                  command=self.modifier_station, **btn_style).grid(row=0, column=1, padx=6)

        tk.Button(btn_frame, text="Supprimer", bg="#e74c3c", fg="white",
                  command=self.supprimer_station, **btn_style).grid(row=0, column=2, padx=6)

        tk.Button(btn_frame, text="Rafraîchir", bg="#f39c12", fg="white",
                  command=self.load_stations, **btn_style).grid(row=0, column=3, padx=6)

        tk.Button(btn_frame, text="Retour", bg="#7f8c8d", fg="white",
                  command=self.retour, **btn_style).grid(row=0, column=4, padx=6)

        self.load_stations()

    # ---------- LOAD ----------
    def load_stations(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT s.id_station, s.libelle_station, s.latitude, s.longitude,
                       l.libelle_ligne, ls.ordre
                FROM station s
                LEFT JOIN ligne_station ls ON s.id_station = ls.id_station
                LEFT JOIN ligne l ON ls.id_ligne = l.id_ligne
                ORDER BY l.libelle_ligne, ls.ordre
            """)

            rows = cursor.fetchall()

            for r in rows:
                self.tree.insert("", "end", values=r)

            conn.close()

        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    # ---------- AJOUT ----------
    def ajouter_station(self):

        add_win = tk.Toplevel(self.root)
        add_win.title("Ajouter Station")
        add_win.geometry("350x400")

        tk.Label(add_win, text="ID Station (laisser vide si auto)").pack(pady=5)
        id_entry = tk.Entry(add_win)
        id_entry.pack()

        tk.Label(add_win, text="Libellé").pack(pady=5)
        libelle_entry = tk.Entry(add_win)
        libelle_entry.pack()

        tk.Label(add_win, text="Latitude").pack(pady=5)
        lat_entry = tk.Entry(add_win)
        lat_entry.pack()

        tk.Label(add_win, text="Longitude").pack(pady=5)
        long_entry = tk.Entry(add_win)
        long_entry.pack()

        tk.Label(add_win, text="ID Ligne").pack(pady=5)
        ligne_entry = tk.Entry(add_win)
        ligne_entry.pack()

        tk.Label(add_win, text="Ordre").pack(pady=5)
        ordre_entry = tk.Entry(add_win)
        ordre_entry.pack()

        def enregistrer():

            id_station = id_entry.get().strip()
            libelle = libelle_entry.get().strip()
            lat = lat_entry.get().strip()
            long = long_entry.get().strip()
            id_ligne = ligne_entry.get().strip()
            ordre = ordre_entry.get().strip()

            if not libelle or not lat or not long or not id_ligne.isdigit():
                messagebox.showwarning("Erreur", "Champs invalides")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()

                if id_station.isdigit():
                    cursor.execute(
                        "INSERT INTO station VALUES (%s,%s,%s,%s)",
                        (int(id_station), libelle, float(lat), float(long))
                    )
                else:
                    cursor.execute(
                        "INSERT INTO station (libelle_station, latitude, longitude) VALUES (%s,%s,%s)",
                        (libelle, float(lat), float(long))
                    )
                    id_station = cursor.lastrowid

                if ordre.isdigit():
                    ordre_val = int(ordre)
                else:
                    cursor.execute(
                        "SELECT MAX(ordre) FROM ligne_station WHERE id_ligne=%s",
                        (int(id_ligne),)
                    )
                    max_order = cursor.fetchone()[0] or 0
                    ordre_val = max_order + 1

                cursor.execute(
                    "INSERT INTO ligne_station VALUES (%s,%s,%s)",
                    (int(id_ligne), int(id_station), ordre_val)
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Succès", "Station ajoutée")
                self.load_stations()
                add_win.destroy()

            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(add_win, text="Ajouter", command=enregistrer).pack(pady=10)

    # ---------- MODIFIER ----------
    def modifier_station(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez une station")
            return

        item = self.tree.item(selected[0])
        old_id = item["values"][0]

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Modifier Station")
        edit_win.geometry("350x300")

        tk.Label(edit_win, text="Libellé").pack(pady=5)
        libelle_entry = tk.Entry(edit_win)
        libelle_entry.insert(0, item["values"][1])
        libelle_entry.pack()

        tk.Label(edit_win, text="Latitude").pack(pady=5)
        lat_entry = tk.Entry(edit_win)
        lat_entry.insert(0, item["values"][2])
        lat_entry.pack()

        tk.Label(edit_win, text="Longitude").pack(pady=5)
        long_entry = tk.Entry(edit_win)
        long_entry.insert(0, item["values"][3])
        long_entry.pack()

        def enregistrer():

            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE station
                    SET libelle_station=%s, latitude=%s, longitude=%s
                    WHERE id_station=%s
                """, (
                    libelle_entry.get(),
                    float(lat_entry.get()),
                    float(long_entry.get()),
                    old_id
                ))

                conn.commit()
                conn.close()

                messagebox.showinfo("Succès", "Station modifiée")
                self.load_stations()
                edit_win.destroy()

            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(edit_win, text="Enregistrer", command=enregistrer).pack(pady=10)

    # ---------- SUPPRIMER ----------
    def supprimer_station(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez une station")
            return

        item = self.tree.item(selected[0])
        id_station = item["values"][0]

        confirm = messagebox.askyesno(
            "Supprimer",
            f"Supprimer station {item['values'][1]} ?"
        )

        if confirm:
            try:

                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute(
                    "DELETE FROM ligne_station WHERE id_station=%s",
                    (id_station,)
                )

                cursor.execute(
                    "DELETE FROM station WHERE id_station=%s",
                    (id_station,)
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Succès", "Station supprimée")
                self.load_stations()

            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    # ---------- RETOUR ----------
    def retour(self):
        self.root.destroy()