# graficos_the_floor.py
# Janela de estatísticas/gráficos para o Tkinter.
# Em vez de duplicar o código de gráficos, este módulo chama diretamente
# as funções já definidas em estatisticas.py.

import tkinter as tk
from tkinter import messagebox

from estatisticas import (
    carregar_jogadores,
    carregar_duelos,
    # funções numéricas
    tempo_medio_resposta,
    media_duelos_regressos,
    estatisticas_jogador,
    jogador_mais_rapido,
    jogador_mais_agressivo,
    resumo_duelos,
    # funções de gráfico
    grafico_duelos_ganhos_perdidos,
    grafico_tempo_medio_por_jogador,
    grafico_circular_vitorias,
    grafico_agressividade,
    grafico_circular_taxa_acerto,
    grafico_duelos_por_categoria,
)


# Funções auxiliares para chamar os gráficos a partir do Tkinter.
# Carregam os dados frescos do ficheiro antes de cada gráfico,
# para que os valores reflitam sempre o estado atual do jogo.

def _grafico_duelos():
    jogadores = carregar_jogadores()
    if not any(j.get("duelos_iniciados", 0) > 0 for j in jogadores):
        messagebox.showinfo("Sem dados", "Ainda não existem duelos registados.")
        return
    grafico_duelos_ganhos_perdidos(jogadores)


def _grafico_tempo():
    jogadores = carregar_jogadores()
    if not any(j.get("tempos_resposta") for j in jogadores):
        messagebox.showinfo("Sem dados", "Ainda não existem tempos de resposta registados.")
        return
    grafico_tempo_medio_por_jogador(jogadores)


def _grafico_vitorias():
    jogadores = carregar_jogadores()
    if not any(j.get("duelos_ganhos", 0) > 0 for j in jogadores):
        messagebox.showinfo("Sem dados", "Ainda não existem vitórias registadas.")
        return
    grafico_circular_vitorias(jogadores)


def _grafico_agressividade():
    jogadores = carregar_jogadores()
    if not any(j.get("duelos_iniciados", 0) > 0 for j in jogadores):
        messagebox.showinfo("Sem dados", "Ainda não existem dados de agressividade.")
        return
    grafico_agressividade(jogadores)


def _grafico_taxa_acerto():
    jogadores = carregar_jogadores()
    if not any(j.get("perguntas_respondidas", 0) > 0 for j in jogadores):
        messagebox.showinfo("Sem dados", "Ainda não existem perguntas respondidas.")
        return
    grafico_circular_taxa_acerto(jogadores)


def _grafico_categorias():
    duelos = carregar_duelos()
    duelos_reais = [d for d in duelos if d.get("id_duelo", 0) != 0]
    if not duelos_reais:
        messagebox.showinfo("Sem dados", "Ainda não existem duelos com categoria registada.")
        return
    grafico_duelos_por_categoria(duelos_reais)


# Janela de estatísticas com botões para cada gráfico

def abrir_janela_graficos():
    janela = tk.Toplevel()
    janela.title("The Floor - Estatísticas")
    janela.geometry("420x460")
    janela.configure(bg="black")

    tk.Label(
        janela,
        text="ESTATÍSTICAS",
        font=("Impact", 26),
        fg="blue",
        bg="black",
    ).pack(pady=18)

    # Cada tuplo: (texto do botão, função a chamar)
    botoes = [
        ("Duelos ganhos / perdidos",      _grafico_duelos),
        ("Tempo médio por jogador",        _grafico_tempo),
        ("Vitórias — gráfico circular",    _grafico_vitorias),
        ("Agressividade",                  _grafico_agressividade),
        ("Taxa de acerto global",          _grafico_taxa_acerto),
        ("Duelos por categoria",           _grafico_categorias),
    ]

    for texto, comando in botoes:
        tk.Button(
            janela,
            text=texto,
            font=("Impact", 11),
            width=30,
            command=comando,
        ).pack(pady=5)

    tk.Button(
        janela,
        text="Fechar",
        font=("Impact", 11),
        width=30,
        command=janela.destroy,
    ).pack(pady=14)


# Permite testar este ficheiro isoladamente
if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.withdraw()
    abrir_janela_graficos()
    raiz.mainloop()