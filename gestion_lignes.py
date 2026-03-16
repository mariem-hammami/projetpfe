import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

class GestionLignes:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Lignes")
        self.root.geometry("750x500")
        self.root.configure(bg="#f4f6f9")

        # ---------- STYLE ----------
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#34495e", foreground="white")

        # ---------- TITRE ----------
        title = tk.Label(self.root, text="Gestion des Lignes", font=("Segoe UI", 20, "bold"),
                         bg="#f4f6f9", fg="#2c3e50")
        title.pack(pady=15)

        # ---------- FRAME TABLE ----------
        table_frame = tk.Frame(self.root, bg="#f4f6f9")
        table_frame.pack(fill="both", expand=True, padx=20)

        scroll_y = tk.Scrollbar(table_frame)
        scroll_y.pack(side="right", fill="y")

        self.tree = ttk.Treeview(table_frame, columns=("id", "libelle", "id_agence"), show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree.yview)

        self.tree.heading("id", text="ID Ligne")
        self.tree.heading("libelle", text="Libellé Ligne")
        self.tree.heading("id_agence", text="ID Agence")

        self.tree.column("id", width=100, anchor="w")
        self.tree.column("libelle", width=350, anchor="w")
        self.tree.column("id_agence", width=150, anchor="w")
        self.tree.pack(fill="both", expand=True)

        # ---------- FRAME BOUTONS ----------
        btn_frame = tk.Frame(self.root, bg="#f4f6f9")
        btn_frame.pack(pady=15)

        btn_style = {"font": ("Segoe UI", 11, "bold"), "width": 14, "bd": 0, "cursor": "hand2"}

        tk.Button(btn_frame, text="Ajouter", bg="#2ecc71", fg="white", command=self.ajouter_ligne, **btn_style).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Modifier", bg="#3498db", fg="white", command=self.modifier_ligne, **btn_style).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Supprimer", bg="#e74c3c", fg="white", command=self.supprimer_ligne, **btn_style).grid(row=0, column=2, padx=6)
        tk.Button(btn_frame, text="Rafraîchir", bg="#f39c12", fg="white", command=self.load_lignes, **btn_style).grid(row=0, column=3, padx=6)
        tk.Button(btn_frame, text="Retour", bg="#7f8c8d", fg="white", command=self.retour, **btn_style).grid(row=0, column=4, padx=6)

        self.load_lignes()

    # ---------- LOAD ----------
    def load_lignes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id_ligne, libelle_ligne, id_agence FROM ligne")
            for r in cursor.fetchall():
                self.tree.insert("", "end", values=r)
            conn.close()
        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    # ---------- AJOUT ----------
    def ajouter_ligne(self):
        win = tk.Toplevel(self.root)
        win.title("Ajouter Ligne")
        win.geometry("350x250")

        tk.Label(win, text="Libellé Ligne:").pack(pady=5)
        libelle_entry = tk.Entry(win)
        libelle_entry.pack(pady=5)

        tk.Label(win, text="ID Agence:").pack(pady=5)
        id_agence_entry = tk.Entry(win)
        id_agence_entry.pack(pady=5)

        def save():
            libelle = libelle_entry.get().strip()
            id_agence = id_agence_entry.get().strip()

            if not libelle or not id_agence:
                messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO ligne (libelle_ligne, id_agence) VALUES (%s,%s)", (libelle, id_agence))
                conn.commit()
                new_id = cursor.lastrowid  # Récupère l'ID généré automatiquement
                conn.close()

                self.tree.insert("", "end", values=(new_id, libelle, id_agence))
                messagebox.showinfo("Succès", "Ligne ajoutée avec ID: {}".format(new_id))
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(win, text="Ajouter", bg="#2ecc71", fg="white", width=14, command=save).pack(pady=15)

    # ---------- MODIFIER ----------
    def modifier_ligne(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez une ligne")
            return

        item = self.tree.item(selected[0])
        ligne_id = item["values"][0]

        win = tk.Toplevel(self.root)
        win.title("Modifier Ligne")
        win.geometry("350x250")

        tk.Label(win, text="Libellé Ligne:").pack(pady=5)
        libelle_entry = tk.Entry(win)
        libelle_entry.insert(0, item["values"][1])
        libelle_entry.pack(pady=5)

        tk.Label(win, text="ID Agence:").pack(pady=5)
        id_agence_entry = tk.Entry(win)
        id_agence_entry.insert(0, item["values"][2])
        id_agence_entry.pack(pady=5)

        def save_changes():
            libelle = libelle_entry.get().strip()
            id_agence = id_agence_entry.get().strip()
            if not libelle or not id_agence:
                messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
                return
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE ligne SET libelle_ligne=%s, id_agence=%s WHERE id_ligne=%s", (libelle, id_agence, ligne_id))
                conn.commit()
                conn.close()
                self.load_lignes()
                messagebox.showinfo("Succès", "Ligne modifiée")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(win, text="Enregistrer", bg="#3498db", fg="white", width=14, command=save_changes).pack(pady=15)

    # ---------- SUPPRIMER ----------
    def supprimer_ligne(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez une ligne")
            return

        item = self.tree.item(selected[0])
        ligne_id = item["values"][0]

        confirm = messagebox.askyesno("Supprimer Ligne", f"Voulez-vous supprimer la ligne {ligne_id} ?")
        if confirm:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ligne WHERE id_ligne=%s", (ligne_id,))
                conn.commit()
                conn.close()
                self.load_lignes()
                messagebox.showinfo("Succès", "Ligne supprimée")
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    # ---------- RETOUR ----------
    def retour(self):
        self.root.destroy()