import tkinter as tk

class ChatbotPassager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chatbot Passager SRTB")
        self.root.geometry("400x400")
        self.root.configure(bg="black")  # fond noir

        # Titre
        tk.Label(self.root, text="Chatbot Passager SRTB", font=("Arial", 16, "bold"),
                 bg="black", fg="#FF8C00").pack(pady=10)  # titre orange

        # Zone de chat
        self.chat_text = tk.Text(self.root, state="disabled", height=15,
                                 bg="black", fg="yellow", font=("Arial", 12))
        self.chat_text.pack(padx=10, pady=10, fill="both", expand=True)

        # Champ texte
        self.entry = tk.Entry(self.root, bg="black", fg="yellow", insertbackground="yellow", font=("Arial", 12))
        self.entry.pack(fill="x", padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        # Bouton envoyer
        tk.Button(self.root, text="Envoyer", bg="#FF8C00", fg="black",
                  font=("Arial", 12, "bold"), command=self.send_message).pack(pady=5)

        self.root.mainloop()

    def send_message(self, event=None):
        user_msg = self.entry.get().strip()
        if not user_msg:
            return
        self.entry.delete(0, "end")

        # Afficher le message utilisateur en jaune
        self.chat_text.config(state="normal")
        self.chat_text.insert("end", f"Vous: {user_msg}\n", "user")
        
        # Réponse du chatbot en blanc
        response = self.generate_response(user_msg)
        self.chat_text.insert("end", f"Chatbot: {response}\n\n", "bot")
        self.chat_text.config(state="disabled")
        self.chat_text.see("end")

        # Tags pour couleurs
        self.chat_text.tag_config("user", foreground="yellow")
        self.chat_text.tag_config("bot", foreground="white")

    def generate_response(self, msg):
        msg = msg.lower()
        if any(x in msg for x in ["bonjour", "salut"]):
            return "Bonjour ! Comment puis-je vous aider ?"
        elif "horaire" in msg:
            return "Les horaires des bus sont disponibles sur le site SRTB."
        elif "ticket" in msg or "prix" in msg:
            return "Le prix d'un ticket est de 1,500 TND."
        elif "bus" in msg:
            return "Pouvez-vous préciser la ligne ou la station ?"
        else:
            return "Désolé, je n'ai pas compris. Pouvez-vous reformuler ?"

# Lancer le chatbot
if __name__ == "__main__":
    ChatbotPassager()