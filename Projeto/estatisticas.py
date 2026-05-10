#Ponto 2.4
# Estatísticas : duas estruturas
#Dois dicionários para o cálculo das estatísticas, um com informação dos jogadores, outro com informação dos duelos

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 
from gestao_jogadores import carregar_jogadores  #importa o dicionário criado dos jogadores para ser usado nas estatísticas
from duelos import carregar_duelos


# FUNCOES DE CALCULO

#Tempos médios de resposta por duelo:
def tempo_medio_resposta(duelos):
    try:
        tempos = []

        for duelo in duelos:
            if duelo["tempo_desafiante"] is not None:
                tempos.append(duelo["tempo_desafiante"])
            if duelo["tempo_desafiado"] is not None:
                tempos.append(duelo["tempo_desafiado"])

        media = sum(tempos) / len(tempos)
        return media

    except ZeroDivisionError:
        print("Sem duelos para calcular a média.")
        return 0.0

    except TypeError:
        print("Erro: tempo de resposta com valor inválido.")
        return 0.0


# Número médio de duelos e regressos à grelha
def media_duelos_regressos(jogadores, duelos):
    try:
        total_duelos = len(duelos)
        total_regressos = sum(jogador["regressos_grelha"] for jogador in jogadores)
        total_jogadores = len(jogadores)

        media_duelos = total_duelos / total_jogadores
        media_regressos = total_regressos / total_jogadores

        print(f"Número médio de duelos por jogador: {media_duelos}")
        print(f"Número médio de regressos à grelha por jogador: {media_regressos}")

        return media_duelos, media_regressos

    except ZeroDivisionError:
        print("Sem jogadores registados para calcular a média.")
        return 0.0, 0.0

    except TypeError:
        print("Erro: valor inválido nos dados dos jogadores.")
        return 0.0, 0.0


#Estatísticas por jogador, como tempo médio de resposta, número de perguntas respondidas por
#categoria, categorias conquistadas e nível de agressividade (duelos iniciados vs. regressos à grelha) para calcular essas estatisticas e apenas devolver o valor

def estatisticas_jogador(jogadores):
    # pede o nome do jogador
    nome = input("Nome do jogador: ")

    for jogador in jogadores:
        if jogador["nome"].lower() == nome.lower():

            tempos = jogador["tempos_resposta"]

            # se não tiver tempos ainda
            if len(tempos) == 0:
                print(f"{jogador['nome']}: sem estatísticas ainda.")
                return

            tempo_medio = sum(tempos) / len(tempos)
            perguntas_por_categoria = jogador["perguntas_por_categoria"]
            categorias_conquistadas = len(jogador["quadriculas"])
            agressividade = jogador["duelos_iniciados"] - jogador["regressos_grelha"]

            print(f"\nEstatísticas de {jogador['nome']}:")
            print(f"Tempo médio de resposta: {tempo_medio} segundos")
            print(f"Perguntas por categoria: {perguntas_por_categoria}")
            print(f"Quadrículas conquistadas: {categorias_conquistadas}")
            print(f"Nível de agressividade: {agressividade}")
            return

    print(f"Jogador '{nome}' não encontrado.")


# Jogador mais rápido
def jogador_mais_rapido(jogadores):
    # filtra só jogadores com tempos registados
    jogadores_com_tempos = [j for j in jogadores if len(j["tempos_resposta"]) > 0]

    if not jogadores_com_tempos:
        print("Sem tempos registados para calcular o jogador mais rápido.")
        return "", 0.0

    jogador_rapido = min(jogadores_com_tempos, key=lambda j: sum(j["tempos_resposta"]) / len(j["tempos_resposta"]))
    menor_tempo = sum(jogador_rapido["tempos_resposta"]) / len(jogador_rapido["tempos_resposta"])

    print(f"O jogador mais rápido é {jogador_rapido['nome']} com um tempo médio de {menor_tempo} segundos.")
    return jogador_rapido["nome"], menor_tempo


