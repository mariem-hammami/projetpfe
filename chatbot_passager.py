import tkinter as tk
import ollama
import mysql.connector

# ---------- connexion database ----------

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="transport_db"
    )


# ---------- chatbot class ----------

class ChatbotPassager:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Chatbot Passager SRTB")
        self.root.geometry("450x450")
        self.root.configure(bg="black")

        # titre
        tk.Label(
            self.root,
            text="Chatbot Passager SRTB",
            font=("Arial", 16, "bold"),
            bg="black",
            fg="#FF8C00"
        ).pack(pady=10)

        # zone chat
        self.chat_text = tk.Text(
            self.root,
            state="disabled",
            bg="black",
            fg="white",
            font=("Arial", 12)
        )
        self.chat_text.pack(padx=10, pady=10, fill="both", expand=True)

        # champ message
        self.entry = tk.Entry(
            self.root,
            bg="black",
            fg="yellow",
            insertbackground="yellow",
            font=("Arial", 12)
        )
        self.entry.pack(fill="x", padx=10, pady=5)

        self.entry.bind("<Return>", self.send_message)

        # bouton envoyer
        tk.Button(
            self.root,
            text="Envoyer",
            bg="#FF8C00",
            fg="black",
            font=("Arial", 12, "bold"),
            command=self.send_message
        ).pack(pady=5)

        self.root.mainloop()

    # ---------- envoyer message ----------

    def send_message(self, event=None):

        user_msg = self.entry.get().strip()

        if not user_msg:
            return

        self.entry.delete(0, "end")

        self.chat_text.config(state="normal")

        self.chat_text.insert("end", f"Vous: {user_msg}\n", "user")

        response = self.generate_response(user_msg)

        self.chat_text.insert("end", f"Chatbot: {response}\n\n", "bot")

        self.chat_text.config(state="disabled")

        self.chat_text.see("end")

        self.chat_text.tag_config("user", foreground="yellow")
        self.chat_text.tag_config("bot", foreground="white")

    # ---------- get lignes + stations ----------

    def get_transport_info(self):

        try:

            conn = connect_db()

            cursor = conn.cursor()

            query = """
            SELECT l.libelle_ligne, s.libelle_station
            FROM ligne l
            JOIN ligne_station ls ON l.id_ligne = ls.id_ligne
            JOIN station s ON ls.id_station = s.id_station
            ORDER BY l.libelle_ligne, ls.ordre
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            conn.close()

            lignes = {}

            for ligne, station in rows:

                if ligne not in lignes:
                    lignes[ligne] = []

                lignes[ligne].append(station)

            text = ""

            for ligne in lignes:

                text += f"Ligne {ligne}:\n"

                for st in lignes[ligne]:

                    text += f"- {st}\n"

                text += "\n"

            return text

        except:
            return "Informations transport indisponibles."

    # ---------- réponse chatbot ----------

    def generate_response(self, msg):

        transport_info = self.get_transport_info()

        try:

            response = ollama.chat(
                model="mistral",
                messages=[
                    {
                        "role": "system",
                        "content": f"""
                        Tu es un assistant pour les passagers de la société SRTB de Bizerte.

                        Voici les lignes et stations disponibles:

                        {transport_info}

                        Réponds aux questions des passagers sur:
                        - les lignes
                        - les stations
                        - les bus
                        - les informations de transport
                        """
                    },
                    {
                        "role": "user",
                        "content": msg
                    }
                ]
            )

            return response["message"]["content"]

        except:

            return "Erreur de connexion avec le modèle IA."


# ---------- lancement ----------

if __name__ == "__main__":

    ChatbotPassager()