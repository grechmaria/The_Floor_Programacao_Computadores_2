# Gestão dos duelos e dinâmica do jogo
import json
import os
import random
import time
from gestao_jogadores import carregar_jogadores, guardar_jogadores


FICHEIRO_JOGADORES = "jogadores.json"
FICHEIRO_DUELOS = "duelos.json"
FICHEIRO_PERGUNTAS = "categorias.json"

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

def sortear_pergunta_unica(perguntas, categoria, perguntas_usadas):  # sorteia uma pergunta da categoria que ainda não foi usada neste duelo
    disponiveis = [  p for p in perguntas if p["categoria"].lower() == categoria.lower() and p["pergunta"] not in perguntas_usadas]
    if not disponiveis:
        return None
    return random.choice(disponiveis)

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

    with open(FICHEIRO_JOGADORES, "w", encoding="utf-8") as f: # guarda os jogadores com as quadrículas inicializadas
        json.dump(jogadores, f, ensure_ascii=False, indent=4)

    return tabuleiro

def imprimir_tabuleiro(tabuleiro):
    largura = max(len(nome) for linha in tabuleiro for nome in linha)  # encontra o nome mais comprido para formatar todas as colunas com a mesma largura

    print("\n----THE FLOOR----\n")
    for linha in tabuleiro:
        linha_formatada = " | ".join(nome.ljust(largura) for nome in linha)
        print(linha_formatada)
        print("-" * len(linha_formatada))

def atualizar_tabuleiro(tabuleiro, jogadores): # reconstrói o tabuleiro com base nas quadrículas atuais de cada jogador
    tabuleiro = [[" " for _ in range(10)] for _ in range(10)]
    for jogador in jogadores:
        for (linha, coluna) in jogador["quadriculas"]:
            tabuleiro[linha][coluna] = jogador["nome"]
    return tabuleiro


# Visinhos (posições adjacentes)


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



# Perguntas e estatísticas

def fazer_pergunta(jogador, pergunta): # mostra a pergunta e mede o tempo de resposta
    input(f"\nPrepara-te, {jogador['nome']}! Prime Enter")
    print(f"Pergunta: {pergunta['pergunta']}")

    inicio = time.time()
    resposta = input("A tua resposta: ").strip().lower()
    tempo = round(time.time() - inicio, 2)  #arredondar

    correta = resposta == pergunta["resposta"].strip().lower()

    if correta:
        print(f"Correto! ({tempo}s)")
    else:
        print(f"Errado! A resposta correta era: {pergunta['resposta']} ({tempo}s)")

    return correta, tempo

def atualizar_estatisticas_jogador(jogador, acertou, tempo, vencedor_duelo):  # atualiza os campos de estatísticas do jogador após o duelo
    jogador["duelos_iniciados"] = jogador.get("duelos_iniciados", 0) + 1

    if acertou:
        jogador["respostas_certas"] = jogador.get("respostas_certas", 0) + 1

    if vencedor_duelo == jogador["nome"]:
        jogador["duelos_ganhos"] = jogador.get("duelos_ganhos", 0) + 1

    tempos = jogador.get("tempos_resposta", [])
    tempos.append(tempo)
    jogador["tempos_resposta"] = tempos



# Duelos:  duelo em formato melhor de 3 rondas, cada jogador responde a uma pergunta diferente por ronda ( para não haver empate)