# Jogador mais agressivo
def jogador_mais_agressivo(jogadores):
    jogador_com_agressividade = [j for j in jogadores if j["duelos_iniciados"] - j["regressos_grelha"] > 0]

    if not jogador_com_agressividade:
        print("Informação insuficiente para calcular o jogador mais agressivo.")
        return "", 0.0
    
    jogador_agressivo = max(jogadores, key=lambda j: j["duelos_iniciados"] - j["regressos_grelha"])
    maior_agressividade = jogador_agressivo["duelos_iniciados"] - jogador_agressivo["regressos_grelha"]

    print(f"O jogador mais agressivo é {jogador_agressivo['nome']} com um nível de agressividade de {maior_agressividade}.")
    return jogador_agressivo["nome"], maior_agressividade

   

#Para mostrar no menu principal

def mostrar_estatisticas():
    jogadores = carregar_jogadores()
    duelos = carregar_duelos()
    media=tempo_medio_resposta(duelos)
    print(f"O tempo médio de resposta é de {media} segundos.")
    media_duelos_regressos(jogadores, duelos)
    estatisticas_jogador(jogadores)
    jogador_mais_rapido(jogadores)
    jogador_mais_agressivo(jogadores)

# MATPLOTLIB

def _cor_padrao(n):
    """Devolve uma lista de n cores no estilo da Aula 7 (tab10)."""
    cmap = plt.get_cmap("tab10")
    return [cmap(i % 10) for i in range(n)]


# Duelos ganhos vs perdidos por jogador
def grafico_duelos_ganhos_perdidos(jogadores):

    jogadores_ativos = [
        j for j in jogadores
        if j["duelos_iniciados"] > 0 or j["duelos_ganhos"] > 0
    ]
    if not jogadores_ativos:
        print("[Gráfico] Sem duelos registados para mostrar.")
        return

    nomes = [j["nome"] for j in jogadores_ativos]
    ganhos = [j["duelos_ganhos"] for j in jogadores_ativos]
    perdidos = [
        j["duelos_iniciados"] - j["duelos_ganhos"] for j in jogadores_ativos
    ]

    x = range(len(nomes))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(max(8, len(nomes) * 0.8), 5))
    barras_ganhos = ax.bar(
        [i - largura / 2 for i in x], ganhos,
        width=largura, label="Duelos Ganhos", color="steelblue"
    )
    barras_perdidos = ax.bar(
        [i + largura / 2 for i in x], perdidos,
        width=largura, label="Duelos Perdidos", color="tomato"
    )

    # etiquetas em cima de cada barra
    for barra in barras_ganhos:
        if barra.get_height() > 0:
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                barra.get_height() + 0.05,
                str(int(barra.get_height())),
                ha="center", va="bottom", fontsize=9
            )
    for barra in barras_perdidos:
        if barra.get_height() > 0:
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                barra.get_height() + 0.05,
                str(int(barra.get_height())),
                ha="center", va="bottom", fontsize=9
            )

    ax.set_title("Duelos Ganhos vs Perdidos por Jogador", fontsize=13, fontweight="bold")
    ax.set_xlabel("Jogador")
    ax.set_ylabel("Número de Duelos")
    ax.set_xticks(list(x))
    ax.set_xticklabels(nomes, rotation=45, ha="right", fontsize=9)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


# Tempo médio de resposta por jogador
def grafico_tempo_medio_por_jogador(jogadores):

    jogadores_com_tempos = [j for j in jogadores if len(j["tempos_resposta"]) > 0]
    if not jogadores_com_tempos:
        print("[Gráfico] Sem tempos de resposta registados.")
        return

    # ordena do mais rápido ao mais lento
    jogadores_com_tempos.sort(
        key=lambda j: sum(j["tempos_resposta"]) / len(j["tempos_resposta"])
    )
    nomes = [j["nome"] for j in jogadores_com_tempos]
    tempos = [
        round(sum(j["tempos_resposta"]) / len(j["tempos_resposta"]), 2)
        for j in jogadores_com_tempos
    ]

    cores = _cor_padrao(len(nomes))
    fig, ax = plt.subplots(figsize=(8, max(4, len(nomes) * 0.45)))
    barras = ax.barh(nomes, tempos, color=cores)

    # etiqueta no fim de cada barra
    for barra, val in zip(barras, tempos):
        ax.text(
            barra.get_width() + 0.02, barra.get_y() + barra.get_height() / 2,
            f"{val}s", va="center", fontsize=9
        )

    ax.set_title("Tempo Médio de Resposta por Jogador", fontsize=13, fontweight="bold")
    ax.set_xlabel("Tempo médio (segundos)")
    ax.set_ylabel("Jogador")
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


