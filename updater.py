import requests
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Substitua com seus dados reais do GitHub
USER = "VitorMarquesLima"
REPO = "bot-tibia-macro"
VERSION_LOCAL = "1.0.0"

URL_VERSION = f"https://raw.githubusercontent.com/{USER}/{REPO}/main/version.txt"
URL_RELEASE = f"https://github.com/{USER}/{REPO}/releases/latest/download/DBBot_Pro.exe"

def check_update():
    try:
        response = requests.get(URL_VERSION, timeout=5)
        remote_version = response.text.strip()

        if remote_version != VERSION_LOCAL:
            answer = messagebox.askyesno("Atualização Disponível", 
                                        f"Versão {remote_version} encontrada!\nDeseja baixar a nova versão?")
            if answer:
                # Abre o navegador para download ou você pode implementar requests.get para baixar direto
                os.startfile(f"https://github.com/{USER}/{REPO}/releases")
                return False
        return True
    except Exception as e:
        print(f"Erro ao verificar: {e}")
        return True

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    if check_update():
        # Tenta abrir o bot principal
        if os.path.exists("DBBot_Pro.exe"):
            subprocess.Popen("DBBot_Pro.exe")
        elif os.path.exists("gui.py"):
            subprocess.Popen(["python", "gui.py"])
        else:
            messagebox.showerror("Erro", "Arquivo principal não encontrado!")