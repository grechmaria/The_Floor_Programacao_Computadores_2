# Projeto_Tkinter.py
# Interface gráfica principal do jogo The Floor

import tkinter as tk
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from duelos_tkinter import iniciar_jogo_tkinter, carregar_jogo_tkinter
from graficos_the_floor import abrir_janela_graficos
from tabuleiro_tkinter import abrir_tabuleiro
from gestao_jogadores_tkinter import menu_jogadores_tkinter          
from gestao_categorias_tkinter import menu_categorias_tkinter        


# ── Janela de menu principal ──────────────────────────────────────────────────

def abrir_menu_jogo():
    janela_inicial.withdraw()

    menu = tk.Toplevel()
    menu.title("The Floor - Menu")
    menu.geometry("400x440")
    menu.configure(bg="black")

    tk.Label(
        menu, text="THE FLOOR",
        font=("Impact", 30), fg="#4fc3f7", bg="black",
    ).pack(pady=20)

    botoes = [
        ("Novo Jogo",        lambda: iniciar_jogo_tkinter(menu)),
        ("Carregar Jogo",    carregar_jogo_tkinter),
        ("Ver Tabuleiro",    abrir_tabuleiro),
        ("Estatísticas",     abrir_janela_graficos),
        ("Gerir Jogadores",  menu_jogadores_tkinter),                # ← corrigido
        ("Gerir Perguntas",  menu_categorias_tkinter),               # ← corrigido
        ("Sair",             janela_inicial.destroy),
    ]

    for texto, comando in botoes:
        tk.Button(
            menu, text=texto,
            font=("Impact", 12), width=20,
            command=comando,
        ).pack(pady=5)


def sair():
    janela_inicial.destroy()


# ── Janela inicial (ecrã de boas-vindas) ─────────────────────────────────────

janela_inicial = tk.Tk()
janela_inicial.title("The Floor")
janela_inicial.geometry("400x300")
janela_inicial.configure(bg="black")

tk.Label(
    janela_inicial, text="THE FLOOR",
    font=("Impact", 28), fg="blue", bg="black",
).pack(pady=40)

tk.Label(
    janela_inicial, text="Queres começar o jogo?",
    font=("Impact", 13), fg="blue", bg="black",
).pack(pady=10)

tk.Button(
    janela_inicial, text="Começar Jogo",
    font=("Impact", 12), width=20,
    command=abrir_menu_jogo,
).pack(pady=10)

tk.Button(
    janela_inicial, text="Sair",
    font=("Impact", 12), width=20,
    command=sair,
).pack(pady=5)

janela_inicial.mainloop()

