# duelos_tkinter.py
# Versão gráfica (Tkinter) da dinâmica de jogo The Floor.

import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import time

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
from tabuleiro_tkinter import JanelaTabuleiro

DURACAO_DUELO = 45  # segundos


# Estilos e utilitários

CORES = {
    "bg":       "#0a0a0a",
    "painel":   "#111111",
    "accent":   "#1565c0",
    "accent2":  "#0d47a1",
    "texto":    "#e0e0e0",
    "titulo":   "#4fc3f7",
    "verde":    "#43a047",
    "vermelho": "#e53935",
    "amarelo":  "#fdd835",
    "cinza":    "#555555",
}

def _estilo_janela(janela, titulo, largura=600, altura=460):
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")
    janela.configure(bg=CORES["bg"])
    janela.resizable(True, True)

def _btn(pai, texto, comando, cor=None, largura=24, fonte_tam=12):
    cor = cor or CORES["accent"]
    return tk.Button(
        pai, text=texto, command=comando,
        font=("Impact", fonte_tam), width=largura,
        bg=cor, fg="white", relief="flat",
        activebackground=CORES["accent2"], activeforeground="white",
        cursor="hand2",
    )

def _label(pai, texto, cor=None, tam=12, bold=False):
    peso = "bold" if bold else "normal"
    cor = cor or CORES["texto"]
    return tk.Label(pai, text=texto, font=("Courier", tam, peso),
                    fg=cor, bg=CORES["bg"], wraplength=540)

def _titulo(pai, texto, tam=22):
    return tk.Label(pai, text=texto, font=("Impact", tam),
                    fg=CORES["titulo"], bg=CORES["bg"])


# Seleção de vizinho

def _obter_vizinhos(jogador, jogadores):
    # Percorre todas as casas do jogador e verifica quais os adversários que têm
    # pelo menos uma casa adjacente (cima, baixo, esquerda, direita)
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


def selecionar_vizinho_tkinter(desafiante, jogadores, tabuleiro_ref=None):
    vizinhos = _obter_vizinhos(desafiante, jogadores)
    if not vizinhos:
        messagebox.showinfo("Sem Vizinhos",
                            f"{desafiante['nome']} não tem vizinhos disponíveis.")
        return None

    resultado = [None]

    janela = tk.Toplevel()
    _estilo_janela(janela, "Escolher Vizinho", 560, 100 + len(vizinhos) * 52)
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
        _btn(frame, texto, lambda v=viz: escolher(v), largura=40).pack(pady=3)

    janela.wait_window()
    return resultado[0]


# Duelo — janela principal com cronómetro e perguntas

