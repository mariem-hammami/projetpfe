import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

class GestionVoyages:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Voyages")
        self.root.geometry("750x500")

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
        add_win = tk.Toplevel(self.root)
        add_win.title("Ajouter Voyage")
        add_win.geometry("350x400")

        # ID Trajet
        tk.Label(add_win, text="ID Trajet:").pack(pady=5)
        id_trajet_entry = tk.Entry(add_win)
        id_trajet_entry.pack(pady=5)

        # Matricule Bus
        tk.Label(add_win, text="Matricule Bus:").pack(pady=5)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT matricule_vehicule FROM vehicule")
            bus_list = [row[0] for row in cursor.fetchall()]
            conn.close()
        except:
            bus_list = []

        matricule_combo = ttk.Combobox(add_win, values=bus_list, state="readonly")
        matricule_combo.pack(pady=5)

        # Date voyage
        tk.Label(add_win, text="Date Voyage:").pack(pady=5)
        date_frame = tk.Frame(add_win)
        date_frame.pack(pady=2)
        year_combo = ttk.Combobox(date_frame, values=[str(y) for y in range(2024, 2031)], width=5)
        year_combo.pack(side="left", padx=2)
        month_combo = ttk.Combobox(date_frame, values=[f"{m:02}" for m in range(1, 13)], width=3)
        month_combo.pack(side="left", padx=2)
        day_combo = ttk.Combobox(date_frame, values=[f"{d:02}" for d in range(1, 32)], width=3)
        day_combo.pack(side="left", padx=2)

        # Heure voyage
        tk.Label(add_win, text="Heure:").pack(pady=5)
        time_frame = tk.Frame(add_win)
        time_frame.pack(pady=2)
        hour_combo = ttk.Combobox(time_frame, values=[f"{h:02}" for h in range(0, 24)], width=3)
        hour_combo.pack(side="left", padx=2)
        minute_combo = ttk.Combobox(time_frame, values=[f"{m:02}" for m in range(0, 60, 5)], width=3)
        minute_combo.pack(side="left", padx=2)

        # Bouton enregistrer
        def save():
            id_trajet = id_trajet_entry.get().strip()
            matricule = matricule_combo.get().strip()
            date_voyage = f"{year_combo.get()}-{month_combo.get()}-{day_combo.get()}"
            heure = f"{hour_combo.get()}:{minute_combo.get()}"

            if not id_trajet or not matricule or not all([year_combo.get(), month_combo.get(), day_combo.get()]) or not all([hour_combo.get(), minute_combo.get()]):
                messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO voyage (id_trajet, matricule_vehicule, date_voyage, heure) VALUES (%s,%s,%s,%s)",
                    (id_trajet, matricule, date_voyage, heure)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Voyage ajouté")
                self.load_voyages()

                # Reset des champs
                id_trajet_entry.delete(0, tk.END)
                matricule_combo.set("")
                year_combo.set("")
                month_combo.set("")
                day_combo.set("")
                hour_combo.set("")
                minute_combo.set("")
                id_trajet_entry.focus()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(add_win, text="Ajouter", command=save).pack(pady=15)

    # ----- Modifier voyage -----
    def modifier_voyage(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un voyage")
            return

        item = self.tree.item(selected[0])
        id_voyage = item["values"][0]

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Modifier Voyage")
        edit_win.geometry("350x400")

        tk.Label(edit_win, text="ID Trajet:").pack(pady=5)
        id_trajet_entry = tk.Entry(edit_win)
        id_trajet_entry.insert(0, item["values"][1])
        id_trajet_entry.pack(pady=5)

        tk.Label(edit_win, text="Matricule Bus:").pack(pady=5)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT matricule_vehicule FROM vehicule")
            bus_list = [row[0] for row in cursor.fetchall()]
            conn.close()
        except:
            bus_list = []
        matricule_combo = ttk.Combobox(edit_win, values=bus_list, state="readonly")
        matricule_combo.set(item["values"][2])
        matricule_combo.pack(pady=5)

        # Date
        tk.Label(edit_win, text="Date Voyage:").pack(pady=5)
        date_frame = tk.Frame(edit_win)
        date_frame.pack(pady=2)
        y, m, d = item["values"][3].split("-")
        year_combo = ttk.Combobox(date_frame, values=[str(yr) for yr in range(2024, 2031)], width=5)
        year_combo.set(y)
        year_combo.pack(side="left", padx=2)
        month_combo = ttk.Combobox(date_frame, values=[f"{mon:02}" for mon in range(1, 13)], width=3)
        month_combo.set(m)
        month_combo.pack(side="left", padx=2)
        day_combo = ttk.Combobox(date_frame, values=[f"{da:02}" for da in range(1, 32)], width=3)
        day_combo.set(d)
        day_combo.pack(side="left", padx=2)

        # Heure
        tk.Label(edit_win, text="Heure:").pack(pady=5)
        time_frame = tk.Frame(edit_win)
        time_frame.pack(pady=2)
        h, mn = item["values"][4].split(":")
        hour_combo = ttk.Combobox(time_frame, values=[f"{hr:02}" for hr in range(0, 24)], width=3)
        hour_combo.set(h)
        hour_combo.pack(side="left", padx=2)
        minute_combo = ttk.Combobox(time_frame, values=[f"{mi:02}" for mi in range(0, 60, 5)], width=3)
        minute_combo.set(mn)
        minute_combo.pack(side="left", padx=2)

        def save_changes():
            id_trajet = id_trajet_entry.get().strip()
            matricule = matricule_combo.get().strip()
            date_voyage = f"{year_combo.get()}-{month_combo.get()}-{day_combo.get()}"
            heure = f"{hour_combo.get()}:{minute_combo.get()}"

            if not id_trajet or not matricule or not all([year_combo.get(), month_combo.get(), day_combo.get()]) or not all([hour_combo.get(), minute_combo.get()]):
                messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE voyage SET id_trajet=%s, matricule_vehicule=%s, date_voyage=%s, heure=%s WHERE id_voyage=%s",
                    (id_trajet, matricule, date_voyage, heure, id_voyage)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Voyage modifié")
                self.load_voyages()
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(edit_win, text="Enregistrer", command=save_changes).pack(pady=15)

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
