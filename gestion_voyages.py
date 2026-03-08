import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import connect_db

class GestionVoyages:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Voyages")
        self.root.geometry("700x400")

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("id_voyage","id_trajet","matricule","date","heure"), show="headings")
        self.tree.heading("id_voyage", text="ID Voyage")
        self.tree.heading("id_trajet", text="ID Trajet")
        self.tree.heading("matricule", text="Matricule Bus")
        self.tree.heading("date", text="Date Voyage")
        self.tree.heading("heure", text="Heure")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Boutons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Ajouter Voyage", command=self.ajouter_voyage).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Modifier Voyage", command=self.modifier_voyage).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Supprimer Voyage", command=self.supprimer_voyage).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Rafraîchir", command=self.load_voyages).pack(side="left", padx=5)

        self.load_voyages()
        self.root.mainloop()

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

    def ajouter_voyage(self):
        id_trajet = simpledialog.askinteger("Ajouter Voyage", "ID Trajet:")
        matricule = simpledialog.askstring("Ajouter Voyage", "Matricule Bus:")
        date_voyage = simpledialog.askstring("Ajouter Voyage", "Date (YYYY-MM-DD):")
        heure = simpledialog.askstring("Ajouter Voyage", "Heure (HH:MM):")
        if id_trajet and matricule and date_voyage and heure:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO voyage (id_trajet, matricule_vehicule, date_voyage, heure) VALUES (%s,%s,%s,%s)",
                    (id_trajet, matricule, date_voyage, heure)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Voyage ajouté !")
                self.load_voyages()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

    def modifier_voyage(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un voyage")
            return
        item = self.tree.item(selected[0])
        id_voyage = item["values"][0]

        new_id_trajet = simpledialog.askinteger("Modifier Voyage", "ID Trajet:", initialvalue=item["values"][1])
        new_matricule = simpledialog.askstring("Modifier Voyage", "Matricule Bus:", initialvalue=item["values"][2])
        new_date = simpledialog.askstring("Modifier Voyage", "Date (YYYY-MM-DD):", initialvalue=item["values"][3])
        new_heure = simpledialog.askstring("Modifier Voyage", "Heure (HH:MM):", initialvalue=item["values"][4])

        if new_id_trajet and new_matricule and new_date and new_heure:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE voyage SET id_trajet=%s, matricule_vehicule=%s, date_voyage=%s, heure=%s WHERE id_voyage=%s",
                    (new_id_trajet, new_matricule, new_date, new_heure, id_voyage)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Voyage modifié !")
                self.load_voyages()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))

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
                messagebox.showinfo("Succès", "Voyage supprimé !")
                self.load_voyages()
            except Exception as e:
                messagebox.showerror("Erreur DB", str(e))