def _janela_duelo(perguntas_duelo, categoria, desafiante, desafiado):
    """Corre o duelo de 45 s. Devolve (vencedor_nome, tempos_dict, acertos_dict)."""
    pontos  = {desafiante["nome"]: 0,  desafiado["nome"]: 0}
    tempos  = {desafiante["nome"]: [], desafiado["nome"]: []}
    acertos = {desafiante["nome"]: 0,  desafiado["nome"]: 0}
    resultado = [None]

    janela = tk.Toplevel()
    _estilo_janela(janela, "DUELO", 640, 620)
    janela.grab_set()

    _titulo(janela, "THE FLOOR — DUELO", 20).pack(pady=(10, 0))
    _label(janela, f"{desafiante['nome']}  vs  {desafiado['nome']}",
           cor=CORES["amarelo"], tam=14, bold=True).pack()
    _label(janela, f"Categoria: {categoria}", cor=CORES["titulo"], tam=12).pack()

    frame_crono = tk.Frame(janela, bg=CORES["bg"])
    frame_crono.pack(pady=4)
    lbl_crono = tk.Label(frame_crono, text="45", font=("Impact", 34),
                         fg=CORES["amarelo"], bg=CORES["bg"], width=4)
    lbl_crono.pack()

    lbl_placar = _label(janela,
                        f"{desafiante['nome']}: 0  |  {desafiado['nome']}: 0",
                        cor=CORES["verde"], tam=13, bold=True)
    lbl_placar.pack(pady=2)

    frame_pergunta = tk.Frame(janela, bg=CORES["painel"], padx=12, pady=10)
    frame_pergunta.pack(fill="x", padx=20, pady=6)

    lbl_vez = _label(frame_pergunta, "", cor=CORES["titulo"], tam=12, bold=True)
    lbl_vez.configure(bg=CORES["painel"])
    lbl_vez.pack()

    lbl_pergunta = tk.Label(frame_pergunta, text="", font=("Courier", 13),
                            fg=CORES["texto"], bg=CORES["painel"],
                            wraplength=560, justify="left")
    lbl_pergunta.pack(pady=(4, 2))

    frame_entrada = tk.Frame(janela, bg=CORES["bg"])
    frame_entrada.pack(pady=4)

    entrada_var = tk.StringVar()
    entrada = tk.Entry(frame_entrada, textvariable=entrada_var,
                       font=("Courier", 14), width=30,
                       bg="#1e1e1e", fg="white", insertbackground="white",
                       relief="flat", bd=4)
    entrada.pack(side="left", padx=(0, 8))

    btn_responder = _btn(frame_entrada, "Responder", lambda: None,
                         cor=CORES["verde"], largura=14, fonte_tam=11)
    btn_responder.pack(side="left")

    lbl_feedback = _label(janela, "", tam=10)
    lbl_feedback.pack(pady=2)

    estado = {
        "idx_pergunta": 0,
        "vez":          0,   # 0 = desafiante, 1 = desafiado (alterna a cada resposta)
        "inicio_resp":  0.0,
        "aguardando":   False,
        "inicio_duelo": time.time(),
        "encerrado":    False,
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
        if restante <= 0 or estado["idx_pergunta"] >= len(perguntas_duelo):
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
            lbl_feedback.config(text=f"✔ Correto! ({tempo_resp}s)", fg=CORES["verde"])
        else:
            lbl_feedback.config(
                text=f"✘ Errado! Resposta: {pergunta['resposta']} ({tempo_resp}s)",
                fg=CORES["vermelho"])

        tempos[jogador_atual["nome"]].append(tempo_resp)
        entrada.config(state="disabled")
        estado["aguardando"] = False

        lbl_placar.config(
            text=(f"{desafiante['nome']}: {pontos[desafiante['nome']]}  |  "
                  f"{desafiado['nome']}: {pontos[desafiado['nome']]}"))

        # Alterna a vez e avança para a pergunta seguinte
        estado["vez"] = 1 - estado["vez"]
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

        p_des = pontos[desafiante["nome"]]
        p_def = pontos[desafiado["nome"]]

        if p_des > p_def:
            vencedor = desafiante["nome"]
            motivo = "mais respostas certas"
        elif p_def > p_des:
            vencedor = desafiado["nome"]
            motivo = "mais respostas certas"
        else:
            # Empate em acertos — desempata pelo tempo médio de resposta
            t_des = (sum(tempos[desafiante["nome"]]) / len(tempos[desafiante["nome"]])
                     if tempos[desafiante["nome"]] else float("inf"))
            t_def = (sum(tempos[desafiado["nome"]]) / len(tempos[desafiado["nome"]])
                     if tempos[desafiado["nome"]] else float("inf"))
            vencedor = desafiante["nome"] if t_des <= t_def else desafiado["nome"]
            motivo = "tempo médio mais rápido"

        resultado[0] = vencedor
        _janela_resultado(desafiante, desafiado, pontos, tempos, vencedor, motivo,
                          on_close=janela.destroy)

    janela.after(500, atualizar_crono)
    janela.after(300, mostrar_proxima_pergunta)
    janela.wait_window()
    return resultado[0], tempos, acertos


# Resultado do duelo

def _janela_resultado(desafiante, desafiado, pontos, tempos, vencedor, motivo, on_close):
    jan = tk.Toplevel()
    _estilo_janela(jan, "Resultado do Duelo", 520, 480)
    jan.grab_set()

    _titulo(jan, "RESULTADO FINAL", 22).pack(pady=(18, 4))

    cor_des = CORES["verde"] if vencedor == desafiante["nome"] else CORES["vermelho"]
    cor_def = CORES["verde"] if vencedor == desafiado["nome"]  else CORES["vermelho"]

    t_des = (round(sum(tempos[desafiante["nome"]]) / len(tempos[desafiante["nome"]]), 2)
             if tempos[desafiante["nome"]] else 0)
    t_def = (round(sum(tempos[desafiado["nome"]]) / len(tempos[desafiado["nome"]]), 2)
             if tempos[desafiado["nome"]] else 0)

    _label(jan, f"{desafiante['nome']}", cor=cor_des, tam=14, bold=True).pack()
    _label(jan, f"{pontos[desafiante['nome']]} acertos  |  {t_des}s médio",
           cor=cor_des, tam=12).pack()
    _label(jan, "vs", cor=CORES["cinza"], tam=11).pack(pady=4)
    _label(jan, f"{desafiado['nome']}", cor=cor_def, tam=14, bold=True).pack()
    _label(jan, f"{pontos[desafiado['nome']]} acertos  |  {t_def}s médio",
           cor=cor_def, tam=12).pack()

    tk.Label(jan, text=f"🏆  {vencedor}  ganhou!",
             font=("Impact", 18), fg=CORES["amarelo"], bg=CORES["bg"]).pack(pady=(14, 2))
    _label(jan, f"({motivo})", cor=CORES["cinza"], tam=11).pack()

    _btn(jan, "Continuar", lambda: (jan.destroy(), on_close()),
         cor=CORES["accent"], largura=20).pack(pady=14)

    jan.wait_window()


# Escolher próximo desafiante

def escolher_proximo_desafiante_tkinter(vencedor_nome, jogadores):
    resultado = [None]

    jan = tk.Toplevel()
    _estilo_janela(jan, "Próximo Duelo", 500, 360)
    jan.grab_set()

    _titulo(jan, "PRÓXIMO DUELO", 18).pack(pady=(16, 4))
    _label(jan, f"{vencedor_nome} venceu!", cor=CORES["amarelo"], tam=13, bold=True).pack()
    _label(jan, "O vencedor quer continuar a jogar?", tam=12).pack(pady=6)

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
         cor=CORES["verde"], largura=32).pack(pady=4)
    _btn(frame, "🎲  Sortear outro jogador", sortear,
         cor=CORES["cinza"], largura=32).pack(pady=4)

    jan.wait_window()
    return resultado[0]


