# duelos_tkinter.py
# Versão gráfica (Tkinter) da dinâmica de jogo The Floor.
# Substitui todas as interações shell de duelos.py por janelas Tkinter.

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import random
import time
import threading

# importações do projeto 
from gestao_jogadores import carregar_jogadores, guardar_jogadores
from duelos import (
    carregar_duelos,
    guardar_duelos,
    carregar_perguntas,
    sortear_perguntas_categoria,
    inicializar_tabuleiro,
    atualizar_tabuleiro,
    transferir_quadricula,
    verificar_fim_jogo,
    _atualizar_estatisticas,
)

DURACAO_DUELO = 45  # segundos


 
#  UTILITÁRIOS DE ESTILO

CORES = {
    "bg":       "#0d1b2a",
    "painel":   "#1b2a3b",
    "accent":   "#1976d2",
    "accent2":  "#1565c0",
    "texto":    "#ffffff",
    "titulo":   "#ffd600",
    "verde":    "#43a047",
    "vermelho": "#e53935",
    "amarelo":  "#ffd600",
    "cinza":    "#546e7a",
}

def _estilo_janela(janela, titulo, largura=480, altura=360):
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")
    janela.configure(bg=CORES["bg"])
    janela.resizable(False, False)

def _btn(pai, texto, comando, cor=None, largura=22, fonte_tam=11):
    cor = cor or CORES["accent"]
    return tk.Button(
        pai, text=texto, command=comando,
        font=("Impact", fonte_tam), width=largura,
        bg=cor, fg="white", relief="flat",
        activebackground=CORES["accent2"], activeforeground="white",
        cursor="hand2",
    )

def _label(pai, texto, cor=None, tam=11, bold=False):
    peso = "bold" if bold else "normal"
    cor = cor or CORES["texto"]
    return tk.Label(pai, text=texto, font=("Courier", tam, peso),
                    fg=cor, bg=CORES["bg"], wraplength=440)

def _titulo(pai, texto, tam=20):
    return tk.Label(pai, text=texto, font=("Impact", tam),
                    fg=CORES["titulo"], bg=CORES["bg"])



#  1. SELEÇÃO DE VIZINHO

def _obter_vizinhos(jogador, jogadores):
    vizinhos = []
    for (linha, coluna) in jogador["quadriculas"]:
        posicoes = [
            (linha - 1, coluna), (linha + 1, coluna),
            (linha, coluna - 1), (linha, coluna + 1),
        ]
        for outro in jogadores:
            if outro["nome"] == jogador["nome"]:
                continue
            for quad in outro["quadriculas"]:
                if list(quad) in [list(p) for p in posicoes]:
                    if outro not in vizinhos:
                        vizinhos.append(outro)
    return vizinhos


def selecionar_vizinho_tkinter(desafiante, jogadores):
    """Abre janela para o desafiante escolher um vizinho. Devolve o vizinho ou None."""
    vizinhos = _obter_vizinhos(desafiante, jogadores)
    if not vizinhos:
        messagebox.showinfo("Sem Vizinhos",
                            f"{desafiante['nome']} não tem vizinhos disponíveis.")
        return None

    resultado = [None]

    altura = max(280, 140 + len(vizinhos) * 54)
    janela = tk.Toplevel()
    _estilo_janela(janela, "Escolher Vizinho", 520, altura)
    janela.grab_set()

    _titulo(janela, "ESCOLHER VIZINHO").pack(pady=(14, 2))
    _label(janela, f"Jogador: {desafiante['nome']}", cor=CORES["amarelo"], tam=10).pack()
    _label(janela, "Escolhe quem desafias:", tam=10).pack(pady=(6, 4))

    frame = tk.Frame(janela, bg=CORES["bg"])
    frame.pack(pady=4)

    def escolher(v):
        resultado[0] = v
        janela.destroy()

    for viz in vizinhos:
        texto = f"{viz['nome']}  [{viz['categoria']}]"
        _btn(frame, texto, lambda v=viz: escolher(v), largura=36).pack(pady=3)

    janela.wait_window()
    return resultado[0]


