import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

class GestionBus:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Bus")
        self.root.geometry("750x500")
        self.root.configure(bg="#f4f6f9")

        # ---------- STYLE ----------
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#34495e", foreground="white")

        # ---------- TITRE ----------
        title = tk.Label(self.root, text="Gestion des Bus", font=("Segoe UI", 20, "bold"), bg="#f4f6f9", fg="#2c3e50")
        title.pack(pady=15)

        # ---------- TABLE ----------
        table_frame = tk.Frame(self.root, bg="#f4f6f9")
        table_frame.pack(fill="both", expand=True, padx=20)
        scroll_y = tk.Scrollbar(table_frame)
        scroll_y.pack(side="right", fill="y")

        self.tree = ttk.Treeview(table_frame, columns=("matricule", "type", "modele", "etat"), show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree.yview)

        self.tree.heading("matricule", text="Matricule")
        self.tree.heading("type", text="Type")
        self.tree.heading("modele", text="Modèle")
        self.tree.heading("etat", text="État")

        self.tree.column("matricule", width=150, anchor="w")
        self.tree.column("type", width=200, anchor="w")
        self.tree.column("modele", width=200, anchor="w")
        self.tree.column("etat", width=120, anchor="w")
        self.tree.pack(fill="both", expand=True)

        # ---------- BOUTONS ----------
        btn_frame = tk.Frame(self.root, bg="#f4f6f9")
        btn_frame.pack(pady=15)
        btn_style = {"font": ("Segoe UI", 11, "bold"), "width": 14, "bd": 0, "cursor": "hand2"}

        tk.Button(btn_frame, text="Ajouter", bg="#2ecc71", fg="white", command=self.ajouter_bus, **btn_style).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Modifier", bg="#3498db", fg="white", command=self.modifier_bus, **btn_style).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Supprimer", bg="#e74c3c", fg="white", command=self.supprimer_bus, **btn_style).grid(row=0, column=2, padx=6)
        tk.Button(btn_frame, text="Rafraîchir", bg="#f39c12", fg="white", command=self.load_bus, **btn_style).grid(row=0, column=3, padx=6)
        tk.Button(btn_frame, text="Retour", bg="#7f8c8d", fg="white", command=self.retour, **btn_style).grid(row=0, column=4, padx=6)

        self.load_bus()

    # ---------- LOAD ----------
    def load_bus(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT matricule_vehicule, type_vehicule, modele_vehicule, etat FROM vehicule")
            for r in cursor.fetchall():
                self.tree.insert("", "end", values=r)
            conn.close()
        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    # ---------- AJOUT ----------
    def ajouter_bus(self):
        win = tk.Toplevel(self.root)
        win.title("Ajouter Bus")
        win.geometry("350x300")

        tk.Label(win, text="Matricule:").pack(pady=5)
        matricule_entry = tk.Entry(win)
        matricule_entry.pack(pady=5)

        tk.Label(win, text="Type:").pack(pady=5)
        type_entry = tk.Entry(win)
        type_entry.pack(pady=5)

        tk.Label(win, text="Modèle:").pack(pady=5)
        modele_entry = tk.Entry(win)
        modele_entry.pack(pady=5)

        tk.Label(win, text="État:").pack(pady=5)
        etat_combo = ttk.Combobox(win, values=["Fonctionnel", "En panne"], state="readonly")
        etat_combo.pack(pady=5)
        etat_combo.set("Fonctionnel")

        def save():
            matricule = matricule_entry.get().strip()
            type_v = type_entry.get().strip()
            modele = modele_entry.get().strip()
            etat = etat_combo.get().strip()

            if not matricule or not type_v or not modele:
                messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
                return
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO vehicule (matricule_vehicule, type_vehicule, modele_vehicule, etat) VALUES (%s,%s,%s,%s)",
                               (matricule, type_v, modele, etat))
                conn.commit()
                conn.close()
                self.load_bus()
                messagebox.showinfo("Succès", "Bus ajouté")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(win, text="Ajouter", bg="#2ecc71", fg="white", width=14, command=save).pack(pady=15)

    # ---------- MODIFIER ----------
    def modifier_bus(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un bus")
            return
        item = self.tree.item(selected[0])
        matricule_old = item["values"][0]

        win = tk.Toplevel(self.root)
        win.title("Modifier Bus")
        win.geometry("350x300")

        tk.Label(win, text="Matricule:").pack(pady=5)
        matricule_entry = tk.Entry(win)
        matricule_entry.insert(0, item["values"][0])
        matricule_entry.pack(pady=5)

        tk.Label(win, text="Type:").pack(pady=5)
        type_entry = tk.Entry(win)
        type_entry.insert(0, item["values"][1])
        type_entry.pack(pady=5)

        tk.Label(win, text="Modèle:").pack(pady=5)
        modele_entry = tk.Entry(win)
        modele_entry.insert(0, item["values"][2])
        modele_entry.pack(pady=5)

        tk.Label(win, text="État:").pack(pady=5)
        etat_combo = ttk.Combobox(win, values=["Fonctionnel", "En panne"], state="readonly")
        etat_combo.pack(pady=5)
        etat_combo.set(item["values"][3])

        def save_changes():
            matricule = matricule_entry.get().strip()
            type_v = type_entry.get().strip()
            modele = modele_entry.get().strip()
            etat = etat_combo.get().strip()

            if not matricule or not type_v or not modele:
                messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
                return
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE vehicule SET matricule_vehicule=%s, type_vehicule=%s, modele_vehicule=%s, etat=%s WHERE matricule_vehicule=%s",
                               (matricule, type_v, modele, etat, matricule_old))
                conn.commit()
                conn.close()
                self.load_bus()
                messagebox.showinfo("Succès", "Bus modifié")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(win, text="Enregistrer", bg="#3498db", fg="white", width=14, command=save_changes).pack(pady=15)

    # ---------- SUPPRIMER ----------
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
                self.load_bus()
                messagebox.showinfo("Succès", "Bus supprimé")
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    # ---------- RETOUR ----------
    def retour(self):
        self.root.destroy()