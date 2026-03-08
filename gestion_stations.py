import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import connect_db

class GestionStations:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Stations")
        self.root.geometry("700x450")

        # Tableau des stations
        self.tree = ttk.Treeview(self.root, columns=("id", "libelle", "latitude", "longitude", "ligne", "ordre"), show="headings")
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
        libelle = simpledialog.askstring("Ajouter Station", "Libellé de la station:")
        latitude = simpledialog.askfloat("Ajouter Station", "Latitude:")
        longitude = simpledialog.askfloat("Ajouter Station", "Longitude:")
        if not (libelle and latitude is not None and longitude is not None):
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Choisir ligne
            cursor.execute("SELECT id_ligne, libelle_ligne FROM ligne")
            lignes = cursor.fetchall()
            if not lignes:
                messagebox.showwarning("Aucune Ligne", "Créez des lignes avant d'ajouter une station.")
                conn.close()
                return

            ligne_str = "\n".join([f"{l[0]} - {l[1]}" for l in lignes])
            id_ligne = simpledialog.askinteger("Choisir Ligne", f"ID de la ligne:\n{ligne_str}")
            if not id_ligne:
                conn.close()
                return

            # Ajouter station
            cursor.execute("INSERT INTO station (libelle_station, latitude, longitude) VALUES (%s,%s,%s)", 
                           (libelle, latitude, longitude))
            id_station = cursor.lastrowid

            # Calculer ordre
            cursor.execute("SELECT MAX(ordre) FROM ligne_station WHERE id_ligne=%s", (id_ligne,))
            max_order = cursor.fetchone()[0] or 0
            ordre = max_order + 1

            # Lier station à ligne
            cursor.execute("INSERT INTO ligne_station (id_ligne, id_station, ordre) VALUES (%s,%s,%s)", 
                           (id_ligne, id_station, ordre))

            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Station ajoutée !")
            self.load_stations()
        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    def modifier_station(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une station")
            return
        item = self.tree.item(selected[0])
        id_station = item["values"][0]

        new_libelle = simpledialog.askstring("Modifier Station", "Libellé:", initialvalue=item["values"][1])
        new_lat = simpledialog.askfloat("Modifier Station", "Latitude:", initialvalue=item["values"][2])
        new_long = simpledialog.askfloat("Modifier Station", "Longitude:", initialvalue=item["values"][3])

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id_ligne, libelle_ligne FROM ligne")
            lignes = cursor.fetchall()
            ligne_str = "\n".join([f"{l[0]} - {l[1]}" for l in lignes])
            new_id_ligne = simpledialog.askinteger("Modifier Ligne", f"ID de la ligne:\n{ligne_str}", initialvalue=item["values"][4])

            if not (new_libelle and new_lat is not None and new_long is not None and new_id_ligne):
                conn.close()
                return

            # Update station
            cursor.execute("UPDATE station SET libelle_station=%s, latitude=%s, longitude=%s WHERE id_station=%s",
                           (new_libelle, new_lat, new_long, id_station))

            # Update ligne_station
            cursor.execute("UPDATE ligne_station SET id_ligne=%s WHERE id_station=%s", (new_id_ligne, id_station))

            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Station modifiée !")
            self.load_stations()
        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    def supprimer_station(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une station")
            return
        item = self.tree.item(selected[0])
        id_station = item["values"][0]

        confirm = messagebox.askyesno("Supprimer Station", f"Voulez-vous supprimer la station {item['values'][1]} ?")
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