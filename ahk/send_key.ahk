#Requires AutoHotkey v2.0
#SingleInstance Force

; Nome da janela do Return Of The Saiyans
TargetTitle := "Return Of The Saiyans"

if A_Args.Length > 0
{
    key := A_Args[1]

    if WinExist(TargetTitle)
    {
        try {
            ; Envia a tecla em background para a janela do jogo
            ControlSend "{" key "}",, TargetTitle
        }
    }
}
ExitApp