# Distribuição das vitórias entre jogadores
def grafico_circular_vitorias(jogadores):

    jogadores_com_vitorias = [j for j in jogadores if j["duelos_ganhos"] > 0]
    if not jogadores_com_vitorias:
        print("[Gráfico] Sem vitórias registadas.")
        return

    nomes = [j["nome"] for j in jogadores_com_vitorias]
    vitorias = [j["duelos_ganhos"] for j in jogadores_com_vitorias]

    # destacar o jogador com mais vitórias
    idx_max = vitorias.index(max(vitorias))
    explode = [0.05] * len(nomes)
    explode[idx_max] = 0.15

    fig, ax = plt.subplots(figsize=(7, 7))
    cunhas, textos, autopcts = ax.pie(
        vitorias,
        labels=nomes,
        autopct="%1.1f%%",
        explode=explode,
        startangle=140,
        colors=_cor_padrao(len(nomes))
    )
    for texto in textos:
        texto.set_fontsize(9)

    ax.set_title("Distribuição das Vitórias por Jogador", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


# Nível de agressividade (duelos iniciados vs regressos)
def grafico_agressividade(jogadores):

    jogadores_ativos = [
        j for j in jogadores
        if j["duelos_iniciados"] > 0 or j["regressos_grelha"] > 0
    ]
    if not jogadores_ativos:
        print("[Gráfico] Sem dados de agressividade.")
        return

    nomes = [j["nome"] for j in jogadores_ativos]
    iniciados = [j["duelos_iniciados"] for j in jogadores_ativos]
    regressos = [j["regressos_grelha"] for j in jogadores_ativos]

    x = range(len(nomes))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(max(8, len(nomes) * 0.8), 5))
    ax.bar(
        [i - largura / 2 for i in x], iniciados,
        width=largura, label="Duelos Iniciados", color="darkorange"
    )
    ax.bar(
        [i + largura / 2 for i in x], regressos,
        width=largura, label="Regressos à Grelha", color="mediumseagreen"
    )

    ax.set_title("Agressividade: Duelos Iniciados vs Regressos à Grelha", fontsize=13, fontweight="bold")
    ax.set_xlabel("Jogador")
    ax.set_ylabel("Contagem")
    ax.set_xticks(list(x))
    ax.set_xticklabels(nomes, rotation=45, ha="right", fontsize=9)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


