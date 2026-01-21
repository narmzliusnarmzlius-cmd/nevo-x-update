def check_for_updates(self):
        try:
            response = requests.get(UPDATE_URL, timeout=5)
            if response.status_code == 200:
                if f'VERSION = "{VERSION}"' not in response.text:
                    self.display_message("SYSTEM", "Updating to latest version... Please wait.")
                    
                    # 1. Gauname dabartinio .exe kelią
                    current_exe = os.path.abspath(sys.argv[0])
                    new_code_content = response.text
                    
                    # 2. Įrašome naują kodą į laikiną .py failą (tik tam kartui)
                    temp_py = os.path.join(os.getenv('TEMP'), "update_script.py")
                    with open(temp_py, "w", encoding="utf-8") as f:
                        f.write(new_code_content)

                    # 3. Paleidžiame PowerShell komandą, kuri palauks 2 sek (kol Nevo užsidarys),
                    #    tada sukompiliuos naują versiją arba tiesiog praneš.
                    #    Kadangi pilnas perrašymas be PyInstaller neįmanomas, 
                    #    geriausia yra atsisiųsti paruoštą .exe failą.
                    
                    # Jei tavo GitHub'e būtų tiesioginė nuoroda į Nevo-X.exe:
                    exe_url = "TAVO_TIESIOGINE_NUORODA_I_EXE_FAILA_GITHUB"
                    
                    # Kol kas saugiausia Windows sistema yra ši:
                    self.display_message("SYSTEM", "New version detected. Opening update link...")
                    import webbrowser
                    webbrowser.open("https://github.com/narmzliusnarmzlius-cmd/nevo-x-update/releases")
        except:
            pass