# Executar duelo

def executar_duelo_tkinter(desafiante, desafiado, jogadores, duelos, tabuleiro_ref=None):
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
        messagebox.showinfo("Defesa", f"{desafiado['nome']} defendeu com sucesso!")

    t_des = (round(sum(tempos[desafiante["nome"]]) / len(tempos[desafiante["nome"]]), 2)
             if tempos[desafiante["nome"]] else 0)
    t_def = (round(sum(tempos[desafiado["nome"]]) / len(tempos[desafiado["nome"]]), 2)
             if tempos[desafiado["nome"]] else 0)

    # Atualiza as estatísticas nos objetos em memória antes de guardar,
    # caso contrário o guardar_jogadores seria chamado sem elas
    _atualizar_estatisticas(desafiante, t_des, vencedor,
                            len(tempos[desafiante["nome"]]),
                            acertos[desafiante["nome"]], categoria)
    _atualizar_estatisticas(desafiado, t_def, vencedor,
                            len(tempos[desafiado["nome"]]),
                            acertos[desafiado["nome"]], categoria)

    guardar_jogadores(jogadores)

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

    # Atualiza o tabuleiro visual após tudo estar guardado
    if tabuleiro_ref and tabuleiro_ref.esta_aberto():
        tabuleiro_ref.atualizar()

    return duelo


# Loop principal do jogo

def _verificar_fim_tkinter(jogadores):
    ativos = [j for j in jogadores if len(j.get("quadriculas", [])) > 0]
    if len(ativos) == 1:
        messagebox.showinfo("Fim de Jogo! 🏆", f"O vencedor é {ativos[0]['nome']}!")
        return True
    return False


