import customtkinter as ctk
from google import genai
import threading
import requests
import sys
import os
import subprocess
import time

# --- CONFIGURATION ---
API_KEY = "AIzaSyDzGQwSFBODnhO4uj9qIt-D-5fDX2765GE"
client = genai.Client(api_key=API_KEY)

VERSION = "1.0.8" 
UPDATE_URL = "https://raw.githubusercontent.com/narmzliusnarmzlius-cmd/nevo-x-update/refs/heads/main/nevo_app.py"


class NevoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"Nevo-X v{VERSION}")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        try:
            if os.path.exists("logo.ico"):
                self.iconbitmap("logo.ico")
        except:
            pass

        self.chat_display = ctk.CTkTextbox(self, width=600, height=450, state="disabled", corner_radius=15)
        self.chat_display.pack(padx=20, pady=20, fill="both", expand=True)

        self.entry = ctk.CTkEntry(self, placeholder_text="Ask Nevo-X...", height=45, corner_radius=10)
        self.entry.pack(padx=20, pady=(0, 20), fill="x")
        self.entry.bind("<Return>", lambda e: self.send_message())

        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def display_message(self, sender, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"{sender}: {text}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def check_for_updates(self):
        try:
            response = requests.get(UPDATE_URL, timeout=5)
            if response.status_code == 200:
                if f'VERSION = "{VERSION}"' not in response.text:
                    self.after(0, lambda: self.display_message("SYSTEM", "New update found! Restarting in 3 seconds..."))
                    time.sleep(3)
                    self.execute_auto_update(response.text)
        except:
            pass

    def execute_auto_update(self, new_code):
        # 1. Išsaugome naują kodą į laikiną failą
        file_path = os.path.abspath(sys.argv[0])
        temp_file = "new_version.py"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(new_code)

        # 2. Sukuriame Batch skriptą, kuris sukeis failus
        # Jis palaukia, kol Nevo-X užsidarys, tada perrašo ir vėl paleidžia
        batch_script = "updater.bat"
        with open(batch_script, "w") as f:
            f.write(f'@echo off\n')
            f.write(f'timeout /t 2 /nobreak > nul\n')
            f.write(f'copy /y "{temp_file}" "{file_path}"\n')
            f.write(f'del "{temp_file}"\n')
            f.write(f'start "" python "{file_path}"\n')
            f.write(f'del "%~f0"\n')

        # 3. Paleidžiame skriptą fone ir išjungiam programą
        subprocess.Popen([batch_script], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        self.destroy()
        sys.exit()

    def ask_ai_logic(self, prompt):
        instr = "You are Nevo-X. Respond in English."
        try:
            response = client.models.generate_content(model="gemini-2.0-flash", contents=instr + prompt)
            self.after(0, lambda: self.display_message("Nevo-X", response.text.strip()))
        except:
            self.after(0, lambda: self.display_message("Nevo-X", "Error."))

    def send_message(self):
        txt = self.entry.get()
        if txt:
            self.display_message("You", txt)
            self.entry.delete(0, "end")
            threading.Thread(target=self.ask_ai_logic, args=(txt,), daemon=True).start()

if __name__ == "__main__":
    app = NevoApp()
    app.mainloop()