#  2. DUELO — janela principal com cronómetro e perguntas

def _janela_duelo(perguntas_duelo, categoria, desafiante, desafiado):
    """
    Corre o duelo de 45 s em Tkinter.
    Devolve (vencedor_nome, tempos_dict, acertos_dict).
    """
    pontos  = {desafiante["nome"]: 0,  desafiado["nome"]: 0}
    tempos  = {desafiante["nome"]: [], desafiado["nome"]: []}
    acertos = {desafiante["nome"]: 0,  desafiado["nome"]: 0}

    resultado = [None]   # guardará o vencedor quando a janela fechar

    #  janela 
    janela = tk.Toplevel()
    _estilo_janela(janela, "DUELO", 520, 520)
    janela.grab_set()

    # Título
    _titulo(janela, "THE FLOOR — DUELO", 18).pack(pady=(10, 0))
    lbl_vs = _label(janela,
                    f"{desafiante['nome']}  vs  {desafiado['nome']}",
                    cor=CORES["amarelo"], tam=12, bold=True)
    lbl_vs.pack()
    _label(janela, f"Categoria: {categoria}", cor=CORES["titulo"], tam=10).pack()

    # Cronómetro
    frame_crono = tk.Frame(janela, bg=CORES["bg"])
    frame_crono.pack(pady=4)
    lbl_crono = tk.Label(frame_crono, text="45", font=("Impact", 28),
                         fg=CORES["amarelo"], bg=CORES["bg"], width=4)
    lbl_crono.pack()

    # Placar
    lbl_placar = _label(janela,
                        f"{desafiante['nome']}: 0  |  {desafiado['nome']}: 0",
                        cor=CORES["verde"], tam=11, bold=True)
    lbl_placar.pack(pady=2)

    # Área de pergunta
    frame_pergunta = tk.Frame(janela, bg=CORES["painel"], padx=12, pady=10)
    frame_pergunta.pack(fill="x", padx=20, pady=6)

    lbl_vez = _label(frame_pergunta, "", cor=CORES["titulo"], tam=10, bold=True)
    lbl_vez.configure(bg=CORES["painel"])
    lbl_vez.pack()

    lbl_pergunta = tk.Label(frame_pergunta, text="", font=("Courier", 11),
                            fg=CORES["texto"], bg=CORES["painel"],
                            wraplength=460, justify="left")
    lbl_pergunta.pack(pady=(4, 2))

    # Entrada de resposta
    frame_entrada = tk.Frame(janela, bg=CORES["bg"])
    frame_entrada.pack(pady=4)

    entrada_var = tk.StringVar()
    entrada = tk.Entry(frame_entrada, textvariable=entrada_var,
                       font=("Courier", 13), width=28,
                       bg="#1b2a3b", fg="#ffffff", insertbackground="#ffd600",
                       relief="flat", bd=4)
    entrada.pack(side="left", padx=(0, 8))

    btn_responder = _btn(frame_entrada, "Responder", lambda: None,
                         cor=CORES["verde"], largura=12, fonte_tam=10)
    btn_responder.pack(side="left")

    # Feedback
    lbl_feedback = _label(janela, "", tam=10)
    lbl_feedback.pack(pady=2)

    #  estado interno 
    estado = {
        "idx_pergunta":   0,
        "vez":            0,   # 0 = desafiante, 1 = desafiado
        "inicio_resp":    0.0,
        "aguardando":     False,
        "inicio_duelo":   time.time(),
        "encerrado":      False,
    }

    jogadores_duelo = [desafiante, desafiado]

    def atualizar_crono():
        if estado["encerrado"]:
            return
        restante = max(0, DURACAO_DUELO - int(time.time() - estado["inicio_duelo"]))
        lbl_crono.config(text=str(restante),
                         fg=CORES["vermelho"] if restante <= 10 else CORES["amarelo"])
        if restante == 0:
            encerrar_duelo()
        else:
            janela.after(1000, atualizar_crono)

    def mostrar_proxima_pergunta():
        if estado["encerrado"]:
            return
        restante = DURACAO_DUELO - int(time.time() - estado["inicio_duelo"])
        if restante <= 0:
            encerrar_duelo()
            return
        if estado["idx_pergunta"] >= len(perguntas_duelo):
            encerrar_duelo()
            return

        pergunta = perguntas_duelo[estado["idx_pergunta"]]
        jogador_atual = jogadores_duelo[estado["vez"]]

        lbl_vez.config(text=f"► {jogador_atual['nome']}")
        lbl_pergunta.config(text=pergunta["pergunta"])
        lbl_feedback.config(text="", fg=CORES["texto"])
        entrada_var.set("")
        entrada.config(state="normal")
        entrada.focus_set()
        estado["inicio_resp"] = time.time()
        estado["aguardando"] = True

    def submeter_resposta():
        if not estado["aguardando"] or estado["encerrado"]:
            return

        pergunta = perguntas_duelo[estado["idx_pergunta"]]
        jogador_atual = jogadores_duelo[estado["vez"]]
        resposta = entrada_var.get().strip().lower()
        tempo_resp = round(time.time() - estado["inicio_resp"], 2)

        correta = resposta == pergunta["resposta"].strip().lower()

        if correta:
            pontos[jogador_atual["nome"]] += 1
            acertos[jogador_atual["nome"]] += 1
            lbl_feedback.config(
                text=f"✔ Correto! ({tempo_resp}s)", fg=CORES["verde"])
        else:
            lbl_feedback.config(
                text=f"✘ Errado! Resposta: {pergunta['resposta']} ({tempo_resp}s)",
                fg=CORES["vermelho"])

        tempos[jogador_atual["nome"]].append(tempo_resp)
        entrada.config(state="disabled")
        estado["aguardando"] = False

        # Atualizar placar
        lbl_placar.config(
            text=(f"{desafiante['nome']}: {pontos[desafiante['nome']]}  |  "
                  f"{desafiado['nome']}: {pontos[desafiado['nome']]}"))

        # Avançar: alterna entre desafiante(0) e desafiado(1)
        if estado["vez"] == 0:
            estado["vez"] = 1
            estado["idx_pergunta"] += 1
            janela.after(1200, mostrar_proxima_pergunta)
        else:
            estado["vez"] = 0
            estado["idx_pergunta"] += 1
            janela.after(1200, mostrar_proxima_pergunta)

    btn_responder.config(command=submeter_resposta)
    entrada.bind("<Return>", lambda e: submeter_resposta())

    def encerrar_duelo():
        if estado["encerrado"]:
            return
        estado["encerrado"] = True
        entrada.config(state="disabled")
        btn_responder.config(state="disabled")

        # Determinar vencedor
        p_des = pontos[desafiante["nome"]]
        p_def = pontos[desafiado["nome"]]

        if p_des > p_def:
            vencedor = desafiante["nome"]
            motivo = "mais respostas certas"
        elif p_def > p_des:
            vencedor = desafiado["nome"]
            motivo = "mais respostas certas"
        else:
            # Desempate por tempo médio
            t_des = (sum(tempos[desafiante["nome"]]) / len(tempos[desafiante["nome"]])
                     if tempos[desafiante["nome"]] else float("inf"))
            t_def = (sum(tempos[desafiado["nome"]]) / len(tempos[desafiado["nome"]])
                     if tempos[desafiado["nome"]] else float("inf"))
            vencedor = desafiante["nome"] if t_des <= t_def else desafiado["nome"]
            motivo = "tempo médio mais rápido"

        resultado[0] = vencedor

        # Janela de resultado
        _janela_resultado(desafiante, desafiado, pontos, tempos, vencedor, motivo,
                          on_close=janela.destroy)

    # Iniciar cronómetro e primeira pergunta
    janela.after(500, atualizar_crono)
    janela.after(300, mostrar_proxima_pergunta)

    janela.wait_window()
    return resultado[0], tempos, acertos


