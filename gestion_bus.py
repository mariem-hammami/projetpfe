import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import connect_db

class GestionBus:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Bus")
        self.root.geometry("700x400")

        # ----- Treeview pour afficher les bus -----
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
        self.root.mainloop()

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

    def ajouter_bus(self):
        matricule = simpledialog.askstring("Ajouter Bus", "Matricule:")
        type_bus = simpledialog.askstring("Ajouter Bus", "Type de véhicule:")
        modele = simpledialog.askstring("Ajouter Bus", "Modèle:")
        etat = simpledialog.askstring("Ajouter Bus", "Etat (fonctionnel/panne):", initialvalue="fonctionnel")

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
                self.load_bus()

            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    def modifier_bus(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un bus")
            return

        item = self.tree.item(selected[0])
        matricule = item["values"][0]

        new_type = simpledialog.askstring("Modifier Bus", "Type:", initialvalue=item["values"][1])
        new_modele = simpledialog.askstring("Modifier Bus", "Modèle:", initialvalue=item["values"][2])
        new_etat = simpledialog.askstring("Modifier Bus", "Etat (fonctionnel/panne):", initialvalue=item["values"][3])

        if new_type and new_modele and new_etat:
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
                self.load_bus()

            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    def supprimer_bus(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un bus")
            return

        item = self.tree.item(selected[0])
        matricule = item["values"][0]

        confirm = messagebox.askyesno("Supprimer Bus", f"Voulez-vous vraiment supprimer le bus {matricule} ?")

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

    def retour(self):
        # Fermer la fenêtre et retourner à la page précédente
        self.root.destroy()