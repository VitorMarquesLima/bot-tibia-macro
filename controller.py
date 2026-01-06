import subprocess
import threading
import time
import os
import keyboard
import tkinter as tk
import json

class BotController:
    def __init__(self):
        self.running = False
        self.stop_event = threading.Event()
        self.priority_lock = threading.Lock()
        self.bat_path = os.path.join("ahk", "run_ahk.bat")
        
        # Estados
        self.combo_enabled = False
        self.attack_enabled = False
        self.food_enabled = False
        
        # Controle de tempo
        self.combo_cooldowns_status = {}
        self.last_food_time = 0
        
        self.overlay_window = None

    def create_overlay(self):
        if self.overlay_window: return
        self.overlay_window = tk.Toplevel()
        self.overlay_window.overrideredirect(True)
        self.overlay_window.attributes("-topmost", True, "-transparentcolor", "black")
        self.overlay_window.config(bg="black")
        self.overlay_window.geometry("+450+120")
        
        self.lbl_combo = tk.Label(self.overlay_window, text="Combo: OFF", fg="#FF3333", bg="black", font=("Arial", 11, "bold"))
        self.lbl_combo.pack(anchor="w")
        self.lbl_attack = tk.Label(self.overlay_window, text="Auto Attack: OFF", fg="#FF3333", bg="black", font=("Arial", 11, "bold"))
        self.lbl_attack.pack(anchor="w")
        self.lbl_food = tk.Label(self.overlay_window, text="Auto Food: OFF", fg="#FF3333", bg="black", font=("Arial", 11, "bold"))
        self.lbl_food.pack(anchor="w")

    def update_overlay_ui(self):
        if not self.overlay_window: return
        self.lbl_combo.config(text=f"Combo: {'ON' if self.combo_enabled else 'OFF'}", 
                              fg="#00FF00" if self.combo_enabled else "#FF3333")
        self.lbl_attack.config(text=f"Auto Attack: {'ON' if self.attack_enabled else 'OFF'}", 
                               fg="#00FF00" if self.attack_enabled else "#FF3333")
        self.lbl_food.config(text=f"Auto Food: {'ON' if self.food_enabled else 'OFF'}", 
                               fg="#00FF00" if self.food_enabled else "#FF3333")

    def toggle_combo(self):
        if self.running:
            self.combo_enabled = not self.combo_enabled
            self.update_overlay_ui()

    def toggle_attack(self):
        if self.running:
            self.attack_enabled = not self.attack_enabled
            self.update_overlay_ui()

    def toggle_food(self):
        if self.running:
            self.food_enabled = not self.food_enabled
            self.update_overlay_ui()

    def call_ahk(self, key, is_priority=False):
        # Evita chamar script se a tecla for vazia ou se ALT estiver pressionado
        if not key or str(key).strip() == "" or keyboard.is_pressed('alt'): return
        
        # Se não for prioridade e já tiver uma execucao prioritaria rodando, ignora
        if not is_priority and self.priority_lock.locked(): return
        
        try:
            subprocess.run([self.bat_path, key], shell=True, check=False)
        except: pass

    def loop_bot(self, settings):
        while not self.stop_event.is_set():
            if self.running:
                current_time = time.time() * 1000.0
                
                # --- Auto Attack ---
                if self.attack_enabled:
                    self.call_ahk(settings.get('attack_key'))
                
                # --- Auto Food ---
                if self.food_enabled:
                    f_min = settings.get('food_min', 9)
                    # Converte minutos para ms
                    if current_time - self.last_food_time >= (float(f_min) * 60000):
                        self.call_ahk(settings.get('food_key'))
                        self.last_food_time = current_time

                # --- Combo (Sem verificação de target) ---
                if self.combo_enabled:
                    reduction = float(settings.get('cd_reduction', 0) or 0)
                    
                    for item in settings.get('combo', []):
                        actual_ms = float(item['ms']) * (1.0 - (reduction / 100.0))
                        last_used = self.combo_cooldowns_status.get(item['key'], 0)
                        
                        if current_time - last_used >= actual_ms:
                            # Executa a magia
                            self.call_ahk(item['key'], item.get('priority', False))
                            
                            # Logica do 2x (double cast)
                            if item.get('2x'):
                                time.sleep(float(item.get('2x_ms', 50)) / 1000.0)
                                self.call_ahk(item['key'], item.get('priority', False))
                            
                            # Atualiza o tempo da ultima utilização
                            self.combo_cooldowns_status[item['key']] = current_time
                
                # Pequena pausa para não usar 100% da CPU
                time.sleep(0.01) 
            else:
                time.sleep(0.1)

    def start_bot(self, settings):
        self.stop_event.clear()
        self.running = True
        self.last_food_time = 0
        self.create_overlay()
        self.update_overlay_ui()
        # Inicia a thread principal do bot
        threading.Thread(target=self.loop_bot, args=(settings,), daemon=True).start()

    def stop_bot(self):
        self.stop_event.set()
        self.running = False
        self.combo_enabled = False
        self.attack_enabled = False
        self.food_enabled = False
        if self.overlay_window:
            self.overlay_window.destroy()
            self.overlay_window = None

    def save_profile(self, profile_name, data):
        with open(f"perfil_{profile_name}.json", 'w') as f:
            json.dump(data, f, indent=4)

    def load_profile(self, profile_name):
        filename = f"perfil_{profile_name}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return None