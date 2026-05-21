# Projeto_Tkinter.py
# Interface gráfica principal do jogo The Floor

import tkinter as tk
from tkinter import messagebox
import os

# chdir UMA SÓ VEZ, aqui, antes de qualquer import do projeto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from duelos_tkinter import iniciar_jogo_tkinter, carregar_jogo_tkinter
from graficos_the_floor import abrir_janela_graficos
from tabuleiro_tkinter import abrir_tabuleiro
from gestao_jogadores_tkinter import menu_jogadores_tkinter
from gestao_categorias_tkinter import menu_categorias_tkinter


CORES = {
    "bg":      "#0d1b2a",
    "accent":  "#1976d2",
    "titulo":  "#ffd600",
    "texto":   "#ffffff",
    "cinza":   "#546e7a",
    "verde":   "#43a047",
    "vermelho":"#e53935",
}


def _btn(pai, texto, comando, cor=None):
    cor = cor or CORES["accent"]
    return tk.Button(
        pai, text=texto, command=comando,
        font=("Impact", 15), width=26,
        bg=cor, fg="white", relief="flat",
        activebackground=CORES["cinza"], activeforeground="white",
        cursor="hand2", pady=8,
    )


# ── Janela inicial ────────────────────────────────────────────────────────────

def _janela_inicial(root):
    root.title("The Floor")
    root.geometry("520x380")
    root.configure(bg=CORES["bg"])
    root.resizable(True, True)

    tk.Label(root, text="THE FLOOR",
             font=("Impact", 32), fg=CORES["titulo"], bg=CORES["bg"]).pack(pady=(40, 10))
    tk.Label(root, text="Queres começar o jogo?",
             font=("Impact", 13), fg=CORES["texto"], bg=CORES["bg"]).pack(pady=6)

    _btn(root, "Começar Jogo", lambda: _abrir_menu(root), cor=CORES["verde"]).pack(pady=6)
    _btn(root, "Sair",         root.destroy,               cor=CORES["cinza"]).pack(pady=4)


# ── Menu principal ────────────────────────────────────────────────────────────

def _abrir_menu(root):
    # NÃO esconder o root — mantê-lo visível evita problemas com grab_set
    # Minimizamos em vez de withdraw para não perder o contexto de janela
    root.withdraw()

    menu = tk.Toplevel(root)
    menu.title("The Floor — Menu")
    menu.geometry("560x620")
    menu.configure(bg=CORES["bg"])
    menu.resizable(True, True)
    # Garantir que o menu aparece no centro do ecrã
    menu.update_idletasks()
    x = (menu.winfo_screenwidth()  - 560) // 2
    y = (menu.winfo_screenheight() - 620) // 2
    menu.geometry(f"560x620+{x}+{y}")

    def ao_fechar():
        menu.destroy()
        root.deiconify()

    menu.protocol("WM_DELETE_WINDOW", ao_fechar)

    tk.Label(menu, text="THE FLOOR",
             font=("Impact", 30), fg=CORES["titulo"], bg=CORES["bg"]).pack(pady=(20, 14))

    # wrapper para fechar menu antes de abrir cada sub-janela
    def abrir(fn, *args):
        def _cmd():
            try:
                if args:
                    fn(*args)
                else:
                    fn()
            except Exception as e:
                messagebox.showerror("Erro", str(e), parent=menu)
        return _cmd

    botoes = [
        ("🎮  Novo Jogo",        abrir(iniciar_jogo_tkinter, menu), CORES["verde"]),
        ("📂  Carregar Jogo",    abrir(carregar_jogo_tkinter),      CORES["accent"]),
        ("🗺   Ver Tabuleiro",   abrir(abrir_tabuleiro),            CORES["accent"]),
        ("📊  Estatísticas",     abrir(abrir_janela_graficos),      CORES["accent"]),
        ("👥  Gerir Jogadores",  abrir(menu_jogadores_tkinter),     CORES["accent"]),
        ("❓  Gerir Perguntas",  abrir(menu_categorias_tkinter),    CORES["accent"]),
        ("🚪  Sair",             root.destroy,                      CORES["vermelho"]),
    ]

    for texto, comando, cor in botoes:
        _btn(menu, texto, comando, cor=cor).pack(pady=4)


# ── Arranque ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    _janela_inicial(root)
    root.mainloop()