#  3. JANELA DE RESULTADO


def _janela_resultado(desafiante, desafiado, pontos, tempos, vencedor, motivo, on_close):
    jan = tk.Toplevel()
    _estilo_janela(jan, "Resultado do Duelo", 420, 400)
    jan.grab_set()

    _titulo(jan, "RESULTADO FINAL", 20).pack(pady=(18, 4))

    cor_des = CORES["verde"] if vencedor == desafiante["nome"] else CORES["vermelho"]
    cor_def = CORES["verde"] if vencedor == desafiado["nome"]  else CORES["vermelho"]

    t_des = (round(sum(tempos[desafiante["nome"]]) / len(tempos[desafiante["nome"]]), 2)
             if tempos[desafiante["nome"]] else 0)
    t_def = (round(sum(tempos[desafiado["nome"]]) / len(tempos[desafiado["nome"]]), 2)
             if tempos[desafiado["nome"]] else 0)

    _label(jan, f"{desafiante['nome']}", cor=cor_des, tam=12, bold=True).pack()
    _label(jan, f"{pontos[desafiante['nome']]} acertos  |  {t_des}s médio",
           cor=cor_des, tam=10).pack()

    _label(jan, "vs", cor=CORES["cinza"], tam=10).pack(pady=4)

    _label(jan, f"{desafiado['nome']}", cor=cor_def, tam=12, bold=True).pack()
    _label(jan, f"{pontos[desafiado['nome']]} acertos  |  {t_def}s médio",
           cor=cor_def, tam=10).pack()

    tk.Label(jan, text=f"🏆  {vencedor}  ganhou!",
             font=("Impact", 16), fg=CORES["amarelo"], bg=CORES["bg"]).pack(pady=(14, 2))
    _label(jan, f"({motivo})", cor=CORES["cinza"], tam=9).pack()

    _btn(jan, "Continuar", lambda: (jan.destroy(), on_close()),
         cor=CORES["accent"], largura=18).pack(pady=14)

    jan.wait_window()


