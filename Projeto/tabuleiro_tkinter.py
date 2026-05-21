# tabuleiro_tkinter.py
# Visualização gráfica do tabuleiro The Floor em Tkinter

import tkinter as tk
import json
import os

FICHEIRO_JOGADORES = "jogadores.json"

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


def _carregar_jogadores():
    if not os.path.exists(FICHEIRO_JOGADORES):
        return []
    try:
        with open(FICHEIRO_JOGADORES, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _construir_mapa_cores(jogadores):
    # Cada jogador recebe sempre a mesma cor baseada na sua posição na lista original
    return {j["nome"]: PALETA[i % len(PALETA)] for i, j in enumerate(jogadores)}


def _construir_grelha(jogadores):
    grelha = [[None] * 10 for _ in range(10)]
    for jogador in jogadores:
        for quad in jogador.get("quadriculas", []):
            linha, coluna = quad[0], quad[1]
            if 0 <= linha < 10 and 0 <= coluna < 10:
                grelha[linha][coluna] = jogador["nome"]
    return grelha


# Classe JanelaTabuleiro

class JanelaTabuleiro:
    """
    Janela do tabuleiro reutilizável. Pode ser aberta standalone (botão do menu)
    ou mantida aberta durante um jogo. O método atualizar() relê o ficheiro e
    redesenha tudo sem abrir uma janela nova.
    """

    def __init__(self, root=None, titulo="The Floor - Tabuleiro"):
        self.janela = tk.Toplevel(root) if root else tk.Toplevel()
        self.janela.title(titulo)
        self.janela.configure(bg="#0a0a0a")
        self.janela.resizable(False, False)

        self.TAM = 58

        jogadores = _carregar_jogadores()
        self.mapa_cores = _construir_mapa_cores(jogadores)

        self._construir_ui(jogadores)

    def _construir_ui(self, jogadores):
        janela = self.janela

        tk.Label(janela, text="THE FLOOR — TABULEIRO",
                 font=("Impact", 22), fg="#4fc3f7", bg="#0a0a0a",
                 ).grid(row=0, column=0, columnspan=12, pady=(12, 4))

        frame_grelha = tk.Frame(janela, bg="#0a0a0a")
        frame_grelha.grid(row=1, column=0, padx=10, pady=6)

        self.celulas = {}
        grelha = _construir_grelha(jogadores)

        for i in range(10):
            for j in range(10):
                nome = grelha[i][j]
                cor = self.mapa_cores.get(nome, "#1a1a2e") if nome else "#1a1a2e"

                frame_cel = tk.Frame(
                    frame_grelha, width=self.TAM, height=self.TAM,
                    bg=cor, highlightbackground="#0a0a0a", highlightthickness=1,
                )
                frame_cel.grid(row=i, column=j, padx=1, pady=1)
                frame_cel.pack_propagate(False)

                lbl = tk.Label(frame_cel, text=self._iniciais(nome),
                               font=("Impact", 11), fg="white", bg=cor)
                lbl.pack(expand=True)

                self.celulas[(i, j)] = (frame_cel, lbl)

        # Painel lateral com ranking dos jogadores ativos
        self.frame_lateral = tk.Frame(janela, bg="#0a0a0a")
        self.frame_lateral.grid(row=1, column=10, padx=(4, 10), pady=6, sticky="n")

        tk.Label(self.frame_lateral, text="JOGADORES",
                 font=("Impact", 13), fg="#4fc3f7", bg="#0a0a0a").pack(pady=(0, 4))

        self.frame_ranking = tk.Frame(self.frame_lateral, bg="#0a0a0a")
        self.frame_ranking.pack()

        self.rodape_label = tk.Label(janela, text="",
                                     font=("Courier", 11), fg="#888888", bg="#0a0a0a")
        self.rodape_label.grid(row=2, column=0, columnspan=12, pady=(0, 6))

        tk.Button(janela, text="↻  Atualizar",
                  font=("Impact", 12), fg="white", bg="#1565c0",
                  activebackground="#0d47a1", relief="flat", padx=10,
                  command=self.atualizar,
                  ).grid(row=3, column=0, columnspan=12, pady=(0, 10))

        self._atualizar_painel(jogadores)

    @staticmethod
    def _iniciais(nome):
        if not nome:
            return ""
        partes = nome.split()
        return partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")

    def atualizar(self):
        """Relê jogadores.json e redesenha a grelha e o painel lateral."""
        jogadores = _carregar_jogadores()

        # Garante que jogadores novos também recebem uma cor
        for i, j in enumerate(jogadores):
            if j["nome"] not in self.mapa_cores:
                self.mapa_cores[j["nome"]] = PALETA[i % len(PALETA)]

        grelha = _construir_grelha(jogadores)

        for i in range(10):
            for j in range(10):
                nome = grelha[i][j]
                cor = self.mapa_cores.get(nome, "#1a1a2e") if nome else "#1a1a2e"
                frame_cel, lbl = self.celulas[(i, j)]
                frame_cel.configure(bg=cor)
                lbl.configure(bg=cor, text=self._iniciais(nome))

        self._atualizar_painel(jogadores)

    def _atualizar_painel(self, jogadores):
        for widget in self.frame_ranking.winfo_children():
            widget.destroy()

        contagem = {
            j["nome"]: len(j.get("quadriculas", []))
            for j in jogadores
            if len(j.get("quadriculas", [])) > 0
        }
        ranking = sorted(contagem.items(), key=lambda x: x[1], reverse=True)

        for nome, n in ranking[:20]:
            cor = self.mapa_cores.get(nome, "#888")
            frame_linha = tk.Frame(self.frame_ranking, bg="#0a0a0a")
            frame_linha.pack(anchor="w", pady=1)
            tk.Label(frame_linha, text="■", font=("Arial", 10),
                     fg=cor, bg="#0a0a0a").pack(side="left")
            nome_curto = nome if len(nome) <= 14 else nome[:13] + "…"
            tk.Label(frame_linha, text=f" {nome_curto} ({n})",
                     font=("Courier", 10), fg="#cccccc", bg="#0a0a0a").pack(side="left")

        ativos = len([j for j in jogadores if len(j.get("quadriculas", [])) > 0])
        eliminados = len(jogadores) - ativos
        self.rodape_label.configure(
            text=f"Ativos: {ativos}   |   Eliminados: {eliminados}")

    def fechar(self):
        try:
            self.janela.destroy()
        except Exception:
            pass

    def esta_aberto(self):
        try:
            return self.janela.winfo_exists()
        except Exception:
            return False


# Função pública mantida para compatibilidade com o menu

def abrir_tabuleiro(root=None):
    return JanelaTabuleiro(root=root)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    raiz = tk.Tk()
    raiz.withdraw()
    abrir_tabuleiro(raiz)
    raiz.mainloop()