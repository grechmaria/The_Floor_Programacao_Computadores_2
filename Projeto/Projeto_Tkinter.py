# Projeto_Tkinter.py
# Interface gráfica principal do jogo The Floor

import tkinter as tk
import os
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from duelos import (
    iniciar_jogo,
    carregar_duelos,
    imprimir_tabuleiro,
    atualizar_tabuleiro,
    selecionar_vizinho_manual,
    executar_duelo,
    verificar_fim_jogo,
    escolher_proximo_desafiante,
)
from gestao_jogadores import carregar_jogadores, guardar_jogadores
from graficos_the_floor import abrir_janela_graficos
from tabuleiro_tkinter import abrir_tabuleiro
from gestao_jogadores import menu_jogadores
from gestao_categorias_perguntas import menu_categorias_perguntas


# Função Carregar Jogo
# Retoma o jogo a partir do estado guardado no jogadores.json
# sem reinicializar o tabuleiro

def carregar_jogo():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    jogadores = carregar_jogadores()

    if not jogadores:
        print("Não há jogadores registados.")
        return

    # Verifica se já existe um tabuleiro guardado
    jogadores_ativos = [j for j in jogadores if len(j.get("quadriculas", [])) > 0]
    if not jogadores_ativos:
        print("Não há jogo guardado. Inicia um novo jogo.")
        return

    print(f"\nJogo carregado! {len(jogadores_ativos)} jogadores ainda ativos.")

    duelos = carregar_duelos()

    # Reconstrói o tabuleiro a partir das quadrículas guardadas
    tabuleiro = [[" " for _ in range(10)] for _ in range(10)]
    for jogador in jogadores:
        for quad in jogador.get("quadriculas", []):
            tabuleiro[quad[0]][quad[1]] = jogador["nome"]

    imprimir_tabuleiro(tabuleiro)

    proximo_desafiante = None

    while True:
        if verificar_fim_jogo(jogadores):
            guardar_jogadores(jogadores)
            break

        if proximo_desafiante:
            desafiante = proximo_desafiante
            proximo_desafiante = None
        else:
            desafiante = random.choice([j for j in jogadores if len(j.get("quadriculas", [])) > 0])

        desafiado = selecionar_vizinho_manual(desafiante, jogadores)

        if desafiado is None:
            print(f"{desafiante['nome']} não tem vizinhos.")
            continue

        duelo = executar_duelo(desafiante, desafiado, jogadores, duelos)

        if duelo is None:
            continue

        tabuleiro = atualizar_tabuleiro(tabuleiro, jogadores)
        imprimir_tabuleiro(tabuleiro)

        vencedor_nome = duelo["vencedor"]
        proximo_desafiante = escolher_proximo_desafiante(vencedor_nome, jogadores)

        continuar = input("\nPrime Enter para o próximo duelo ou 0 para sair: ")
        if continuar == "0":
            guardar_jogadores(jogadores)
            print("Jogo pausado. O estado foi guardado.")
            break


# Janela inicial — ecrã de boas-vindas

def abrir_menu_jogo():
    janela_inicial.withdraw()  # esconde em vez de destruir

    menu = tk.Toplevel()
    menu.title("The Floor - Menu")
    menu.geometry("400x420")
    menu.configure(bg="black")

    tk.Label(
        menu,
        text="THE FLOOR",
        font=("Impact", 30),
        fg="blue",
        bg="black",
    ).pack(pady=20)

    tk.Button(menu, text="Novo Jogo",       font=("Impact", 12), width=20, command=iniciar_jogo).pack(pady=6)
    tk.Button(menu, text="Carregar Jogo",   font=("Impact", 12), width=20, command=carregar_jogo).pack(pady=6)
    tk.Button(menu, text="Ver Tabuleiro",   font=("Impact", 12), width=20, command=abrir_tabuleiro).pack(pady=6)
    tk.Button(menu, text="Estatísticas",    font=("Impact", 12), width=20, command=abrir_janela_graficos).pack(pady=6)
    tk.Button(menu, text="Gerir Jogadores", font=("Impact", 12), width=20, command=menu_jogadores).pack(pady=6)
    tk.Button(menu, text="Gerir Perguntas", font=("Impact", 12), width=20, command=menu_categorias_perguntas).pack(pady=6)
    tk.Button(menu, text="Sair",            font=("Impact", 12), width=20, command=janela_inicial.destroy).pack(pady=6)


def sair():
    janela_inicial.destroy()


# Janela inicial

janela_inicial = tk.Tk()
janela_inicial.title("The Floor")
janela_inicial.geometry("400x300")
janela_inicial.configure(bg="black")

tk.Label(
    janela_inicial,
    text="THE FLOOR",
    font=("Impact", 28),
    fg="blue",
    bg="black",
).pack(pady=40)

tk.Label(
    janela_inicial,
    text="Queres começar o jogo?",
    font=("Impact", 13),
    fg="blue",
    bg="black",
).pack(pady=10)

tk.Button(
    janela_inicial,
    text="Começar Jogo",
    font=("Impact", 12),
    width=20,
    command=abrir_menu_jogo,
).pack(pady=10)

tk.Button(
    janela_inicial,
    text="Sair",
    font=("Impact", 12),
    width=20,
    command=sair,
).pack(pady=5)

janela_inicial.mainloop()