#  4. PRÓXIMO DESAFIANTE


def escolher_proximo_desafiante_tkinter(vencedor_nome, jogadores):
    """Popup: vencedor fica ou sorteia outro?"""
    resultado = [None]

    jan = tk.Toplevel()
    _estilo_janela(jan, "Próximo Duelo", 400, 300)
    jan.grab_set()

    _titulo(jan, "PRÓXIMO DUELO", 16).pack(pady=(16, 4))
    _label(jan, f"{vencedor_nome} venceu!", cor=CORES["amarelo"], tam=11, bold=True).pack()
    _label(jan, "O vencedor quer continuar a jogar?", tam=10).pack(pady=6)

    frame = tk.Frame(jan, bg=CORES["bg"])
    frame.pack(pady=6)

    def ficar():
        for j in jogadores:
            if j["nome"] == vencedor_nome:
                j["regressos_grelha"] = j.get("regressos_grelha", 0) + 1
                resultado[0] = j
                break
        jan.destroy()

    def sortear():
        outros = [j for j in jogadores
                  if j["nome"] != vencedor_nome and len(j.get("quadriculas", [])) > 0]
        resultado[0] = random.choice(outros) if outros else None
        jan.destroy()

    _btn(frame, f"✔  {vencedor_nome} continua", ficar,
         cor=CORES["verde"], largura=28).pack(pady=4)
    _btn(frame, "🎲  Sortear outro jogador", sortear,
         cor=CORES["cinza"], largura=28).pack(pady=4)

    jan.wait_window()
    return resultado[0]


#  5. EXECUTAR DUELO (equivalente a duelos.executar_duelo)


