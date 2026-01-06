import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import threading
from controller import BotController

class BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DBBot Pro - Tibia")
        self.root.geometry("480x750")
        
        self.controller = BotController()
        self.combo_data = []

        # --- CABEÇALHO ---
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(side="top", fill="x", padx=15, pady=10)

        self.btn_status = tk.Button(
            self.header_frame, text="OFF", bg="#e74c3c", fg="white", 
            font=("Arial", 12, "bold"), height=2, width=8, command=self.toggle_bot
        )
        self.btn_status.pack(side="left")

        self.lbl_info = tk.Label(self.header_frame, text="SISTEMA: OFFLINE", font=("Arial", 10, "bold"), fg="red")
        self.lbl_info.pack(side="right", padx=10)

        # --- ABAS ---
        self.tabs = ttk.Notebook(self.root)
        self.tab_combo = ttk.Frame(self.tabs)
        self.tab_utils = ttk.Frame(self.tabs)
        self.tab_config = ttk.Frame(self.tabs)
        
        self.tabs.add(self.tab_combo, text="Combo")
        self.tabs.add(self.tab_utils, text="Utilidades")
        self.tabs.add(self.tab_config, text="Ajustes")
        self.tabs.pack(expand=1, fill="both")

        self.setup_combo_tab()
        self.setup_utils_tab()
        self.setup_config_tab()
        
        # Garante que a hotkey Mestre (Delete) funcione assim que abrir
        self.update_master_hotkey()

    def setup_combo_tab(self):
        # -- Atributos --
        f_attr = tk.LabelFrame(self.tab_combo, text="Atributos")
        f_attr.pack(fill="x", padx=10, pady=5)
        tk.Label(f_attr, text="CD Reduction %:").grid(row=0, column=0, padx=5)
        self.ent_cd = tk.Entry(f_attr, width=10)
        self.ent_cd.insert(0, "0.0")
        self.ent_cd.grid(row=0, column=1)

        # -- Adicionar Magia --
        f_add = tk.LabelFrame(self.tab_combo, text="Adicionar Magia")
        f_add.pack(fill="x", padx=10, pady=5)
        
        self.ent_c_key = tk.Entry(f_add, width=8)
        self.ent_c_key.config(state='readonly')
        self.ent_c_key.grid(row=0, column=0, padx=5)
        tk.Button(f_add, text="Set", command=lambda: self.listen_key(self.ent_c_key)).grid(row=0, column=1)
        
        tk.Label(f_add, text="MS:").grid(row=0, column=2, padx=5)
        self.ent_c_ms = tk.Entry(f_add, width=8)
        self.ent_c_ms.grid(row=0, column=3)
        
        # Opções Extras
        self.v_2x = tk.BooleanVar()
        tk.Checkbutton(f_add, text="2x", variable=self.v_2x).grid(row=1, column=0)
        
        tk.Label(f_add, text="Intervalo 2x (ms):").grid(row=1, column=1, sticky="e")
        self.ent_2x_ms = tk.Entry(f_add, width=5)
        self.ent_2x_ms.insert(0, "50")
        self.ent_2x_ms.grid(row=1, column=2, sticky="w")
        
        self.v_pri = tk.BooleanVar()
        tk.Checkbutton(f_add, text="Prioridade", variable=self.v_pri).grid(row=1, column=3)
        
        tk.Button(f_add, text="ADICIONAR MAGIA", command=self.add_magia, bg="#3498db", fg="white").grid(row=2, column=0, columnspan=4, pady=8, sticky="ew")

        # -- Lista --
        self.listb = tk.Listbox(self.tab_combo, height=12)
        self.listb.pack(fill="both", padx=10, pady=5)
        tk.Button(self.tab_combo, text="Limpar Lista", command=self.clear_list).pack(pady=5)

    def setup_utils_tab(self):
        f_food = tk.LabelFrame(self.tab_utils, text="Auto Food")
        f_food.pack(fill="x", padx=10, pady=10)
        
        # Tecla para comer (Ex: F10)
        self.ent_food_key = self.create_hk_field(f_food, "Tecla Food (Jogo):", "", 0)
        
        # Minutos
        tk.Label(f_food, text="Minutos:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_food_min = tk.Entry(f_food, width=12)
        self.ent_food_min.insert(0, "9")
        self.ent_food_min.grid(row=1, column=1)
        
        # Hotkey para ligar/desligar auto food
        self.hk_food_toggle = self.create_hk_field(f_food, "Hotkey Ligar Food:", "", 2)

    def setup_config_tab(self):
        f_hk = tk.LabelFrame(self.tab_config, text="Atalhos Globais")
        f_hk.pack(fill="x", padx=10, pady=5)
        
        self.ent_game_atk = self.create_hk_field(f_hk, "Tecla Ataque Jogo:", "space", 0)
        self.hk_atk = self.create_hk_field(f_hk, "Hotkey Ligar AutoAtk:", "", 1)
        self.hk_combo = self.create_hk_field(f_hk, "Hotkey Ligar Combo:", "", 2)
        
        # Botão Master
        self.hk_master = self.create_hk_field(f_hk, "Ligar/Desligar Bot:", "delete", 3)

        # -- Perfil --
        f_prof = tk.LabelFrame(self.tab_config, text="Gestão de Perfis")
        f_prof.pack(fill="x", padx=10, pady=10)
        
        tk.Label(f_prof, text="Nome do Perfil:").pack(pady=2)
        self.ent_prof_name = tk.Entry(f_prof, width=30)
        self.ent_prof_name.pack(pady=5)
        
        f_btns = tk.Frame(f_prof)
        f_btns.pack(pady=5)
        tk.Button(f_btns, text="SALVAR PERFIL", bg="#2980b9", fg="white", command=self.save_p).pack(side="left", padx=5)
        tk.Button(f_btns, text="CARREGAR", command=self.load_p).pack(side="left", padx=5)

    def create_hk_field(self, frame, label_text, default_val, row):
        tk.Label(frame, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        
        ent = tk.Entry(frame, width=12)
        ent.insert(0, default_val) # Insere o valor ANTES de travar
        ent.config(state='readonly')
        ent.grid(row=row, column=1, padx=5)
        
        tk.Button(frame, text="Set", command=lambda: self.listen_key(ent)).grid(row=row, column=2)
        return ent

    def listen_key(self, entry):
        def capture():
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, "...pressione...")
            
            key_event = keyboard.read_event(suppress=True)
            if key_event.event_type == keyboard.KEY_DOWN:
                key = key_event.name
                entry.delete(0, tk.END)
                entry.insert(0, key)
                entry.config(state='readonly')
                
                # Se alterou a tecla mestre, atualiza o hook global
                if entry == self.hk_master:
                    self.root.after(100, self.update_master_hotkey)
                    
        threading.Thread(target=capture, daemon=True).start()

    def update_master_hotkey(self):
        try:
            keyboard.unhook_all()
            mk = self.hk_master.get()
            if mk and mk != "...pressione..." and mk.strip() != "":
                keyboard.add_hotkey(mk, self.toggle_bot)
        except Exception as e:
            print(f"Erro ao registrar hotkey master: {e}")

    def add_magia(self):
        k = self.ent_c_key.get()
        m = self.ent_c_ms.get()
        
        if k and m.isdigit() and k != "...pressione...":
            item = {
                'key': k, 
                'ms': m, 
                'priority': self.v_pri.get(), 
                '2x': self.v_2x.get(), 
                '2x_ms': self.ent_2x_ms.get()
            }
            self.combo_data.append(item)
            
            display_text = f"Tecla: {k} | MS: {m} {'[2X]' if item['2x'] else ''} {'[P]' if item['priority'] else ''}"
            self.listb.insert(tk.END, display_text)

    def clear_list(self):
        self.combo_data = []
        self.listb.delete(0, tk.END)

    def toggle_bot(self):
        if not self.controller.running:
            # Pega as hotkeys configuradas na GUI
            h_atk = self.hk_atk.get()
            h_combo = self.hk_combo.get()
            h_food = self.hk_food_toggle.get()
            
            # Registra hotkeys auxiliares (apenas se não estiverem vazias)
            if h_atk and h_atk not in ["", "...pressione..."]:
                keyboard.add_hotkey(h_atk, self.controller.toggle_attack)
            
            if h_combo and h_combo not in ["", "...pressione..."]:
                keyboard.add_hotkey(h_combo, self.controller.toggle_combo)
                
            if h_food and h_food not in ["", "...pressione..."]:
                keyboard.add_hotkey(h_food, self.controller.toggle_food)
            
            # Prepara configurações para enviar ao controller
            settings = {
                'cd_reduction': self.ent_cd.get(),
                'attack_key': self.ent_game_atk.get(),
                'food_key': self.ent_food_key.get(),
                'food_min': self.ent_food_min.get(),
                'combo': self.combo_data
            }
            
            self.controller.start_bot(settings)
            
            # Atualiza GUI
            self.btn_status.config(text="ON", bg="#2ecc71") # Verde
            self.lbl_info.config(text="SISTEMA: ONLINE", fg="green")
        else:
            self.controller.stop_bot()
            self.update_master_hotkey() # Reseta os hooks
            
            # Atualiza GUI
            self.btn_status.config(text="OFF", bg="#e74c3c") # Vermelho
            self.lbl_info.config(text="SISTEMA: OFFLINE", fg="red")

    def save_p(self):
        name = self.ent_prof_name.get()
        if name:
            data = {
                'cd': self.ent_cd.get(),
                'combo': self.combo_data
            }
            self.controller.save_profile(name, data)
            messagebox.showinfo("Sucesso", f"Perfil '{name}' salvo!")

    def load_p(self):
        name = self.ent_prof_name.get()
        p = self.controller.load_profile(name)
        if p:
            self.ent_cd.delete(0, tk.END)
            self.ent_cd.insert(0, p.get('cd', '0.0'))
            
            self.clear_list()
            self.combo_data = p.get('combo', [])
            
            for i in self.combo_data:
                display_text = f"Tecla: {i['key']} | MS: {i['ms']} {'[2X]' if i.get('2x') else ''} {'[P]' if i.get('priority') else ''}"
                self.listb.insert(tk.END, display_text)
            messagebox.showinfo("Sucesso", "Perfil carregado!")
        else:
            messagebox.showerror("Erro", "Perfil não encontrado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BotGUI(root)
    root.mainloop()