import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

class GestionBus:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Bus")
        self.root.geometry("700x400")

        # ----- Table pour afficher les bus -----
        self.tree = ttk.Treeview(
            self.root,
            columns=("matricule", "type", "modele", "etat"),
            show="headings"
        )
        self.tree.heading("matricule", text="Matricule")
        self.tree.heading("type", text="Type")
        self.tree.heading("modele", text="Modèle")
        self.tree.heading("etat", text="Etat")
        self.tree.column("matricule", width=120)
        self.tree.column("type", width=150)
        self.tree.column("modele", width=150)
        self.tree.column("etat", width=100)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # ----- Boutons -----
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Ajouter Bus", command=self.ajouter_bus).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Modifier Bus", command=self.modifier_bus).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Supprimer Bus", command=self.supprimer_bus).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Rafraîchir", command=self.load_bus).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Retour", command=self.retour).pack(side="left", padx=5)

        self.load_bus()

    # ----- Charger les bus -----
    def load_bus(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT matricule_vehicule, type_vehicule, modele_vehicule, etat FROM vehicule")
            rows = cursor.fetchall()
            for r in rows:
                self.tree.insert("", "end", values=r)
            conn.close()
        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    # ----- Ajouter Bus -----
    def ajouter_bus(self):
        win = tk.Toplevel(self.root)
        win.title("Ajouter Bus")
        win.geometry("300x300")

        tk.Label(win, text="Matricule").pack(pady=5)
        entry_matricule = tk.Entry(win)
        entry_matricule.pack()

        tk.Label(win, text="Type véhicule").pack(pady=5)
        entry_type = tk.Entry(win)
        entry_type.pack()

        tk.Label(win, text="Modèle").pack(pady=5)
        entry_modele = tk.Entry(win)
        entry_modele.pack()

        tk.Label(win, text="Etat").pack(pady=5)
        etat_var = tk.StringVar(value="fonctionnel")
        tk.Radiobutton(win, text="Fonctionnel", variable=etat_var, value="fonctionnel").pack()
        tk.Radiobutton(win, text="En panne", variable=etat_var, value="en panne").pack()

        def save_bus():
            matricule = entry_matricule.get()
            type_bus = entry_type.get()
            modele = entry_modele.get()
            etat = etat_var.get()

            if matricule and type_bus and modele and etat:
                try:
                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO vehicule (matricule_vehicule, type_vehicule, modele_vehicule, etat) VALUES (%s,%s,%s,%s)",
                        (matricule, type_bus, modele, etat)
                    )
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Succès", "Bus ajouté !")
                    win.destroy()
                    self.load_bus()
                except Exception as e:
                    messagebox.showerror("Erreur DB", str(e))
            else:
                messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")

        tk.Button(win, text="Enregistrer", command=save_bus).pack(pady=15)

    # ----- Modifier Bus -----
    def modifier_bus(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un bus")
            return

        item = self.tree.item(selected[0])
        matricule = item["values"][0]

        win = tk.Toplevel(self.root)
        win.title("Modifier Bus")
        win.geometry("300x300")

        tk.Label(win, text="Type véhicule").pack(pady=5)
        entry_type = tk.Entry(win)
        entry_type.insert(0, item["values"][1])
        entry_type.pack()

        tk.Label(win, text="Modèle").pack(pady=5)
        entry_modele = tk.Entry(win)
        entry_modele.insert(0, item["values"][2])
        entry_modele.pack()

        tk.Label(win, text="Etat").pack(pady=5)
        etat_var = tk.StringVar(value=item["values"][3])
        tk.Radiobutton(win, text="Fonctionnel", variable=etat_var, value="fonctionnel").pack()
        tk.Radiobutton(win, text="En panne", variable=etat_var, value="en panne").pack()

        def update_bus():
            new_type = entry_type.get()
            new_modele = entry_modele.get()
            new_etat = etat_var.get()
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE vehicule SET type_vehicule=%s, modele_vehicule=%s, etat=%s WHERE matricule_vehicule=%s",
                    (new_type, new_modele, new_etat, matricule)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Bus modifié !")
                win.destroy()
                self.load_bus()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(win, text="Enregistrer", command=update_bus).pack(pady=15)

    # ----- Supprimer Bus -----
    def supprimer_bus(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un bus")
            return

        item = self.tree.item(selected[0])
        matricule = item["values"][0]

        confirm = messagebox.askyesno("Supprimer Bus", f"Voulez-vous supprimer le bus {matricule} ?")
        if confirm:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM vehicule WHERE matricule_vehicule=%s", (matricule,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Bus supprimé !")
                self.load_bus()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    # ----- Retour -----
    def retour(self):
        self.root.destroy()