# Quadrículas por jogador (território atual)
def grafico_quadriculas_por_jogador(jogadores):
    jogadores_ativos = [j for j in jogadores if len(j["quadriculas"]) > 0]
    if not jogadores_ativos:
        print("[Gráfico] Sem quadrículas registadas.")
        return

    jogadores_ativos.sort(key=lambda j: len(j["quadriculas"]), reverse=True)
    nomes = [j["nome"] for j in jogadores_ativos]
    quadriculas = [len(j["quadriculas"]) for j in jogadores_ativos]

    cores = _cor_padrao(len(nomes))
    fig, ax = plt.subplots(figsize=(max(8, len(nomes) * 0.6), 5))
    barras = ax.bar(nomes, quadriculas, color=cores)

    for barra, val in zip(barras, quadriculas):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 0.1,
            str(val),
            ha="center", va="bottom", fontsize=9
        )

    ax.set_title("Quadrículas por Jogador (Território Atual)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Jogador")
    ax.set_ylabel("Nº de Quadrículas")
    ax.set_xticks(range(len(nomes)))
    ax.set_xticklabels(nomes, rotation=45, ha="right", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


# Taxa de acerto global (certas vs erradas)
def grafico_circular_taxa_acerto(jogadores):

    total_respondidas = sum(j["perguntas_respondidas"] for j in jogadores)
    total_certas = sum(j["respostas_certas"] for j in jogadores)
    total_erradas = total_respondidas - total_certas

    if total_respondidas == 0:
        print("[Gráfico] Sem perguntas respondidas para mostrar.")
        return

    valores = [total_certas, total_erradas]
    labels = ["Respostas Certas", "Respostas Erradas"]
    cores = ["steelblue", "tomato"]
    explode = [0.05, 0.05]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        valores,
        labels=labels,
        autopct="%1.1f%%",
        explode=explode,
        colors=cores,
        startangle=90
    )
    ax.set_title("Taxa de Acerto Global", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


# Duelos por categoria (quantas vezes cada categoria foi disputada)
def grafico_duelos_por_categoria(duelos):
    if not duelos:
        print("[Gráfico] Sem duelos registados.")
        return

    contagem = {}
    for duelo in duelos:
        cat = duelo.get("categoria", "Desconhecida")
        contagem[cat] = contagem.get(cat, 0) + 1

    # ordenar por frequência
    categorias = sorted(contagem, key=contagem.get, reverse=True)
    valores = [contagem[c] for c in categorias]
    cores = _cor_padrao(len(categorias))

    fig, ax = plt.subplots(figsize=(8, max(4, len(categorias) * 0.4)))
    barras = ax.barh(categorias, valores, color=cores)

    for barra, val in zip(barras, valores):
        ax.text(
            barra.get_width() + 0.05,
            barra.get_y() + barra.get_height() / 2,
            str(val), va="center", fontsize=9
        )

    ax.set_title("Número de Duelos por Categoria", fontsize=13, fontweight="bold")
    ax.set_xlabel("Nº de Duelos")
    ax.set_ylabel("Categoria")
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

# menu de estatisticas4

def mostrar_estatisticas():
    jogadores = carregar_jogadores()
    duelos = carregar_duelos()

    while True:
        print("\n--- ESTATÍSTICAS ---")
        print("1. Tempo médio de resposta global")
        print("2. Média de duelos e regressos por jogador")
        print("3. Estatísticas de um jogador específico")
        print("4. Jogador mais rápido")
        print("5. Jogador mais agressivo")
        print("─── Gráficos ───────────────────────────")
        print("6.  Duelos ganhos vs perdidos [barras]")
        print("7.  Tempo médio de resposta por jogador [barras horizontais]")
        print("8.  Distribuição de vitórias [circular]")
        print("9.  Agressividade por jogador [barras]")
        print("10. Quadrículas por jogador [barras]")
        print("11. Taxa de acerto global [circular]")
        print("12. Duelos por categoria [barras horizontais]")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            media = tempo_medio_resposta(duelos)
            print(f"Tempo médio de resposta: {media:.2f}s")

        elif opcao == "2":
            media_duelos_regressos(jogadores, duelos)

        elif opcao == "3":
            estatisticas_jogador(jogadores)

        elif opcao == "4":
            jogador_mais_rapido(jogadores)

        elif opcao == "5":
            jogador_mais_agressivo(jogadores)

        elif opcao == "6":
            grafico_duelos_ganhos_perdidos(jogadores)

        elif opcao == "7":
            grafico_tempo_medio_por_jogador(jogadores)

        elif opcao == "8":
            grafico_circular_vitorias(jogadores)

        elif opcao == "9":
            grafico_agressividade(jogadores)

        elif opcao == "10":
            grafico_quadriculas_por_jogador(jogadores)

        elif opcao == "11":
            grafico_circular_taxa_acerto(jogadores)

        elif opcao == "12":
            grafico_duelos_por_categoria(duelos)

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")



    

