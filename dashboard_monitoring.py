import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime

class DashboardMonitoringPRO:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Dashboard Monitoring SRTB - Temps Réel")
        self.root.geometry("950x600")
        self.root.config(bg="white")  # fond principal en blanc

        # ----- Header -----
        header = tk.Frame(self.root, bg="#E07B00", height=60)  # orange sombre
        header.pack(fill="x")

        tk.Label(header,
                 text="Monitoring Passagers – SRTB",
                 bg="#E07B00",
                 fg="black",
                 font=("Arial", 18, "bold")).pack(side="left", padx=10, pady=15)

        # ----- Bouton Retour -----
        tk.Button(header,
                  text="Retour",
                  bg="white",
                  fg="black",
                  font=("Arial", 12, "bold"),
                  command=self.retour).pack(side="right", padx=10, pady=10)

        # ----- Total Passagers -----
        self.total_label = tk.Label(self.root,
                                    text="Total Passagers: 0 (A/D: 0/0)",
                                    font=("Arial", 14, "bold"),
                                    bg="white",        # fond blanc
                                    fg="#E07B00")      # texte orange sombre
        self.total_label.pack(pady=10)

        # ----- Treeview Lignes → Stations -----
        columns = ("ascendant", "descendant")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="white",    # fond tableau blanc
                        foreground="black",    # texte noir
                        fieldbackground="white",
                        font=("Arial", 12))
        style.map("Treeview",
                  background=[("selected", "#E07B00")],
                  foreground=[("selected", "black")])

        self.tree = ttk.Treeview(self.root, columns=columns)
        self.tree.heading("#0", text="Ligne / Station", anchor="w")
        self.tree.heading("ascendant", text="Ascendant")
        self.tree.heading("descendant", text="Descendant")
        self.tree.column("#0", width=250)
        self.tree.column("ascendant", width=100, anchor="center")
        self.tree.column("descendant", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # ----- Alertes -----
        self.alertes_text = tk.Text(self.root, height=5,
                                    bg="#FFF5F5", fg="red",
                                    font=("Arial", 12, "bold"))
        self.alertes_text.pack(fill="x", padx=10, pady=5)
        self.alertes_text.config(state="disabled")

        # ----- Bouton Rafraîchir -----
        tk.Button(self.root,
                  text="Rafraîchir",
                  bg="#E07B00",
                  fg="black",
                  font=("Arial", 12, "bold"),
                  command=self.update_dashboard).pack(pady=5)

        # ----- Lignes et Stations -----
        self.lignes = {
            "Corniche": ["Corniche Centre", "La Plage", "Port"],
            "Ras Jebal": ["Menzel Centre", "Zone Industrielle", "Hôpital"],
            "Tunis": ["Bizerte Gare", "Nozha", "Tunis Station"]
        }

        # Données simulées
        self.data = {}
        for ligne, stations in self.lignes.items():
            for station in stations:
                self.data[(ligne, station)] = {"asc": 0, "desc": 0}

        self.total_asc = 0
        self.total_desc = 0

        # Créer les lignes dans le Treeview
        self.ligne_ids = {}
        for ligne in self.lignes:
            self.ligne_ids[ligne] = self.tree.insert("", "end", text=ligne, open=True, tags=("ligne",))

        # Tag couleur lignes
        self.tree.tag_configure("ligne", foreground="#E07B00", font=("Arial", 13, "bold"))

        # ----- Lancer le dashboard -----
        self.update_dashboard()
        self.root.mainloop()

    # ----- Mise à jour Dashboard -----
    def update_dashboard(self):
        self.total_asc = 0
        self.total_desc = 0

        # Mise à jour des données simulées
        for (ligne, station), values in self.data.items():
            new_asc = random.randint(0, 5)
            new_desc = random.randint(0, 3)
            values["asc"] += new_asc
            values["desc"] += new_desc
            self.total_asc += new_asc
            self.total_desc += new_desc

        total = self.total_asc - self.total_desc
        self.total_label.config(text=f"Total Passagers: {total} (A/D: {self.total_asc}/{self.total_desc})")

        # Supprimer uniquement les stations existantes
        for ligne in self.lignes:
            for child in self.tree.get_children(self.ligne_ids[ligne]):
                self.tree.delete(child)

        # Ajouter stations sous chaque ligne
        for (ligne, station), values in self.data.items():
            self.tree.insert(self.ligne_ids[ligne], "end",
                             text=station,
                             values=(values["asc"], values["desc"]),
                             tags=("station",))

        # Tag couleur stations
        self.tree.tag_configure("station", foreground="black", font=("Arial", 12))  # texte noir

        # Alertes
        self.alertes_text.config(state="normal")
        self.alertes_text.delete("1.0", "end")
        if total > 80:
            self.alertes_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] ⚠ Surcharge détectée !\n")
        if random.choice([True, False]):
            ligne = random.choice(list(self.lignes.keys()))
            station = random.choice(self.lignes[ligne])
            self.alertes_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] ⚠ Bus en panne à {station} ({ligne})\n")
        if self.alertes_text.get("1.0", "end").strip() == "":
            self.alertes_text.insert("end", "Aucune alerte\n")
        self.alertes_text.config(state="disabled")

        # Refresh auto toutes les 10 secondes
        self.after_id = self.root.after(10000, self.update_dashboard)

    # ----- Retour -----
    def retour(self):
        if hasattr(self, "after_id"):
            self.root.after_cancel(self.after_id)
        self.root.destroy()