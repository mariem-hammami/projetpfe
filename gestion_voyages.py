import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

class GestionVoyages:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Voyages")
        self.root.geometry("750x500")
        self.root.configure(bg="#f4f6f9")

        # ---------- STYLE ----------
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#34495e", foreground="white")

        # ---------- TITRE ----------
        title = tk.Label(self.root, text="Gestion des Voyages", font=("Segoe UI", 20, "bold"), bg="#f4f6f9", fg="#2c3e50")
        title.pack(pady=15)

        # ---------- TABLE ----------
        table_frame = tk.Frame(self.root, bg="#f4f6f9")
        table_frame.pack(fill="both", expand=True, padx=20)

        scroll_y = tk.Scrollbar(table_frame)
        scroll_y.pack(side="right", fill="y")

        self.tree = ttk.Treeview(table_frame, columns=("id_voyage", "id_trajet", "matricule", "date", "heure"), show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree.yview)

        self.tree.heading("id_voyage", text="ID Voyage")
        self.tree.heading("id_trajet", text="ID Trajet")
        self.tree.heading("matricule", text="Matricule Bus")
        self.tree.heading("date", text="Date Voyage")
        self.tree.heading("heure", text="Heure")

        self.tree.column("id_voyage", width=100, anchor="w")
        self.tree.column("id_trajet", width=120, anchor="w")
        self.tree.column("matricule", width=150, anchor="w")
        self.tree.column("date", width=150, anchor="w")
        self.tree.column("heure", width=100, anchor="w")

        self.tree.pack(fill="both", expand=True)

        # ---------- BOUTONS ----------
        btn_frame = tk.Frame(self.root, bg="#f4f6f9")
        btn_frame.pack(pady=15)

        btn_style = {"font": ("Segoe UI", 11, "bold"), "width": 14, "bd": 0, "cursor": "hand2"}

        tk.Button(btn_frame, text="Ajouter", bg="#2ecc71", fg="white", command=self.ajouter_voyage, **btn_style).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Modifier", bg="#3498db", fg="white", command=self.modifier_voyage, **btn_style).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Supprimer", bg="#e74c3c", fg="white", command=self.supprimer_voyage, **btn_style).grid(row=0, column=2, padx=6)
        tk.Button(btn_frame, text="Rafraîchir", bg="#f39c12", fg="white", command=self.load_voyages, **btn_style).grid(row=0, column=3, padx=6)
        tk.Button(btn_frame, text="Retour", bg="#7f8c8d", fg="white", command=self.retour, **btn_style).grid(row=0, column=4, padx=6)

        self.load_voyages()

    # ---------- LOAD ----------
    def load_voyages(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id_voyage, id_trajet, matricule_vehicule, date_voyage, heure FROM voyage")
            for r in cursor.fetchall():
                self.tree.insert("", "end", values=r)
            conn.close()
        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    # ---------- AJOUT ----------
    def ajouter_voyage(self):
        win = tk.Toplevel(self.root)
        win.title("Ajouter Voyage")
        win.geometry("350x400")

        tk.Label(win, text="ID Trajet").pack(pady=5)
        id_trajet_entry = tk.Entry(win)
        id_trajet_entry.pack()

        tk.Label(win, text="Matricule Bus").pack(pady=5)
        matricule_entry = tk.Entry(win)  # ➜ ici on tape librement la matricule
        matricule_entry.pack()

        # ---------- DATE ----------
        tk.Label(win, text="Date Voyage").pack(pady=5)
        date_frame = tk.Frame(win)
        date_frame.pack(pady=2)
        year_combo = ttk.Combobox(date_frame, values=[str(y) for y in range(2024, 2031)], width=5)
        year_combo.pack(side="left", padx=2)
        month_combo = ttk.Combobox(date_frame, values=[f"{m:02}" for m in range(1, 13)], width=3)
        month_combo.pack(side="left", padx=2)
        day_combo = ttk.Combobox(date_frame, values=[f"{d:02}" for d in range(1, 32)], width=3)
        day_combo.pack(side="left", padx=2)

        # ---------- HEURE ----------
        tk.Label(win, text="Heure").pack(pady=5)
        time_frame = tk.Frame(win)
        time_frame.pack(pady=2)
        hour_combo = ttk.Combobox(time_frame, values=[f"{h:02}" for h in range(0, 24)], width=3)
        hour_combo.pack(side="left", padx=2)
        minute_combo = ttk.Combobox(time_frame, values=[f"{m:02}" for m in range(0, 60, 5)], width=3)
        minute_combo.pack(side="left", padx=2)

        def save():
            id_trajet = id_trajet_entry.get().strip()
            matricule = matricule_entry.get().strip()
            date_voyage = f"{year_combo.get()}-{month_combo.get()}-{day_combo.get()}"
            heure = f"{hour_combo.get()}:{minute_combo.get()}"

            if not id_trajet or not matricule or not all([year_combo.get(), month_combo.get(), day_combo.get()]) or not all([hour_combo.get(), minute_combo.get()]):
                messagebox.showwarning("Champs manquants", "Remplissez tous les champs")
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
                self.load_voyages()
                messagebox.showinfo("Succès", "Voyage ajouté")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

        tk.Button(win, text="Ajouter", bg="#2ecc71", fg="white", width=14, command=save).pack(pady=15)

    # ---------- MODIFIER ----------
    def modifier_voyage(self):
        messagebox.showinfo("Info", "Fonction de modification à implémenter de la même manière")

    # ---------- SUPPRIMER ----------
    def supprimer_voyage(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez un voyage")
            return
        item = self.tree.item(selected[0])
        id_voyage = item["values"][0]

        confirm = messagebox.askyesno("Supprimer", f"Supprimer voyage {id_voyage} ?")
        if confirm:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM voyage WHERE id_voyage=%s", (id_voyage,))
                conn.commit()
                conn.close()
                self.load_voyages()
                messagebox.showinfo("Succès", "Voyage supprimé")
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    # ---------- RETOUR ----------
    def retour(self):
        self.root.destroy()