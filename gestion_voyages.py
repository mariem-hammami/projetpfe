import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import connect_db

class GestionVoyages:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestion des Voyages & Pannes")
        self.root.geometry("700x400")

        self.tree = ttk.Treeview(self.root, columns=("id_voyage","id_trajet","matricule","date","heure","etat"), show="headings")
        self.tree.heading("id_voyage", text="ID Voyage")
        self.tree.heading("id_trajet", text="ID Trajet")
        self.tree.heading("matricule", text="Matricule Bus")
        self.tree.heading("date", text="Date Voyage")
        self.tree.heading("heure", text="Heure")
        self.tree.heading("etat", text="État (OK/Panne)")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

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
            cursor.execute("SELECT id_voyage,id_trajet,matricule_vehicule,date_voyage,heure,etat FROM voyage")
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
        etat = simpledialog.askstring("Ajouter Voyage", "État (OK/Panne):")
        if id_trajet and matricule and date_voyage and heure and etat:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO voyage (id_trajet, matricule_vehicule, date_voyage, heure, etat) VALUES (%s,%s,%s,%s,%s)",
                               (id_trajet, matricule, date_voyage, heure, etat))
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

        new_etat = simpledialog.askstring("Modifier Voyage", "État (OK/Panne):", initialvalue=item["values"][5])
        if new_etat:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE voyage SET etat=%s WHERE id_voyage=%s", (new_etat, id_voyage))
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