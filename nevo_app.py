import customtkinter as ctk
from google import genai
import threading
import time
import requests
import sys
import os

# --- CONFIGURATION ---
API_KEY = "AIzaSyDzGQwSFBODnhO4uj9qIt-D-5fDX2765GE"
client = genai.Client(api_key=API_KEY)

# Ensure this version is the same in your local file and on GitHub
VERSION = "1.0.5" 

# Your GitHub RAW link (Must be exactly this for your account)
UPDATE_URL = "https://raw.githubusercontent.com/narmzliusnarmzlius-cmd/nevo-x-update/refs/heads/main/nevo_app.py"
 

class NevoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"Nevo-X v{VERSION}")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        # Try to load window icon if logo.ico exists
        try:
            if os.path.exists("logo.ico"):
                self.iconbitmap("logo.ico")
        except:
            pass

        # Chat display area
        self.chat_display = ctk.CTkTextbox(self, width=600, height=450, state="disabled", corner_radius=15, font=("Roboto", 14))
        self.chat_display.pack(padx=20, pady=20, fill="both", expand=True)

        # Input field
        self.entry = ctk.CTkEntry(self, placeholder_text="Ask Nevo-X...", height=45, corner_radius=10)
        self.entry.pack(padx=20, pady=(0, 20), fill="x")
        self.entry.bind("<Return>", lambda e: self.send_message())

        # Check for updates in the background without auto-deleting the app
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def check_for_updates(self):
        try:
            response = requests.get(UPDATE_URL, timeout=5)
            if response.status_code == 200:
                # If the version string in GitHub file is different from our VERSION
                if f'VERSION = "{VERSION}"' not in response.text:
                    self.display_message("SYSTEM", "A new version of Nevo-X is available!")
                    self.display_message("SYSTEM", "Please visit GitHub to download the latest update.")
        except:
            pass

    def display_message(self, sender, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"{sender}: {text}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def ask_ai_logic(self, prompt):
        # Professional English instructions
        instr = (
            "You are Nevo-X, a professional AI assistant created by Nevo. "
            "Always respond in English. "
            "Be helpful, direct, and concise. "
            "Do not mention your creator or name unless explicitly asked."
        )
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=instr + prompt,
                config={"tools": [{"google_search": {}}]}
            )
            answer = response.text.strip()
            self.after(0, lambda: self.display_message("Nevo-X", answer))
        except:
            self.after(0, lambda: self.display_message("Nevo-X", "Connection error. Please try again."))

    def send_message(self):
        txt = self.entry.get()
        if not txt: return
        self.display_message("You", txt)
        self.entry.delete(0, "end")
        threading.Thread(target=self.ask_ai_logic, args=(txt,), daemon=True).start()

if __name__ == "__main__":
    app = NevoApp()
    app.mainloop()

