import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

class GestionStations:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Stations")
        self.root.geometry("750x500")

        # Tableau des stations
        self.tree = ttk.Treeview(
            self.root,
            columns=("id", "libelle", "latitude", "longitude", "ligne", "ordre"),
            show="headings"
        )
        self.tree.heading("id", text="ID Station")
        self.tree.heading("libelle", text="Libellé")
        self.tree.heading("latitude", text="Latitude")
        self.tree.heading("longitude", text="Longitude")
        self.tree.heading("ligne", text="Ligne")
        self.tree.heading("ordre", text="Ordre")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Boutons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Ajouter Station", command=self.ajouter_station).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Modifier Station", command=self.modifier_station).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Supprimer Station", command=self.supprimer_station).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Rafraîchir", command=self.load_stations).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Retour", command=self.retour).pack(side="left", padx=5)

        self.load_stations()
        self.root.mainloop()

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
            for r in cursor.fetchall():
                self.tree.insert("", "end", values=r)
            conn.close()
        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    def ajouter_station(self):
        # Fenêtre persistante pour ajouter stations
        add_win = tk.Toplevel(self.root)
        add_win.title("Ajouter Station")
        add_win.geometry("350x400")

        tk.Label(add_win, text="ID Station (laisser vide si auto):").pack(pady=5)
        id_entry = tk.Entry(add_win)
        id_entry.pack(pady=5)

        tk.Label(add_win, text="Libellé de la station:").pack(pady=5)
        libelle_entry = tk.Entry(add_win)
        libelle_entry.pack(pady=5)

        tk.Label(add_win, text="Latitude:").pack(pady=5)
        lat_entry = tk.Entry(add_win)
        lat_entry.pack(pady=5)

        tk.Label(add_win, text="Longitude:").pack(pady=5)
        long_entry = tk.Entry(add_win)
        long_entry.pack(pady=5)

        tk.Label(add_win, text="ID Ligne:").pack(pady=5)
        ligne_entry = tk.Entry(add_win)
        ligne_entry.pack(pady=5)

        tk.Label(add_win, text="Ordre (laisser vide pour auto):").pack(pady=5)
        ordre_entry = tk.Entry(add_win)
        ordre_entry.pack(pady=5)

        def enregistrer():
            id_station = id_entry.get().strip()
            libelle = libelle_entry.get().strip()
            lat = lat_entry.get().strip()
            long = long_entry.get().strip()
            id_ligne = ligne_entry.get().strip()
            ordre = ordre_entry.get().strip()

            if not libelle or not lat or not long or not id_ligne.isdigit():
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs obligatoires correctement")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()

                # Insérer station
                if id_station.isdigit():
                    cursor.execute(
                        "INSERT INTO station (id_station, libelle_station, latitude, longitude) VALUES (%s,%s,%s,%s)",
                        (int(id_station), libelle, float(lat), float(long))
                    )
                else:
                    cursor.execute(
                        "INSERT INTO station (libelle_station, latitude, longitude) VALUES (%s,%s,%s)",
                        (libelle, float(lat), float(long))
                    )

                if not id_station.isdigit():
                    id_station = cursor.lastrowid

                # Déterminer ordre
                if ordre.isdigit():
                    ordre_val = int(ordre)
                else:
                    cursor.execute("SELECT MAX(ordre) FROM ligne_station WHERE id_ligne=%s", (int(id_ligne),))
                    max_order = cursor.fetchone()[0] or 0
                    ordre_val = max_order + 1

                # Lier station à la ligne
                cursor.execute(
                    "INSERT INTO ligne_station (id_ligne, id_station, ordre) VALUES (%s,%s,%s)",
                    (int(id_ligne), int(id_station), ordre_val)
                )

                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Station ajoutée !")
                self.load_stations()

                # Reset des champs pour ajouter une nouvelle station
                id_entry.delete(0, tk.END)
                libelle_entry.delete(0, tk.END)
                lat_entry.delete(0, tk.END)
                long_entry.delete(0, tk.END)
                ligne_entry.delete(0, tk.END)
                ordre_entry.delete(0, tk.END)
                id_entry.focus()

            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(add_win, text="Ajouter", command=enregistrer).pack(pady=10)

    def modifier_station(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une station")
            return

        item = self.tree.item(selected[0])
        old_id = item["values"][0]

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Modifier Station")
        edit_win.geometry("350x400")

        tk.Label(edit_win, text="ID Station:").pack(pady=5)
        id_entry = tk.Entry(edit_win)
        id_entry.insert(0, old_id)
        id_entry.pack(pady=5)

        tk.Label(edit_win, text="Libellé:").pack(pady=5)
        libelle_entry = tk.Entry(edit_win)
        libelle_entry.insert(0, item["values"][1])
        libelle_entry.pack(pady=5)

        tk.Label(edit_win, text="Latitude:").pack(pady=5)
        lat_entry = tk.Entry(edit_win)
        lat_entry.insert(0, item["values"][2])
        lat_entry.pack(pady=5)

        tk.Label(edit_win, text="Longitude:").pack(pady=5)
        long_entry = tk.Entry(edit_win)
        long_entry.insert(0, item["values"][3])
        long_entry.pack(pady=5)

        tk.Label(edit_win, text="ID Ligne:").pack(pady=5)
        ligne_entry = tk.Entry(edit_win)
        ligne_entry.insert(0, item["values"][4])
        ligne_entry.pack(pady=5)

        tk.Label(edit_win, text="Ordre:").pack(pady=5)
        ordre_entry = tk.Entry(edit_win)
        ordre_entry.insert(0, item["values"][5])
        ordre_entry.pack(pady=5)

        def enregistrer_modif():
            new_id = id_entry.get().strip()
            new_libelle = libelle_entry.get().strip()
            new_lat = lat_entry.get().strip()
            new_long = long_entry.get().strip()
            new_id_ligne = ligne_entry.get().strip()
            new_ordre = ordre_entry.get().strip()

            if not new_id.isdigit() or not new_libelle or not new_lat or not new_long or not new_id_ligne.isdigit():
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs obligatoires correctement")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE station SET id_station=%s, libelle_station=%s, latitude=%s, longitude=%s WHERE id_station=%s",
                    (int(new_id), new_libelle, float(new_lat), float(new_long), old_id)
                )
                cursor.execute(
                    "UPDATE ligne_station SET id_ligne=%s, ordre=%s WHERE id_station=%s",
                    (int(new_id_ligne), int(new_ordre) if new_ordre.isdigit() else 1, int(new_id))
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Station modifiée !")
                self.load_stations()
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(edit_win, text="Enregistrer", command=enregistrer_modif).pack(pady=10)

    def supprimer_station(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une station")
            return

        item = self.tree.item(selected[0])
        id_station = item["values"][0]

        confirm = messagebox.askyesno(
            "Supprimer Station",
            f"Voulez-vous supprimer la station {item['values'][1]} ?"
        )
        if confirm:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ligne_station WHERE id_station=%s", (id_station,))
                cursor.execute("DELETE FROM station WHERE id_station=%s", (id_station,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Station supprimée !")
                self.load_stations()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    def retour(self):
        self.root.destroy()