def executar_duelo_tkinter(desafiante, desafiado, jogadores, duelos):
    categoria = desafiado["categoria"]
    desafiado["duelos_aceites"] = desafiado.get("duelos_aceites", 0) + 1

    todas_perguntas = carregar_perguntas()
    perguntas_duelo = sortear_perguntas_categoria(todas_perguntas, categoria, n=20)

    if not perguntas_duelo:
        messagebox.showerror("Sem Perguntas",
                             f"Não há perguntas na categoria '{categoria}'.")
        return None

    vencedor, tempos, acertos = _janela_duelo(
        perguntas_duelo, categoria, desafiante, desafiado)

    if vencedor is None:
        return None

    quadriculas_transferidas = []
    if vencedor == desafiante["nome"]:
        quadriculas_transferidas = transferir_quadricula(desafiante, desafiado, jogadores)
    else:
        messagebox.showinfo("Defesa",
                            f"{desafiado['nome']} defendeu com sucesso!")

    guardar_jogadores(jogadores)

    t_des = (round(sum(tempos[desafiante["nome"]]) / len(tempos[desafiante["nome"]]), 2)
             if tempos[desafiante["nome"]] else 0)
    t_def = (round(sum(tempos[desafiado["nome"]]) / len(tempos[desafiado["nome"]]), 2)
             if tempos[desafiado["nome"]] else 0)

    duelo = {
        "id_duelo":                 len(duelos) + 1,
        "desafiante":               desafiante["nome"],
        "desafiado":                desafiado["nome"],
        "categoria":                categoria,
        "acertos_desafiante":       acertos[desafiante["nome"]],
        "tempo_medio_desafiante":   t_des,
        "acertos_desafiado":        acertos[desafiado["nome"]],
        "tempo_medio_desafiado":    t_def,
        "vencedor":                 vencedor,
        "quadriculas_transferidas": quadriculas_transferidas,
    }
    duelos.append(duelo)
    guardar_duelos(duelos)

    # Atualizar estatísticas
    _atualizar_estatisticas(desafiante, t_des, vencedor,
                            len(tempos[desafiante["nome"]]),
                            acertos[desafiante["nome"]], categoria)
    _atualizar_estatisticas(desafiado, t_def, vencedor,
                            len(tempos[desafiado["nome"]]),
                            acertos[desafiado["nome"]], categoria)

    return duelo


#  6. LOOP PRINCIPAL DO JOGO EM TKINTER


def _verificar_fim_tkinter(jogadores):
    ativos = [j for j in jogadores if len(j.get("quadriculas", [])) > 0]
    if len(ativos) == 1:
        messagebox.showinfo("Fim de Jogo! 🏆",
                            f"O vencedor é {ativos[0]['nome']}!")
        return True
    return False


def _janela_entre_duelos(desafiante_nome, jogadores, duelos,
                          proximo_cb, pausar_cb):
    """
    Janela mostrada entre duelos: tabuleiro resumido + botões Continuar / Pausar.
    proximo_cb() → continua o jogo
    pausar_cb()  → guarda e sai
    """
    jan = tk.Toplevel()
    _estilo_janela(jan, "Entre Duelos", 460, 420)
    jan.grab_set()

    _titulo(jan, "THE FLOOR", 20).pack(pady=(12, 2))

    ativos = [j for j in jogadores if len(j.get("quadriculas", [])) > 0]
    _label(jan, f"Jogadores ativos: {len(ativos)}", cor=CORES["amarelo"], tam=10).pack()

    # Mini-ranking (top 8)
    ranking = sorted(ativos, key=lambda j: len(j.get("quadriculas", [])), reverse=True)
    frame_rank = tk.Frame(jan, bg=CORES["painel"], padx=10, pady=8)
    frame_rank.pack(fill="x", padx=20, pady=8)

    tk.Label(frame_rank, text="TOP JOGADORES", font=("Impact", 11),
             fg=CORES["titulo"], bg=CORES["painel"]).pack()

    for j in ranking[:8]:
        n_quads = len(j.get("quadriculas", []))
        linha = f"  {j['nome']:<22} {n_quads} quadrículas"
        tk.Label(frame_rank, text=linha, font=("Courier", 9),
                 fg=CORES["texto"], bg=CORES["painel"], anchor="w").pack(fill="x")

    _label(jan, f"Próximo desafiante: {desafiante_nome}",
           cor=CORES["verde"], tam=10, bold=True).pack(pady=4)

    frame_btn = tk.Frame(jan, bg=CORES["bg"])
    frame_btn.pack(pady=8)

    def continuar():
        jan.destroy()
        proximo_cb()

    def pausar():
        guardar_jogadores(jogadores)
        messagebox.showinfo("Jogo Pausado", "Estado guardado. Até já!")
        jan.destroy()
        pausar_cb()

    _btn(frame_btn, "▶  Próximo Duelo", continuar,
         cor=CORES["verde"], largura=24).pack(pady=4)
    _btn(frame_btn, "⏸  Pausar e Guardar", pausar,
         cor=CORES["cinza"], largura=24).pack(pady=4)

    jan.wait_window()


