import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

class GestionVoyages:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Voyages")
        self.root.geometry("700x400")

        # ----- Tableau des voyages -----
        self.tree = ttk.Treeview(
            self.root,
            columns=("id_voyage", "id_trajet", "matricule", "date", "heure"),
            show="headings"
        )

        self.tree.heading("id_voyage", text="ID Voyage")
        self.tree.heading("id_trajet", text="ID Trajet")
        self.tree.heading("matricule", text="Matricule Bus")
        self.tree.heading("date", text="Date Voyage")
        self.tree.heading("heure", text="Heure")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # ----- Boutons -----
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Ajouter Voyage", command=self.ajouter_voyage).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Modifier Voyage", command=self.modifier_voyage).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Supprimer Voyage", command=self.supprimer_voyage).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Rafraîchir", command=self.load_voyages).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Retour", command=self.retour).pack(side="left", padx=5)

        self.load_voyages()
        self.root.mainloop()

    # ----- Charger les voyages -----
    def load_voyages(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id_voyage, id_trajet, matricule_vehicule, date_voyage, heure FROM voyage")
            rows = cursor.fetchall()

            for r in rows:
                self.tree.insert("", "end", values=r)

            conn.close()

        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    # ----- Ajouter voyage -----
    def ajouter_voyage(self):
        window = tk.Toplevel(self.root)
        window.title("Ajouter Voyage")
        window.geometry("300x300")

        tk.Label(window, text="ID Trajet").pack(pady=5)
        id_trajet_entry = tk.Entry(window)
        id_trajet_entry.pack(pady=5)

        tk.Label(window, text="Matricule Bus").pack(pady=5)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT matricule_vehicule FROM vehicule")
            bus_list = [row[0] for row in cursor.fetchall()]
            conn.close()
        except:
            bus_list = []

        matricule_combo = ttk.Combobox(window, values=bus_list, state="readonly")
        matricule_combo.pack(pady=5)

        tk.Label(window, text="Date Voyage (YYYY-MM-DD)").pack(pady=5)
        date_entry = tk.Entry(window)
        date_entry.pack(pady=5)

        tk.Label(window, text="Heure (HH:MM)").pack(pady=5)
        heure_entry = tk.Entry(window)
        heure_entry.pack(pady=5)

        def save():
            id_trajet = id_trajet_entry.get()
            matricule = matricule_combo.get()
            date_voyage = date_entry.get()
            heure = heure_entry.get()

            if id_trajet and matricule and date_voyage and heure:
                try:
                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute(
                        """INSERT INTO voyage
                           (id_trajet, matricule_vehicule, date_voyage, heure)
                           VALUES (%s,%s,%s,%s)""",
                        (id_trajet, matricule, date_voyage, heure)
                    )
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Succès", "Voyage ajouté")
                    window.destroy()
                    self.load_voyages()

                except Exception as e:
                    messagebox.showerror("Erreur DB", str(e))
            else:
                messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")

        tk.Button(window, text="Enregistrer", command=save).pack(pady=15)

    # ----- Modifier voyage -----
    def modifier_voyage(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un voyage")
            return

        item = self.tree.item(selected[0])
        id_voyage = item["values"][0]

        window = tk.Toplevel(self.root)
        window.title("Modifier Voyage")
        window.geometry("300x300")

        tk.Label(window, text="ID Trajet").pack(pady=5)
        id_trajet_entry = tk.Entry(window)
        id_trajet_entry.insert(0, item["values"][1])
        id_trajet_entry.pack(pady=5)

        tk.Label(window, text="Matricule Bus").pack(pady=5)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT matricule_vehicule FROM vehicule")
            bus_list = [row[0] for row in cursor.fetchall()]
            conn.close()
        except:
            bus_list = []

        matricule_combo = ttk.Combobox(window, values=bus_list, state="readonly")
        matricule_combo.set(item["values"][2])
        matricule_combo.pack(pady=5)

        tk.Label(window, text="Date Voyage (YYYY-MM-DD)").pack(pady=5)
        date_entry = tk.Entry(window)
        date_entry.insert(0, item["values"][3])
        date_entry.pack(pady=5)

        tk.Label(window, text="Heure (HH:MM)").pack(pady=5)
        heure_entry = tk.Entry(window)
        heure_entry.insert(0, item["values"][4])
        heure_entry.pack(pady=5)

        def save_changes():
            id_trajet = id_trajet_entry.get()
            matricule = matricule_combo.get()
            date_voyage = date_entry.get()
            heure = heure_entry.get()

            if id_trajet and matricule and date_voyage and heure:
                try:
                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute(
                        """UPDATE voyage
                           SET id_trajet=%s, matricule_vehicule=%s, date_voyage=%s, heure=%s
                           WHERE id_voyage=%s""",
                        (id_trajet, matricule, date_voyage, heure, id_voyage)
                    )
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Succès", "Voyage modifié")
                    window.destroy()
                    self.load_voyages()
                except Exception as e:
                    messagebox.showerror("Erreur DB", str(e))
            else:
                messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")

        tk.Button(window, text="Enregistrer", command=save_changes).pack(pady=15)

    # ----- Supprimer voyage -----
    def supprimer_voyage(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un voyage")
            return

        item = self.tree.item(selected[0])
        id_voyage = item["values"][0]

        confirm = messagebox.askyesno("Supprimer Voyage", f"Voulez-vous supprimer le voyage {id_voyage} ?")
        if confirm:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM voyage WHERE id_voyage=%s", (id_voyage,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Voyage supprimé")
                self.load_voyages()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    # ----- Retour -----
    def retour(self):
        self.root.destroy()