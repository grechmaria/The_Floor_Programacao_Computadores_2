# tabuleiro_tkinter.py
# Visualização gráfica do tabuleiro The Floor em Tkinter
# Grelha 10x10 com cores por jogador, atualiza em tempo real

import tkinter as tk
import json
import os
import random

FICHEIRO_JOGADORES = "jogadores.json"

# Paleta de cores para os jogadores (até 100 cores distintas)
PALETA = [
    "#e63946", "#457b9d", "#2a9d8f", "#e9c46a", "#f4a261",
    "#264653", "#8ecae6", "#a8dadc", "#606c38", "#dda15e",
    "#bc6c25", "#023047", "#ffb703", "#fb8500", "#6a4c93",
    "#1982c4", "#8ac926", "#ff595e", "#ffca3a", "#6a994e",
    "#a7c957", "#386641", "#bc4749", "#f2e8cf", "#90be6d",
    "#f9c74f", "#f8961e", "#f3722c", "#f94144", "#43aa8b",
    "#4d908e", "#577590", "#277da1", "#b5838d", "#6d6875",
    "#e07a5f", "#3d405b", "#81b29a", "#f2cc8f", "#118ab2",
    "#06d6a0", "#ffd166", "#ef476f", "#073b4c", "#cbf3f0",
    "#2ec4b6", "#e71d36", "#ff9f1c", "#011627", "#fdfffc",
    "#a8c686", "#669bbc", "#c1121f", "#fdf0d5", "#003049",
    "#fcbf49", "#eae2b7", "#d62828", "#f77f00", "#023e8a",
    "#0096c7", "#00b4d8", "#48cae4", "#90e0ef", "#ade8f4",
    "#caf0f8", "#7b2d8b", "#ff6b6b", "#feca57", "#48dbfb",
    "#ff9ff3", "#54a0ff", "#5f27cd", "#341f97", "#ee5a24",
    "#009432", "#0652dd", "#9980fa", "#833471", "#fd79a8",
    "#d63031", "#e17055", "#fdcb6e", "#00b894", "#00cec9",
    "#6c5ce7", "#a29bfe", "#fab1a0", "#74b9ff", "#81ecec",
    "#55efc4", "#636e72", "#2d3436", "#b2bec3", "#dfe6e9",
    "#f8b500", "#c44569", "#40407a", "#218c74", "#84817a",
]


