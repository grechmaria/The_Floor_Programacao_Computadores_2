# Projeto_Tkinter.py
# Ponto de entrada do jogo The Floor : janela inicial e menu principal
# O jogo deve executado neste ficheiro.

import tkinter as tk
from tkinter import messagebox
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from duelos_tkinter import (
    novo_duelo_tkinter,
    carregar_jogo_tkinter,
    reiniciar_jogo_tkinter,
)
from graficos_the_floor import abrir_janela_graficos
from tabuleiro_tkinter import abrir_tabuleiro
from gestao_jogadores_tkinter import menu_jogadores_tkinter
from gestao_categorias_tkinter import menu_categorias_tkinter


CORES = {
    "bg":       "#0d1b2a",
    "accent":   "#1976d2",
    "titulo":   "#ffd600",
    "texto":    "#ffffff",
    "cinza":    "#546e7a",
    "verde":    "#43a047",
    "vermelho": "#e53935",
    "laranja":  "#e65100",
}

#Função que cria e devolve um botão com as cores e fonte do jogo

def _btn(pai, texto, comando, cor=None):
    cor = cor or CORES["accent"]
    return tk.Button(
        pai, text=texto, command=comando,
        font=("Impact", 15), width=28,
        bg=cor, fg="white", relief="flat",
        activebackground=CORES["cinza"], activeforeground="white",
        cursor="hand2", pady=8,
    )


# Janela inicial

def _janela_inicial(root):
    root.title("The Floor")
    root.geometry("520x380")
    root.configure(bg=CORES["bg"])
    root.resizable(True, True)

    tk.Label(root, text="THE FLOOR",
             font=("Impact", 32), fg=CORES["titulo"], bg=CORES["bg"]).pack(pady=(40, 10))
    tk.Label(root, text="Queres começar o jogo?",
             font=("Impact", 13), fg=CORES["texto"], bg=CORES["bg"]).pack(pady=6)

    _btn(root, "Começar", lambda: _abrir_menu(root), cor=CORES["verde"]).pack(pady=6)
    _btn(root, "Sair",    root.destroy,               cor=CORES["cinza"]).pack(pady=4)


# Menu principal

def _abrir_menu(root):
    root.withdraw()

    menu = tk.Toplevel(root)
    menu.title("The Floor — Menu")
    menu.geometry("580x680")
    menu.configure(bg=CORES["bg"])
    menu.resizable(True, True)
    menu.update_idletasks()
    x = (menu.winfo_screenwidth()  - 580) // 2  # Obtém a largura total do ecrã em píxeis
    y = (menu.winfo_screenheight() - 680) // 2
    menu.geometry(f"580x680+{x}+{y}")

    def ao_fechar():
        menu.destroy()
        root.deiconify()

    menu.protocol("WM_DELETE_WINDOW", ao_fechar)

    tk.Label(menu, text="THE FLOOR",
             font=("Impact", 30), fg=CORES["titulo"], bg=CORES["bg"]).pack(pady=(20, 6))

    # Pequeno label cinzento para separar visualmente as secções do menu
    def separador(texto):
        tk.Label(menu, text=texto,
                 font=("Courier", 9), fg="#455a64", bg=CORES["bg"]).pack(pady=(8, 2))

    # Wrapper que apanha exceções e mostra uma caixa de erro em vez de crashar, fn é o parâmetro que recebe a função a executar
    def abrir(fn, *args):
        def _cmd():
            try:
                fn(*args) if args else fn()
            except Exception as e:
                messagebox.showerror("Erro", str(e), parent=menu)
        return _cmd


    separador("JOGO")

    _btn(menu, "▶  Novo Duelo",
         abrir(novo_duelo_tkinter), cor=CORES["verde"]).pack(pady=3)
    tk.Label(menu,
             text="Inicia um jogo novo (inicializa o tabuleiro com todos os jogadores)",
             font=("Courier", 8), fg="#78909c", bg=CORES["bg"]).pack()

    _btn(menu, "📂  Carregar Jogo",
         abrir(carregar_jogo_tkinter), cor=CORES["accent"]).pack(pady=3)
    tk.Label(menu,
             text="Retoma o jogo que estava em curso (estado guardado)",
             font=("Courier", 8), fg="#78909c", bg=CORES["bg"]).pack()

    _btn(menu, "🔄  Reiniciar Jogo",
         abrir(reiniciar_jogo_tkinter), cor=CORES["laranja"]).pack(pady=3)
    tk.Label(menu,
             text="Repõe todos os jogadores e apaga o historial (pede confirmação)",
             font=("Courier", 8), fg="#78909c", bg=CORES["bg"]).pack()


    separador("INFORMAÇÃO")

    _btn(menu, "🗺   Ver Tabuleiro",
         abrir(abrir_tabuleiro), cor=CORES["accent"]).pack(pady=3)
    _btn(menu, "📊  Estatísticas",
         abrir(abrir_janela_graficos), cor=CORES["accent"]).pack(pady=3)


    separador("GESTÃO")

    _btn(menu, "👥  Gerir Jogadores",
         abrir(menu_jogadores_tkinter), cor=CORES["accent"]).pack(pady=3)
    _btn(menu, "❓  Gerir Perguntas",
         abrir(menu_categorias_tkinter), cor=CORES["accent"]).pack(pady=3)

    tk.Frame(menu, bg=CORES["bg"], height=6).pack()
    _btn(menu, "🚪  Sair", root.destroy, cor=CORES["vermelho"]).pack(pady=4)


# Arranque

if __name__ == "__main__":
    root = tk.Tk()
    _janela_inicial(root)
    root.mainloop()