def iniciar_jogo_tkinter(root=None):
    """Ponto de entrada do jogo em modo Tkinter. Chama-se a partir do menu."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    jogadores = carregar_jogadores()

    if len(jogadores) < 2:
        messagebox.showerror("Erro",
                             "São necessários pelo menos 2 jogadores para iniciar o jogo.")
        return

    duelos = carregar_duelos()
    inicializar_tabuleiro(jogadores)

    proximo_desafiante = [None]   # lista para mutabilidade em closures
    jogo_ativo = [True]

    def ciclo_jogo():
        if not jogo_ativo[0]:
            return

        jogadores_atuais = carregar_jogadores()   # lê estado atualizado

        if _verificar_fim_tkinter(jogadores_atuais):
            return

        # Escolher desafiante
        if proximo_desafiante[0]:
            # encontra o mesmo objeto na lista atualizada
            nome_prox = proximo_desafiante[0]["nome"]
            desafiante = next(
                (j for j in jogadores_atuais if j["nome"] == nome_prox),
                None)
            proximo_desafiante[0] = None
        else:
            ativos = [j for j in jogadores_atuais if len(j.get("quadriculas", [])) > 0]
            desafiante = random.choice(ativos) if ativos else None

        if desafiante is None:
            return

        # Escolher vizinho
        desafiado = selecionar_vizinho_tkinter(desafiante, jogadores_atuais)
        if desafiado is None:
            ciclo_jogo()   # tenta de novo com outro jogador
            return

        # Executar duelo
        duelo = executar_duelo_tkinter(desafiante, desafiado, jogadores_atuais, duelos)
        if duelo is None:
            ciclo_jogo()
            return

        if _verificar_fim_tkinter(jogadores_atuais):
            guardar_jogadores(jogadores_atuais)
            return

        # Determinar próximo desafiante
        prox = escolher_proximo_desafiante_tkinter(duelo["vencedor"], jogadores_atuais)
        proximo_desafiante[0] = prox

        # Mostrar ecrã entre duelos
        nome_prox_str = prox["nome"] if prox else "Aleatório"
        _janela_entre_duelos(
            nome_prox_str, jogadores_atuais, duelos,
            proximo_cb=ciclo_jogo,
            pausar_cb=lambda: jogo_ativo.__setitem__(0, False),
        )

    ciclo_jogo()



#  7. CARREGAR JOGO (retomar jogo guardado) em Tkinter


def carregar_jogo_tkinter():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    jogadores = carregar_jogadores()

    if not jogadores:
        messagebox.showerror("Erro", "Não há jogadores registados.")
        return

    ativos = [j for j in jogadores if len(j.get("quadriculas", [])) > 0]
    if not ativos:
        messagebox.showinfo("Sem Jogo", "Não há jogo guardado. Inicia um novo jogo.")
        return

    messagebox.showinfo("Jogo Carregado",
                        f"Jogo retomado! {len(ativos)} jogadores ainda ativos.")
    iniciar_jogo_tkinter()


# Teste isolado
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    raiz = tk.Tk()
    raiz.withdraw()
    iniciar_jogo_tkinter(raiz)
    raiz.mainloop()