def melhor_de_3(perguntas, categoria, desafiante, desafiado, jogadores):
    pontos = {desafiante["nome"]: 0, desafiado["nome"]: 0}
    perguntas_usadas = []
    total_rondas = 3

    print(f"\nDUELO: {desafiante['nome']} vs {desafiado['nome']} ")
    print(f"Categoria: {categoria} | Melhor de {total_rondas} rondas\n")

    # guarda os tempos e acertos por jogador para as estatísticas
    acertos = {desafiante["nome"]: False, desafiado["nome"]: False}
    tempos = {desafiante["nome"]: 0, desafiado["nome"]: 0}

    for ronda in range(1, total_rondas + 1):
        print(f"Ronda {ronda}/{total_rondas} | {desafiante['nome']}: {pontos[desafiante['nome']]} — {desafiado['nome']}: {pontos[desafiado['nome']]}")

        # sortear quem responde primeiro nesta ronda
        primeiro, segundo = random.sample([desafiante, desafiado], 2)

        # primeiro jogador responde
        print(f"\nVez de {primeiro['nome']}:")
        pergunta = sortear_pergunta_unica(perguntas, categoria, perguntas_usadas)
        if not pergunta:
            print("Sem perguntas disponíveis para continuar.")
            break
        perguntas_usadas.append(pergunta["pergunta"])
        acertou, tempo = fazer_pergunta(primeiro, pergunta)
        acertos[primeiro["nome"]] = acertou
        tempos[primeiro["nome"]] = tempo
        if acertou:
            pontos[primeiro["nome"]] += 1

        # segundo jogador responde a uma pergunta diferente
        print(f"\nVez de {segundo['nome']}:")
        pergunta = sortear_pergunta_unica(perguntas, categoria, perguntas_usadas)
        if not pergunta:
            print("Sem perguntas disponíveis para continuar.")
            break
        perguntas_usadas.append(pergunta["pergunta"])
        acertou, tempo = fazer_pergunta(segundo, pergunta)
        acertos[segundo["nome"]] = acertou
        tempos[segundo["nome"]] = tempo
        if acertou:
            pontos[segundo["nome"]] += 1

        print(f"\nPontuação: {desafiante['nome']} {pontos[desafiante['nome']]} — {pontos[desafiado['nome']]} {desafiado['nome']}")

        # verificar vitória antecipada
        rondas_restantes = total_rondas - ronda
        if pontos[desafiante["nome"]] > pontos[desafiado["nome"]] + rondas_restantes:
            print(f"{desafiante['nome']} venceu antecipadamente!")
            break
        if pontos[desafiado["nome"]] > pontos[desafiante["nome"]] + rondas_restantes:
            print(f"{desafiado['nome']} venceu antecipadamente!")
            break

    # desempate — rondas extra até haver vencedor
    while pontos[desafiante["nome"]] == pontos[desafiado["nome"]]:
        print("\nEmpate, próxima ronda.")

        primeiro, segundo = random.sample([desafiante, desafiado], 2)

        print(f"\nVez de {primeiro['nome']}:")
        pergunta = sortear_pergunta_unica(perguntas, categoria, perguntas_usadas)
        if not pergunta:
            # sem perguntas: o desafiado mantém a quadrícula
            print(f"Sem perguntas para continuar. {desafiado['nome']} mantém a quadrícula.")
            return desafiado["nome"]
        perguntas_usadas.append(pergunta["pergunta"])
        acertou, tempo = fazer_pergunta(primeiro, pergunta)
        acertos[primeiro["nome"]] = acertou
        tempos[primeiro["nome"]] = tempo
        if acertou:
            pontos[primeiro["nome"]] += 1

        print(f"\nVez de {segundo['nome']}:")
        pergunta = sortear_pergunta_unica(perguntas, categoria, perguntas_usadas)
        if not pergunta:
            print(f"Sem perguntas para continuar. {desafiado['nome']} mantém a quadrícula.")
            return desafiado["nome"]
        perguntas_usadas.append(pergunta["pergunta"])
        acertou, tempo = fazer_pergunta(segundo, pergunta)
        acertos[segundo["nome"]] = acertou
        tempos[segundo["nome"]] = tempo
        if acertou:
            pontos[segundo["nome"]] += 1

    vencedor = desafiante["nome"] if pontos[desafiante["nome"]] > pontos[desafiado["nome"]] else desafiado["nome"]
    print(f"\nVencedor do duelo: {vencedor}")

    # atualizar estatísticas de ambos os jogadores
    atualizar_estatisticas_jogador(desafiante, acertos[desafiante["nome"]], tempos[desafiante["nome"]], vencedor)
    atualizar_estatisticas_jogador(desafiado, acertos[desafiado["nome"]], tempos[desafiado["nome"]], vencedor)

    return vencedor


# Registo do duelo no ficheiro duelo.json e excutar duelo

def executar_duelo(desafiante, desafiado, jogadores, duelos):
    print(f"\nDUELO: {desafiante['nome']} desafia {desafiado['nome']}!")

    # a categoria é a do desafiado (é a quadrícula dele que está em jogo)
    categoria = desafiado["categoria"]
    perguntas = carregar_perguntas()

    vencedor = melhor_de_3(perguntas, categoria, desafiante, desafiado, jogadores)

    # transferir quadrícula se o desafiante ganhou
    quadriculas_transferidas = []
    if vencedor == desafiante["nome"]:
        quadriculas_transferidas = transferir_quadricula(desafiante, desafiado, jogadores)
    else:
        print(f"{desafiado['nome']} defendeu com sucesso!")
    guardar_jogadores(jogadores)

    # atualizar duelo no ficheiro duelos.json
    duelo = {
        "id_duelo": len(duelos) + 1,
        "desafiante": desafiante["nome"],
        "desafiado": desafiado["nome"],
        "categoria": categoria,
        "resposta_desafiante": "",
        "tempo_desafiante": 0,
        "resposta_desafiado": "",
        "tempo_desafiado": 0,
        "vencedor": vencedor,
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
            for quad_p in perdedor["quadriculas"]:
                if quad_p[0] == pos[0] and quad_p[1] == pos[1]:  # comparação elemento a elemento
                    perdedor["quadriculas"].remove(quad_p)
                    ganhador["quadriculas"].append(quad_p)
                    print(f"Quadrícula {quad_p} transferida de {perdedor['nome']} para {ganhador['nome']}.")
                    return [quad_p]  # transfere apenas 1 por duelo

    print(f"Sem quadrículas adjacentes para transferir.")
    return []

#Pergunta ao utilizador se o vencedor deve participar ou não no próximo duelo

def escolher_proximo_desafiante(vencedor_nome, jogadores):   
    print(f"\n{vencedor_nome} venceu o duelo!")
    print("1. Vencedor fica no próximo duelo")
    print("2. Outros jogadores")
    
    opcao = input("Escolha: ")
    
    if opcao == "1":
        for j in jogadores:
            if j["nome"] == vencedor_nome:
                j["regressos_grelha"] += 1
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
            jogadores_ativos.append(jogador)  #cria lista dos jogadores que ainda têm quadrículas
 
    if len(jogadores_ativos) == 1:
        print(f"Fim do jogo! Vencedor: {jogadores[0]['nome']}")   #quando só há um com quadrículas
        return True
    return False


# Loop princial do iniciar_jogo ( chamado no menu principal)

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