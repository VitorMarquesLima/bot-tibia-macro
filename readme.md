# DBBot Pro - Tibia Automation Tool

Este projeto é uma ferramenta de automação externa para Tibia (e derivados), desenvolvida em **Python** com integração via **AutoHotkey (AHK)** para simulação de teclas.

O foco atual é oferecer um sistema de **Combo/Rotação** de alta precisão baseado em tempo (Cooldowns), **Auto Attack** e **Auto Food**, com uma interface gráfica (GUI) amigável e Overlay (HUD) visual.

## 🚀 Status Atual do Projeto

O projeto encontra-se em estágio **Estável** (v1.0 - Core Logic).

### ✅ Funcionalidades Implementadas
- [x] **Interface Gráfica (GUI):** Construída com Tkinter, organizada em abas (Combo, Utilidades, Ajustes).
- [x] **Overlay (HUD):** Janela transparente e *Always-on-Top* que mostra o status (ON/OFF) do Combo, Attack e Food.
- [x] **Sistema de Combo (Time-based):**
    - Execução de magias baseada em milissegundos (ms).
    - Suporte a **Double Cast (2x)**: Executa a mesma magia duas vezes com intervalo curto.
    - Sistema de Prioridade na fila de execução.
    - **Otimização:** Removida verificação de imagem (pixel reading) para garantir execução instantânea das magias.
- [x] **Auto Attack:** Mantém a tecla de ataque do jogo pressionada/ativa.
- [x] **Auto Food:** Consome comida automaticamente baseado em intervalo de minutos configurável.
- [x] **Gestão de Hotkeys:**
    - Hotkeys globais para ligar/desligar funções sem focar na janela do bot.
    - Proteção contra campos vazios na configuração.
- [x] **Sistema de Perfis:** Salvar e carregar configurações completas em arquivos `.json`.

### 🚧 Em Desenvolvimento / Futuro
- [ ] Auto Healing (Cura baseada em % de vida).
- [ ] Reimplementação opcional de verificação de Target (Image Search).
- [ ] Anti-Idle.

---

## 🛠️ Pré-requisitos

Para rodar este projeto, você precisa ter instalado:

1.  **Python 3.x**: [Download](https://www.python.org/downloads/)
2.  **AutoHotkey (v1.1 ou v2)**: Necessário para o envio de teclas via script `.ahk`. [Download](https://www.autohotkey.com/)

### Bibliotecas Python
Instale as dependências executando no terminal:

```bash
pip install keyboard pyautogui