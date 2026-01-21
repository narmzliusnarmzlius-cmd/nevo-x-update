import customtkinter as ctk
from google import genai
import threading
import time
import requests
import sys
import os

# Konfigūracija
API_KEY = "AIzaSyDzGQwSFBODnhO4uj9qIt-D-5fDX2765GE"
client = genai.Client(api_key=API_KEY)
VERSION = "1.0.0"
# Čia turėtų būti nuoroda į tavo naujausią kodo failą (raw formatu)
UPDATE_URL = "https://tavo-nuoroda.com/nevo_app.py"
 

class NevoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"Nevo-X v{VERSION}")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.chat_display = ctk.CTkTextbox(self, width=600, height=450, state="disabled", corner_radius=15, font=("Roboto", 14))
        self.chat_display.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Klauskite Nevo-X...", height=45, corner_radius=10)
        self.entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = ctk.CTkButton(self.input_frame, text="SIŲSTI", command=self.send_message, width=120, height=45, corner_radius=10)
        self.send_btn.grid(row=0, column=1)

        # Paleidžiame atnaujinimo patikrą fone, kad netrukdytų startui
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def check_for_updates(self):
        """Tikrina ar yra nauja kodo versija"""
        try:
            # Pavyzdys: nuskaitome failą iš interneto
            response = requests.get(UPDATE_URL, timeout=5)
            if response.status_code == 200:
                # Jei faile randa kitokią versiją nei dabartinė, siūlo atnaujinti
                if f'VERSION = "{VERSION}"' not in response.text:
                    self.display_message("SISTEMA", "Rastas atnaujinimas. Siunčiama nauja versija...")
                    with open("nevo_app_new.py", "w", encoding="utf-8") as f:
                        f.write(response.text)
                    self.display_message("SISTEMA", "Atnaujinimas atsisiųstas. Prašome perkrauti programą.")
        except:
            pass # Jei nėra interneto, tiesiog praleidžiame

    def display_message(self, sender, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"{sender}: ")
        self.chat_display.configure(state="disabled")
        
        if sender == "Nevo-X":
            threading.Thread(target=self.animate_text, args=(text,), daemon=True).start()
        else:
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"{text}\n\n")
            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")

    def animate_text(self, text):
        self.chat_display.configure(state="normal")
        for char in text:
            self.chat_display.insert("end", char)
            self.chat_display.see("end")
            time.sleep(0.01)
        self.chat_display.insert("end", "\n\n")
        self.chat_display.configure(state="disabled")

    def ask_ai_logic(self, prompt):
        instr = (
            "Tu esi Nevo-X. Tave sukūrė Nevo. "
            "Niekada neprisistatyk savo vardu, nebent tavęs tiesiogiai paklausia. "
            "Kalbėk lietuviškai. Naudok internetą tyliai."
        )
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=instr + prompt,
                config={"tools": [{"google_search": {}}]}
            )
            t = response.text
            answer = t.strip()
            
            # Išvalome netyčinius prisistatymus
            bad_phrases = ["Aš esu Nevo-X, sukurtas Nevo.", "Aš esu Nevo-X, sukurta Nevo."]
            for phrase in bad_phrases:
                if answer.startswith(phrase):
                    answer = answer.replace(phrase, "").strip()

            self.after(0, lambda: self.display_message("Nevo-X", answer))
        except:
            self.after(0, lambda: self.display_message("Nevo-X", "Ryšio trikdis."))

    def send_message(self):
        user_text = self.entry.get()
        if not user_text: return
        self.display_message("Tu", user_text)
        self.entry.delete(0, "end")
        threading.Thread(target=self.ask_ai_logic, args=(user_text,), daemon=True).start()

if __name__ == "__main__":
    app = NevoApp()
    app.mainloop()