def _janela_entre_duelos(desafiante_nome, jogadores, duelos,
                          proximo_cb, pausar_cb, tabuleiro_ref=None):
    jan = tk.Toplevel()
    _estilo_janela(jan, "Entre Duelos", 560, 500)
    jan.grab_set()

    _titulo(jan, "THE FLOOR", 22).pack(pady=(12, 2))

    ativos = [j for j in jogadores if len(j.get("quadriculas", [])) > 0]
    _label(jan, f"Jogadores ativos: {len(ativos)}", cor=CORES["amarelo"], tam=12).pack()

    ranking = sorted(ativos, key=lambda j: len(j.get("quadriculas", [])), reverse=True)
    frame_rank = tk.Frame(jan, bg=CORES["painel"], padx=10, pady=8)
    frame_rank.pack(fill="x", padx=20, pady=8)

    tk.Label(frame_rank, text="TOP JOGADORES", font=("Impact", 13),
             fg=CORES["titulo"], bg=CORES["painel"]).pack()

    for j in ranking[:8]:
        n_quads = len(j.get("quadriculas", []))
        linha = f"  {j['nome']:<22} {n_quads} quadrículas"
        tk.Label(frame_rank, text=linha, font=("Courier", 11),
                 fg=CORES["texto"], bg=CORES["painel"], anchor="w").pack(fill="x")

    _label(jan, f"Próximo desafiante: {desafiante_nome}",
           cor=CORES["verde"], tam=12, bold=True).pack(pady=4)

    frame_btn = tk.Frame(jan, bg=CORES["bg"])
    frame_btn.pack(pady=8)

    def continuar():
        jan.destroy()
        proximo_cb()

    def pausar():
        guardar_jogadores(jogadores)
        if tabuleiro_ref and tabuleiro_ref.esta_aberto():
            tabuleiro_ref.atualizar()
        messagebox.showinfo("Jogo Pausado", "Estado guardado. Até já!")
        jan.destroy()
        pausar_cb()

    _btn(frame_btn, "▶  Próximo Duelo", continuar,
         cor=CORES["verde"], largura=28).pack(pady=4)
    _btn(frame_btn, "⏸  Pausar e Guardar", pausar,
         cor=CORES["cinza"], largura=28).pack(pady=4)

    jan.wait_window()