def carregar_jogadores():
    if not os.path.exists(FICHEIRO_JOGADORES):
        return []
    try:
        with open(FICHEIRO_JOGADORES, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def construir_mapa_cores(jogadores):
    """Associa uma cor a cada jogador."""
    mapa = {}
    for i, jogador in enumerate(jogadores):
        mapa[jogador["nome"]] = PALETA[i % len(PALETA)]
    return mapa


def construir_grelha(jogadores):
    """Reconstrói a grelha 10x10 a partir das quadrículas dos jogadores."""
    grelha = [[None for _ in range(10)] for _ in range(10)]
    for jogador in jogadores:
        for quad in jogador.get("quadriculas", []):
            linha, coluna = quad[0], quad[1]
            if 0 <= linha < 10 and 0 <= coluna < 10:
                grelha[linha][coluna] = jogador["nome"]
    return grelha


def abrir_tabuleiro():
    """Abre a janela do tabuleiro gráfico."""
    janela = tk.Toplevel()
    janela.title("The Floor - Tabuleiro")
    janela.configure(bg="#0a0a0a")
    janela.resizable(False, False)

    jogadores = carregar_jogadores()
    mapa_cores = construir_mapa_cores(jogadores)
    grelha = construir_grelha(jogadores)

    # Contar quadrículas por jogador para o painel lateral
    contagem = {}
    for jogador in jogadores:
        n = len(jogador.get("quadriculas", []))
        if n > 0:
            contagem[jogador["nome"]] = n

    TAM = 52  # tamanho de cada célula em pixels

    # --- Título ---
    tk.Label(
        janela,
        text="THE FLOOR",
        font=("Impact", 22),
        fg="#4fc3f7",
        bg="#0a0a0a",
    ).grid(row=0, column=0, columnspan=11, pady=(12, 4))

    # --- Grelha 10x10 ---
    frame_grelha = tk.Frame(janela, bg="#0a0a0a")
    frame_grelha.grid(row=1, column=0, padx=12, pady=8)

    celulas = {}
    for i in range(10):
        for j in range(10):
            nome = grelha[i][j]
            cor = mapa_cores.get(nome, "#1a1a2e") if nome else "#1a1a2e"
            texto = ""
            if nome:
                # Mostra as iniciais do jogador
                partes = nome.split()
                texto = partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")

            frame_cel = tk.Frame(
                frame_grelha,
                width=TAM,
                height=TAM,
                bg=cor,
                highlightbackground="#0a0a0a",
                highlightthickness=1,
            )
            frame_cel.grid(row=i, column=j, padx=1, pady=1)
            frame_cel.pack_propagate(False)

            tk.Label(
                frame_cel,
                text=texto,
                font=("Impact", 11),
                fg="white",
                bg=cor,
            ).pack(expand=True)

            celulas[(i, j)] = (frame_cel, cor, nome)

    # --- Painel lateral: jogadores ativos ---
    frame_lateral = tk.Frame(janela, bg="#0a0a0a")
    frame_lateral.grid(row=1, column=10, padx=(4, 12), pady=8, sticky="n")

    tk.Label(
        frame_lateral,
        text="JOGADORES",
        font=("Impact", 13),
        fg="#4fc3f7",
        bg="#0a0a0a",
    ).pack(pady=(0, 6))

    # Ordena por número de quadrículas (maior primeiro)
    ranking = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
    for nome, n in ranking[:20]:  # mostra os top 20
        cor = mapa_cores.get(nome, "#888")
        frame_linha = tk.Frame(frame_lateral, bg="#0a0a0a")
        frame_linha.pack(anchor="w", pady=1)

        tk.Label(
            frame_linha,
            text="■",
            font=("Arial", 10),
            fg=cor,
            bg="#0a0a0a",
        ).pack(side="left")

        nome_curto = nome if len(nome) <= 16 else nome[:14] + "…"
        tk.Label(
            frame_linha,
            text=f" {nome_curto} ({n})",
            font=("Courier", 9),
            fg="#cccccc",
            bg="#0a0a0a",
        ).pack(side="left")

    # --- Rodapé com estatísticas rápidas ---
    ativos = len([j for j in jogadores if len(j.get("quadriculas", [])) > 0])
    eliminados = len(jogadores) - ativos

    rodape_label = tk.Label(
        janela,
        text=f"Jogadores ativos: {ativos}   |   Eliminados: {eliminados}",
        font=("Courier", 10),
        fg="#888888",
        bg="#0a0a0a",
    )
    rodape_label.grid(row=2, column=0, columnspan=11, pady=(0, 10))

    # --- Botão atualizar ---
    def atualizar():
        jogadores_novos = carregar_jogadores()
        mapa_cores_novo = construir_mapa_cores(jogadores_novos)
        grelha_nova = construir_grelha(jogadores_novos)

        for i in range(10):
            for j in range(10):
                nome = grelha_nova[i][j]
                cor = mapa_cores_novo.get(nome, "#1a1a2e") if nome else "#1a1a2e"
                texto = ""
                if nome:
                    partes = nome.split()
                    texto = partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")
                frame_cel, _, _ = celulas[(i, j)]
                frame_cel.configure(bg=cor)
                for widget in frame_cel.winfo_children():
                    widget.configure(bg=cor, text=texto)

        # Atualizar rodapé
        ativos = len([j for j in jogadores_novos if len(j.get("quadriculas", [])) > 0])
        eliminados = len(jogadores_novos) - ativos
        rodape_label.configure(text=f"Jogadores ativos: {ativos}   |   Eliminados: {eliminados}")

    tk.Button(
        janela,
        text="↻  Atualizar Tabuleiro",
        font=("Impact", 11),
        fg="white",
        bg="#1565c0",
        activebackground="#0d47a1",
        relief="flat",
        padx=10,
        command=atualizar,
    ).grid(row=3, column=0, columnspan=11, pady=(0, 12))


# Permite testar isoladamente
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    raiz = tk.Tk()
    raiz.withdraw()
    abrir_tabuleiro()
    raiz.mainloop()