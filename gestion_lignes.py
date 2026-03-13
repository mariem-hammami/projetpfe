import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

class GestionLignes:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Lignes")
        self.root.geometry("600x450")

        # ----- Treeview pour afficher les lignes -----
        self.tree = ttk.Treeview(self.root, columns=("id", "libelle", "id_agence"), show="headings")
        self.tree.heading("id", text="ID Ligne")
        self.tree.heading("libelle", text="Libellé Ligne")
        self.tree.heading("id_agence", text="ID Agence")

        self.tree.column("id", width=80)
        self.tree.column("libelle", width=250)
        self.tree.column("id_agence", width=100)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # ----- Boutons -----
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Ajouter Ligne", command=self.ajouter_ligne).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Modifier Ligne", command=self.modifier_ligne).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Supprimer Ligne", command=self.supprimer_ligne).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Rafraîchir", command=self.load_lignes).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Retour", command=self.retour).pack(side="left", padx=5)

        self.load_lignes()
        self.root.mainloop()

    def load_lignes(self):
        # Charger les lignes depuis la DB
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id_ligne, libelle_ligne, id_agence FROM ligne")
            rows = cursor.fetchall()
            for r in rows:
                self.tree.insert("", "end", values=r)
            conn.close()
        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    def ajouter_ligne(self):
        # ---- Fenêtre d'ajout persistant ----
        add_win = tk.Toplevel(self.root)
        add_win.title("Ajouter Ligne")
        add_win.geometry("300x250")

        tk.Label(add_win, text="ID Ligne:").pack(pady=5)
        id_entry = tk.Entry(add_win)
        id_entry.pack(pady=5)

        tk.Label(add_win, text="Libellé ligne:").pack(pady=5)
        libelle_entry = tk.Entry(add_win)
        libelle_entry.pack(pady=5)

        tk.Label(add_win, text="ID Agence:").pack(pady=5)
        id_agence_entry = tk.Entry(add_win)
        id_agence_entry.pack(pady=5)

        def enregistrer():
            id_ligne = id_entry.get().strip()
            libelle = libelle_entry.get().strip()
            id_agence = id_agence_entry.get().strip()

            if not libelle or not id_agence.isdigit():
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs correctement")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()

                if id_ligne.isdigit():  # ID fourni manuellement
                    cursor.execute(
                        "INSERT INTO ligne (id_ligne, libelle_ligne, id_agence) VALUES (%s,%s,%s)",
                        (int(id_ligne), libelle, int(id_agence))
                    )
                else:  # Auto-increment
                    cursor.execute(
                        "INSERT INTO ligne (libelle_ligne, id_agence) VALUES (%s,%s)",
                        (libelle, int(id_agence))
                    )

                conn.commit()
                conn.close()

                messagebox.showinfo("Succès", "Ligne ajoutée !")
                self.load_lignes()

                # Reset des champs pour ajouter une nouvelle ligne
                id_entry.delete(0, tk.END)
                libelle_entry.delete(0, tk.END)
                id_agence_entry.delete(0, tk.END)
                id_entry.focus()

            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(add_win, text="Ajouter", command=enregistrer).pack(pady=10)

    def modifier_ligne(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une ligne")
            return

        item = self.tree.item(selected[0])
        old_id = item["values"][0]

        # ---- Fenêtre de modification ----
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Modifier Ligne")
        edit_win.geometry("300x250")

        tk.Label(edit_win, text="ID Ligne:").pack(pady=5)
        id_entry = tk.Entry(edit_win)
        id_entry.insert(0, old_id)
        id_entry.pack(pady=5)

        tk.Label(edit_win, text="Libellé de la ligne:").pack(pady=5)
        libelle_entry = tk.Entry(edit_win)
        libelle_entry.insert(0, item["values"][1])
        libelle_entry.pack(pady=5)

        tk.Label(edit_win, text="ID Agence:").pack(pady=5)
        id_agence_entry = tk.Entry(edit_win)
        id_agence_entry.insert(0, item["values"][2])
        id_agence_entry.pack(pady=5)

        def enregistrer_modif():
            new_id = id_entry.get().strip()
            new_libelle = libelle_entry.get().strip()
            new_id_agence = id_agence_entry.get().strip()

            if not new_id.isdigit() or not new_libelle or not new_id_agence.isdigit():
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs correctement")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE ligne SET id_ligne=%s, libelle_ligne=%s, id_agence=%s WHERE id_ligne=%s",
                    (int(new_id), new_libelle, int(new_id_agence), old_id)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Ligne modifiée !")
                self.load_lignes()
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(edit_win, text="Enregistrer", command=enregistrer_modif).pack(pady=10)

    def supprimer_ligne(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une ligne")
            return

        item = self.tree.item(selected[0])
        id_ligne = item["values"][0]

        confirm = messagebox.askyesno(
            "Supprimer Ligne",
            f"Voulez-vous vraiment supprimer la ligne {item['values'][1]} ?"
        )
        if confirm:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM ligne WHERE id_ligne=%s",
                    (id_ligne,)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Ligne supprimée !")
                self.load_lignes()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    def retour(self):
        self.root.destroy()
