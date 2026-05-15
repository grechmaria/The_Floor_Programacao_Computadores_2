# Gestão dos duelos e dinâmica do jogo
import json
import os
import random
import time
from gestao_jogadores import carregar_jogadores, guardar_jogadores


FICHEIRO_JOGADORES = "jogadores.json"
FICHEIRO_DUELOS = "duelos.json"
FICHEIRO_PERGUNTAS = "categorias.json"
DURACAO_DUELO = 45  # segundos, como no The Floor RTP

# Carregar e guardar duelos

def carregar_duelos():
    if not os.path.exists(FICHEIRO_DUELOS):
        return []
    try:
        with open(FICHEIRO_DUELOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Erro ao ler o ficheiro de duelos.")
        return []

def guardar_duelos(duelos):
    try:
        with open(FICHEIRO_DUELOS, "w", encoding="utf-8") as f:
            json.dump(duelos, f, indent=4, ensure_ascii=False)
    except IOError:
        print("Erro ao guardar o ficheiro de duelos.")


# Carregar perguntas

def carregar_perguntas():
    if not os.path.exists(FICHEIRO_PERGUNTAS):
        return []
    try:
        with open(FICHEIRO_PERGUNTAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erro ao ler o ficheiro de perguntas.")
        return []

def sortear_perguntas_categoria(perguntas, categoria, n=20):
    """Sorteia até n perguntas únicas da categoria para o duelo."""
    disponiveis = [p for p in perguntas if p["categoria"].lower() == categoria.lower()]
    random.shuffle(disponiveis)
    return disponiveis[:n]

# Tabuleiro

def inicializar_tabuleiro(jogadores):
    tabuleiro = []     # cria grelha 10x10 e atribui uma quadrícula a cada jogador pela ordem da lista
    for i in range(10):
        linha = []
        for j in range(10):
            indice = i * 10 + j
            jogadores[indice]["quadriculas"] = [[i, j]]
            linha.append(jogadores[indice]["nome"])
        tabuleiro.append(linha)

    with open(FICHEIRO_JOGADORES, "w", encoding="utf-8") as f:  # guarda os jogadores com as quadrículas inicializadas
        json.dump(jogadores, f, ensure_ascii=False, indent=4)

    return tabuleiro

def imprimir_tabuleiro(tabuleiro):
    largura = max(len(nome) for linha in tabuleiro for nome in linha)  # encontra o nome mais comprido para formatar todas as colunas com a mesma largura

    print("\n----THE FLOOR----\n")
    for linha in tabuleiro:
        linha_formatada = " | ".join(nome.ljust(largura) for nome in linha)
        print(linha_formatada)
        print("-" * len(linha_formatada))

def atualizar_tabuleiro(tabuleiro, jogadores):  # reconstrói o tabuleiro com base nas quadrículas atuais de cada jogador
    tabuleiro = [[" " for _ in range(10)] for _ in range(10)]
    for jogador in jogadores:
        for (linha, coluna) in jogador["quadriculas"]:
            tabuleiro[linha][coluna] = jogador["nome"]
    return tabuleiro


# Vizinhos (posições adjacentes)

def obter_vizinhos(jogador, jogadores):
    vizinhos = []
    for (linha, coluna) in jogador["quadriculas"]:
        posicoes_possiveis = [
            (linha - 1, coluna),  # cima
            (linha + 1, coluna),  # baixo
            (linha, coluna - 1),  # esquerda
            (linha, coluna + 1)   # direita
        ]
        for outro_jogador in jogadores:
            if outro_jogador["nome"] == jogador["nome"]:
                continue
            for quadricula in outro_jogador["quadriculas"]:
                if list(quadricula) in [list(p) for p in posicoes_possiveis]:
                    if outro_jogador not in vizinhos:
                        vizinhos.append(outro_jogador)
    return vizinhos


def selecionar_vizinho_manual(desafiante, jogadores):   # mostra os vizinhos disponíveis e deixa o desafiante escolher
    vizinhos = obter_vizinhos(desafiante, jogadores)

    if not vizinhos:
        return None

    print(f"\nJogador sorteado: {desafiante['nome']}")
    print("Vizinhos disponíveis para desafiar:")
    for i, vizinho in enumerate(vizinhos, start=1):
        print(f"  {i}. {vizinho['nome']} (categoria: {vizinho['categoria']})")

    escolha = input("Escolhe um vizinho (número): ")

    try:
        indice = int(escolha) - 1
        if 0 <= indice < len(vizinhos):  # verifica se está dentro do intervalo válido
            return vizinhos[indice]
        else:
            print("Escolha inválida. Vizinho escolhido aleatoriamente.")
            return random.choice(vizinhos)
    except ValueError:
        print("Escolha inválida. Vizinho escolhido aleatoriamente.")
        return random.choice(vizinhos)


# Lógica do duelo ao estilo The Floor RTP
#
# Regras:
#   - O duelo tem 45 segundos no total (cronómetro partilhado).
#   - Ambos os jogadores respondem às MESMAS perguntas, em turnos alternados.
#   - Conta o número de respostas certas. Quem acertar mais ganha.
#   - Em empate, ganha quem tiver o menor tempo médio de resposta.
#   - O desafiado é o dono da categoria (é a sua quadrícula que está em jogo).

def _tempo_restante(inicio, duracao):
    """Segundos que faltam para o fim do duelo (>= 0)."""
    return max(0.0, duracao - (time.time() - inicio))

def _cronometro_ativo(inicio, duracao):
    return (time.time() - inicio) < duracao


def fazer_pergunta_com_tempo(jogador, pergunta, inicio_duelo):
    """
    Apresenta a pergunta ao jogador e lê a resposta dentro do tempo restante.
    Devolve (correta, tempo_resposta_segundos).
    """
    restante = _tempo_restante(inicio_duelo, DURACAO_DUELO)
    if restante <= 0:
        print(f"  Tempo esgotado! {jogador['nome']} não tem tempo para responder.")
        return False, 0.0

    print(f"\n  [Tempo restante: {restante:.0f}s]")
    input(f"  Prepara-te, {jogador['nome']}! Prime Enter quando pronto...")

    restante = _tempo_restante(inicio_duelo, DURACAO_DUELO)
    if restante <= 0:
        print(f"  Tempo esgotado enquanto {jogador['nome']} se preparava!")
        return False, 0.0

    print(f"  Pergunta: {pergunta['pergunta']}")
    print(f"  [Tempo restante: {restante:.0f}s]")

    inicio_resp = time.time()
    resposta = input("  Resposta: ").strip().lower()
    tempo_resp = round(time.time() - inicio_resp, 2)

    correta = resposta == pergunta["resposta"].strip().lower()

    if correta:
        print(f"  Correto! ({tempo_resp}s)")
    else:
        print(f"  Errado! A resposta correta era: {pergunta['resposta']} ({tempo_resp}s)")

    # Nota: mesmo que o tempo tenha acabado durante a digitação, a resposta conta
    return correta, tempo_resp


def duelo_the_floor(perguntas_duelo, categoria, desafiante, desafiado):
    """
    Duelo de 45 segundos ao estilo The Floor RTP.
    Devolve (nome_vencedor, dict_tempos_por_jogador, dict_acertos_por_jogador).
    """
    pontos  = {desafiante["nome"]: 0,  desafiado["nome"]: 0}
    tempos  = {desafiante["nome"]: [], desafiado["nome"]: []}
    acertos = {desafiante["nome"]: 0,  desafiado["nome"]: 0}

    separador = "=" * 52
    print(f"\n{separador}")
    print(f"  DUELO: {desafiante['nome']}  vs  {desafiado['nome']}")
    print(f"  Categoria: {categoria}")
    print(f"  Duração: {DURACAO_DUELO} segundos")
    print(separador)
    print()
    print("  Regras:")
    print("  - Ambos respondem às mesmas perguntas, em alternância.")
    print("  - Ganha quem acertar mais dentro dos 45 segundos.")
    print("  - Em caso de empate, decide o tempo médio de resposta.")
    print()

    input("  Prime Enter para começar o duelo...")
    print()

    inicio_duelo  = time.time()
    perguntas_idx = 0

    while _cronometro_ativo(inicio_duelo, DURACAO_DUELO) and perguntas_idx < len(perguntas_duelo):
        pergunta = perguntas_duelo[perguntas_idx]
        perguntas_idx += 1

        print(f"\n  {'─'*48}")
        print(f"  Pergunta {perguntas_idx} de {len(perguntas_duelo)}")
        print(f"  {'─'*48}")

        # Desafiante responde
        if not _cronometro_ativo(inicio_duelo, DURACAO_DUELO):
            break
        print(f"\n  >>> Vez de {desafiante['nome']} <<<")
        correta, t = fazer_pergunta_com_tempo(desafiante, pergunta, inicio_duelo)
        if correta:
            pontos[desafiante["nome"]]  += 1
            acertos[desafiante["nome"]] += 1
        if t > 0:
            tempos[desafiante["nome"]].append(t)

        # Desafiado responde à mesma pergunta
        if not _cronometro_ativo(inicio_duelo, DURACAO_DUELO):
            print(f"\n  Tempo esgotado! {desafiado['nome']} não conseguiu responder.")
            break
        print(f"\n  >>> Vez de {desafiado['nome']} <<<")
        correta, t = fazer_pergunta_com_tempo(desafiado, pergunta, inicio_duelo)
        if correta:
            pontos[desafiado["nome"]]  += 1
            acertos[desafiado["nome"]] += 1
        if t > 0:
            tempos[desafiado["nome"]].append(t)

        # Placar parcial
        print(f"\n  Placar: {desafiante['nome']} {pontos[desafiante['nome']]} "
              f"--- {pontos[desafiado['nome']]} {desafiado['nome']}")

    # Resultado final
    print(f"\n{separador}")
    print("  TEMPO ESGOTADO!")
    print(f"  Resultado final:")
    print(f"    {desafiante['nome']}: {pontos[desafiante['nome']]} resposta(s) certa(s)")
    print(f"    {desafiado['nome']}: {pontos[desafiado['nome']]} resposta(s) certa(s)")

    if pontos[desafiante["nome"]] > pontos[desafiado["nome"]]:
        vencedor = desafiante["nome"]
        print(f"\n  VENCEDOR: {vencedor} (mais respostas certas)")

    elif pontos[desafiado["nome"]] > pontos[desafiante["nome"]]:
        vencedor = desafiado["nome"]
        print(f"\n  VENCEDOR: {vencedor} (mais respostas certas)")

    else:
        # Empate: desempate pelo tempo médio de resposta
        print("\n  Empate! Desempate pelo tempo médio de resposta...")

        t_des = (sum(tempos[desafiante["nome"]]) / len(tempos[desafiante["nome"]])) \
                if tempos[desafiante["nome"]] else float("inf")
        t_def = (sum(tempos[desafiado["nome"]])  / len(tempos[desafiado["nome"]])) \
                if tempos[desafiado["nome"]]  else float("inf")

        print(f"    Tempo médio {desafiante['nome']}: {t_des:.2f}s")
        print(f"    Tempo médio {desafiado['nome']}: {t_def:.2f}s")

        if t_des <= t_def:
            vencedor = desafiante["nome"]
        else:
            vencedor = desafiado["nome"]

        print(f"\n  VENCEDOR pelo tempo: {vencedor}")

    print(separador)

    # Atualizar estatísticas
    t_medio_des = (sum(tempos[desafiante["nome"]]) / len(tempos[desafiante["nome"]])) \
                  if tempos[desafiante["nome"]] else 0.0
    t_medio_def = (sum(tempos[desafiado["nome"]])  / len(tempos[desafiado["nome"]])) \
                  if tempos[desafiado["nome"]]  else 0.0

    _atualizar_estatisticas(desafiante, t_medio_des, vencedor,
                            len(tempos[desafiante["nome"]]), acertos[desafiante["nome"]])
    _atualizar_estatisticas(desafiado,  t_medio_def, vencedor,
                            len(tempos[desafiado["nome"]]),  acertos[desafiado["nome"]])

    return vencedor, tempos, acertos


def _atualizar_estatisticas(jogador, tempo_medio, vencedor_duelo,
                             perguntas_respondidas=0, respostas_certas=0):
    jogador["duelos_iniciados"]      = jogador.get("duelos_iniciados", 0) + 1
    jogador["perguntas_respondidas"] = jogador.get("perguntas_respondidas", 0) + perguntas_respondidas
    jogador["respostas_certas"]      = jogador.get("respostas_certas", 0) + respostas_certas

    if vencedor_duelo == jogador["nome"]:
        jogador["duelos_ganhos"]  = jogador.get("duelos_ganhos", 0) + 1
    else:
        jogador["duelos_perdidos"] = jogador.get("duelos_perdidos", 0) + 1

    if tempo_medio > 0:
        tempos = jogador.get("tempos_resposta", [])
        tempos.append(round(tempo_medio, 2))
        jogador["tempos_resposta"] = tempos


# Registo do duelo no ficheiro duelo.json e executar duelo

def executar_duelo(desafiante, desafiado, jogadores, duelos):
    print(f"\nDUELO: {desafiante['nome']} desafia {desafiado['nome']}!")

    # a categoria é a do desafiado (é a quadrícula dele que está em jogo)
    categoria = desafiado["categoria"]
    todas_perguntas = carregar_perguntas()

    # Sortear até 20 perguntas da categoria para o duelo
    perguntas_duelo = sortear_perguntas_categoria(todas_perguntas, categoria, n=20)

    if not perguntas_duelo:
        print(f"  Sem perguntas disponíveis na categoria '{categoria}'.")
        return None

    vencedor, tempos, acertos = duelo_the_floor(perguntas_duelo, categoria, desafiante, desafiado)

    # transferir quadrícula se o desafiante ganhou
    quadriculas_transferidas = []
    if vencedor == desafiante["nome"]:
        quadriculas_transferidas = transferir_quadricula(desafiante, desafiado, jogadores)
    else:
        print(f"{desafiado['nome']} defendeu com sucesso!")
    guardar_jogadores(jogadores)

    # Calcular tempos médios para o registo
    t_des = round(sum(tempos[desafiante["nome"]]) / len(tempos[desafiante["nome"]]), 2) \
            if tempos[desafiante["nome"]] else 0
    t_def = round(sum(tempos[desafiado["nome"]])  / len(tempos[desafiado["nome"]]),  2) \
            if tempos[desafiado["nome"]]  else 0

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
        "quadriculas_transferidas": quadriculas_transferidas
    }
    duelos.append(duelo)
    guardar_duelos(duelos)

    return duelo


# Transferência de quadrículas

def transferir_quadricula(ganhador, perdedor, jogadores):
    # transfere 1 quadrícula adjacente do perdedor para o ganhador
    for quad_g in ganhador["quadriculas"]:
        linha, coluna = quad_g[0], quad_g[1]
        adjacentes = [
            [linha - 1, coluna],
            [linha + 1, coluna],
            [linha, coluna - 1],
            [linha, coluna + 1]
        ]
        for pos in adjacentes:
            for quad_p in list(perdedor["quadriculas"]):  # cópia para iterar com segurança
                if quad_p[0] == pos[0] and quad_p[1] == pos[1]:  # comparação elemento a elemento
                    perdedor["quadriculas"].remove(quad_p)
                    ganhador["quadriculas"].append(quad_p)
                    print(f"Quadrícula {quad_p} transferida de {perdedor['nome']} para {ganhador['nome']}.")
                    return [quad_p]  # transfere apenas 1 por duelo

    print(f"Sem quadrículas adjacentes para transferir.")
    return []

# Pergunta ao utilizador se o vencedor deve participar ou não no próximo duelo

def escolher_proximo_desafiante(vencedor_nome, jogadores):
    print(f"\n{vencedor_nome} venceu o duelo!")
    print("1. Vencedor fica no próximo duelo")
    print("2. Outros jogadores")

    opcao = input("Escolha: ")

    if opcao == "1":
        for j in jogadores:
            if j["nome"] == vencedor_nome:
                j["regressos_grelha"] = j.get("regressos_grelha", 0) + 1
                return j

    # opção 2 ou inválida: sortear outro jogador que não o vencedor
    outros = [j for j in jogadores if j["nome"] != vencedor_nome and len(j["quadriculas"]) > 0]
    if outros:
        return random.choice(outros)
    return None


# Condição de fim do jogo

def verificar_fim_jogo(jogadores):
    jogadores_ativos = []

    for jogador in jogadores:
        if len(jogador["quadriculas"]) > 0:
            jogadores_ativos.append(jogador)  # cria lista dos jogadores que ainda têm quadrículas

    if len(jogadores_ativos) == 1:
        print(f"Fim do jogo! Vencedor: {jogadores_ativos[0]['nome']}")  # quando só há um com quadrículas
        return True
    return False


# Loop principal do iniciar_jogo (chamado no menu principal)

def iniciar_jogo():
    jogadores = carregar_jogadores()

    if len(jogadores) < 2:
        print("São necessários pelo menos 2 jogadores para iniciar o jogo.")
        return

    duelos = carregar_duelos()
    tabuleiro = inicializar_tabuleiro(jogadores)
    imprimir_tabuleiro(tabuleiro)

    proximo_desafiante = None  # no início não há vencedor anterior

    while True:
        if verificar_fim_jogo(jogadores):
            guardar_jogadores(jogadores)
            break

        # se há um desafiante definido (vencedor que ficou), usa-o
        if proximo_desafiante:
            desafiante = proximo_desafiante
            proximo_desafiante = None
        else:
            desafiante = random.choice([j for j in jogadores if len(j["quadriculas"]) > 0])

        desafiado = selecionar_vizinho_manual(desafiante, jogadores)

        if desafiado is None:
            print(f"{desafiante['nome']} não tem vizinhos.")
            continue

        duelo = executar_duelo(desafiante, desafiado, jogadores, duelos)

        if duelo is None:
            continue

        tabuleiro = atualizar_tabuleiro(tabuleiro, jogadores)
        imprimir_tabuleiro(tabuleiro)

        # perguntar se o vencedor fica
        vencedor_nome = duelo["vencedor"]
        proximo_desafiante = escolher_proximo_desafiante(vencedor_nome, jogadores)

        continuar = input("\nPrime Enter para o próximo duelo ou 0 para sair: ")
        if continuar == "0":
            guardar_jogadores(jogadores)
            print("Jogo pausado. O estado foi guardado.")
            break