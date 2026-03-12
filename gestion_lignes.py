import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import connect_db

class GestionLignes:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Lignes")
        self.root.geometry("600x400")

        # ----- Treeview pour afficher les lignes -----
        self.tree = ttk.Treeview(self.root, columns=("id", "libelle", "id_agence"), show="headings")
        self.tree.heading("id", text="ID Ligne")
        self.tree.heading("libelle", text="Libellé Ligne")
        self.tree.heading("id_agence", text="ID Agence")

        self.tree.column("id", width=80)
        self.tree.column("libelle", width=300)
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
        libelle = simpledialog.askstring("Ajouter Ligne", "Libellé de la ligne:")
        id_agence = simpledialog.askinteger("Ajouter Ligne", "ID Agence:")

        if libelle and id_agence is not None:
            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO ligne (libelle_ligne, id_agence) VALUES (%s,%s)",
                    (libelle, id_agence)
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Succès", "Ligne ajoutée !")
                self.load_lignes()

            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    def modifier_ligne(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une ligne")
            return

        item = self.tree.item(selected[0])
        id_ligne = item["values"][0]

        new_libelle = simpledialog.askstring(
            "Modifier Ligne",
            "Nouveau libellé de la ligne:",
            initialvalue=item["values"][1]
        )

        new_id_agence = simpledialog.askinteger(
            "Modifier Ligne",
            "Nouvel ID Agence:",
            initialvalue=item["values"][2]
        )

        if new_libelle and new_id_agence is not None:
            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute(
                    "UPDATE ligne SET libelle_ligne=%s, id_agence=%s WHERE id_ligne=%s",
                    (new_libelle, new_id_agence, id_ligne)
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Succès", "Ligne modifiée !")
                self.load_lignes()

            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

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
        # Fermer la fenêtre et retourner à la page précédente
        self.root.destroy()