def _iniciar_ciclo_jogo(inicializar=False):
    """
    Núcleo do loop de jogo. Se inicializar=True, chama inicializar_tabuleiro()
    antes de começar — usado no Novo Duelo. Se False, retoma o estado que estava
    guardado em jogadores.json — usado no Carregar Jogo.
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    jogadores = carregar_jogadores()

    if len(jogadores) < 2:
        messagebox.showerror("Erro",
                             "São necessários pelo menos 2 jogadores para iniciar o jogo.")
        return

    duelos = carregar_duelos()

    if inicializar:
        ativos = [j for j in jogadores if len(j.get("quadriculas", [])) > 0]
        if ativos:
            resp = messagebox.askyesno(
                "Jogo em Curso",
                "Já existe um jogo em curso. Iniciar um novo duelo irá APAGAR o progresso atual.\n\nTem a certeza?")
            if not resp:
                return
        inicializar_tabuleiro(jogadores)
        jogadores = carregar_jogadores()

    tabuleiro = JanelaTabuleiro()
    tabuleiro.atualizar()

    proximo_desafiante = [None]
    jogo_ativo = [True]

    def ciclo_jogo():
        if not jogo_ativo[0]:
            return

        jogadores_atuais = carregar_jogadores()

        if tabuleiro.esta_aberto():
            tabuleiro.atualizar()

        if _verificar_fim_tkinter(jogadores_atuais):
            if tabuleiro.esta_aberto():
                tabuleiro.atualizar()
            return

        if proximo_desafiante[0]:
            nome_prox = proximo_desafiante[0]["nome"]
            desafiante = next(
                (j for j in jogadores_atuais
                 if j["nome"] == nome_prox and len(j.get("quadriculas", [])) > 0), None)
            proximo_desafiante[0] = None
            # se o desafiante preferido entretanto foi eliminado, sorteia outro
            if desafiante is None:
                ativos = [j for j in jogadores_atuais if len(j.get("quadriculas", [])) > 0]
                desafiante = random.choice(ativos) if ativos else None
        else:
            ativos = [j for j in jogadores_atuais if len(j.get("quadriculas", [])) > 0]
            desafiante = random.choice(ativos) if ativos else None

        if desafiante is None:
            return

        desafiado = selecionar_vizinho_tkinter(desafiante, jogadores_atuais, tabuleiro)
        if desafiado is None:
            ciclo_jogo()
            return

        duelo = executar_duelo_tkinter(
            desafiante, desafiado, jogadores_atuais, duelos, tabuleiro_ref=tabuleiro)
        if duelo is None:
            ciclo_jogo()
            return

        if tabuleiro.esta_aberto():
            tabuleiro.atualizar()

        if _verificar_fim_tkinter(jogadores_atuais):
            guardar_jogadores(jogadores_atuais)
            if tabuleiro.esta_aberto():
                tabuleiro.atualizar()
            return

        prox = escolher_proximo_desafiante_tkinter(duelo["vencedor"], jogadores_atuais)
        proximo_desafiante[0] = prox

        nome_prox_str = prox["nome"] if prox else "Aleatório"
        _janela_entre_duelos(
            nome_prox_str, jogadores_atuais, duelos,
            proximo_cb=ciclo_jogo,
            pausar_cb=lambda: jogo_ativo.__setitem__(0, False),
            tabuleiro_ref=tabuleiro,
        )

    ciclo_jogo()


# Pontos de entrada públicos

def novo_duelo_tkinter(root=None):
    _iniciar_ciclo_jogo(inicializar=True)


def carregar_jogo_tkinter(root=None):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    jogadores = carregar_jogadores()

    if not jogadores:
        messagebox.showerror("Erro", "Não há jogadores registados.")
        return

    ativos = [j for j in jogadores if len(j.get("quadriculas", [])) > 0]
    if not ativos:
        messagebox.showinfo(
            "Sem Jogo Guardado",
            "Não existe nenhum jogo em curso para retomar.\n\nInicia um Novo Duelo.")
        return

    messagebox.showinfo("Jogo Retomado",
                        f"A retomar o jogo!\n{len(ativos)} jogadores ainda ativos.")
    _iniciar_ciclo_jogo(inicializar=False)


# Reiniciar jogo

def reiniciar_jogo_tkinter(root=None):
    """
    Mostra uma janela de confirmação antes de reiniciar. Se o utilizador confirmar,
    chama _executar_reinicio() que faz o reset efetivo dos ficheiros.
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    confirmacao = tk.Toplevel()
    confirmacao.title("⚠  Reiniciar Jogo")
    confirmacao.geometry("480x260")
    confirmacao.configure(bg="#1a0000")
    confirmacao.resizable(False, False)
    confirmacao.grab_set()

    tk.Label(confirmacao, text="⚠  ATENÇÃO  ⚠",
             font=("Impact", 22), fg="#ff5252", bg="#1a0000").pack(pady=(20, 8))
    tk.Label(confirmacao,
             text="Esta ação irá:\n"
                  "• Apagar todo o progresso do jogo atual\n"
                  "• Repor todos os jogadores ao estado inicial\n"
                  "• Limpar o historial de duelos\n\n"
                  "Esta operação NÃO pode ser desfeita!",
             font=("Courier", 11), fg="#ffcccc", bg="#1a0000",
             justify="left").pack(padx=30)

    frame_btns = tk.Frame(confirmacao, bg="#1a0000")
    frame_btns.pack(pady=16)

    def confirmar():
        confirmacao.destroy()
        _executar_reinicio()

    def cancelar():
        confirmacao.destroy()

    tk.Button(frame_btns, text="✔  Sim, Reiniciar",
              font=("Impact", 13), width=20, bg="#c62828", fg="white",
              relief="flat", cursor="hand2", command=confirmar).pack(side="left", padx=8)
    tk.Button(frame_btns, text="✘  Cancelar",
              font=("Impact", 13), width=20, bg="#555555", fg="white",
              relief="flat", cursor="hand2", command=cancelar).pack(side="left", padx=8)

    confirmacao.wait_window()


def _executar_reinicio():
    import shutil

    FICHEIRO_JOGADORES = "jogadores.json"
    FICHEIRO_RESET     = "jogadores_reset.json"
    FICHEIRO_DUELOS    = "duelos.json"

    try:
        if not os.path.exists(FICHEIRO_RESET):
            messagebox.showerror("Erro", f"Ficheiro '{FICHEIRO_RESET}' não encontrado!")
            return

        shutil.copy2(FICHEIRO_RESET, FICHEIRO_JOGADORES)

        with open(FICHEIRO_DUELOS, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

        jogadores = carregar_jogadores()
        if len(jogadores) < 100:
            messagebox.showerror(
                "Erro",
                f"São necessários 100 jogadores no ficheiro reset. "
                f"Encontrados: {len(jogadores)}.")
            return

        inicializar_tabuleiro(jogadores)

        messagebox.showinfo(
            "Jogo Reiniciado ✔",
            "O jogo foi reiniciado com sucesso!\n\n"
            "Todos os jogadores estão ativos no tabuleiro.\n"
            "Podes iniciar um Novo Duelo quando quiseres.")

    except Exception as e:
        messagebox.showerror("Erro ao Reiniciar", str(e))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    raiz = tk.Tk()
    raiz.withdraw()
    novo_duelo_tkinter(raiz)
    raiz.mainloop()