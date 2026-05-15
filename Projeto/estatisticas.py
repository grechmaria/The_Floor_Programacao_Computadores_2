#Ponto 2.4
# Estatísticas : duas estruturas
#Dois dicionários para o cálculo das estatísticas, um com informação dos jogadores, outro com informação dos duelos

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 
from gestao_jogadores import carregar_jogadores  #importa o dicionário criado dos jogadores para ser usado nas estatísticas
from duelos import carregar_duelos


# FUNCOES DE CALCULO

#Tempos médios de resposta (calculado a partir dos jogadores):
def tempo_medio_resposta(jogadores):
    try:
        todos_tempos = []
        for jogador in jogadores:
            todos_tempos.extend(jogador.get("tempos_resposta", []))

        if not todos_tempos:
            print("Sem tempos registados para calcular a média.")
            return 0.0

        media = sum(todos_tempos) / len(todos_tempos)
        return media

    except (ZeroDivisionError, TypeError):
        print("Erro ao calcular o tempo médio de resposta.")
        return 0.0


# Número médio de duelos e regressos à grelha
def media_duelos_regressos(jogadores, duelos):
    try:
        total_duelos = len(duelos)
        total_regressos = sum(jogador.get("regressos_grelha", 0) for jogador in jogadores)
        total_jogadores = len(jogadores)

        if total_jogadores == 0:
            print("Sem jogadores registados para calcular a média.")
            return 0.0, 0.0

        media_duelos = total_duelos / total_jogadores
        media_regressos = total_regressos / total_jogadores

        print(f"Número médio de duelos por jogador: {media_duelos:.2f}")
        print(f"Número médio de regressos à grelha por jogador: {media_regressos:.2f}")

        return media_duelos, media_regressos

    except (ZeroDivisionError, TypeError):
        print("Erro: valor inválido nos dados dos jogadores.")
        return 0.0, 0.0


#Estatísticas por jogador, como tempo médio de resposta, número de perguntas respondidas por
#categoria, categorias conquistadas e nível de agressividade (duelos iniciados vs. regressos à grelha) para calcular essas estatisticas e apenas devolver o valor

def estatisticas_jogador(jogadores):
    # pede o nome do jogador
    nome = input("Nome do jogador: ").strip()

    for jogador in jogadores:
        if jogador["nome"].lower() == nome.lower():

            tempos = jogador.get("tempos_resposta", [])
            perguntas_respondidas = jogador.get("perguntas_respondidas", 0)
            respostas_certas      = jogador.get("respostas_certas", 0)
            duelos_iniciados      = jogador.get("duelos_iniciados", 0)
            duelos_aceites        = jogador.get("duelos_aceites", 0)
            duelos_ganhos         = jogador.get("duelos_ganhos", 0)
            duelos_perdidos       = jogador.get("duelos_perdidos", 0)
            regressos             = jogador.get("regressos_grelha", 0)
            quadriculas           = len(jogador.get("quadriculas", []))
            perguntas_cat         = jogador.get("perguntas_por_categoria", {})

            tempo_medio = (sum(tempos) / len(tempos)) if tempos else 0.0
            taxa_acerto = (respostas_certas / perguntas_respondidas * 100) if perguntas_respondidas > 0 else 0.0
            agressividade = duelos_iniciados - regressos

            print(f"\nEstatísticas de {jogador['nome']}:")
            print(f"  Tempo médio de resposta : {tempo_medio:.2f}s")
            print(f"  Perguntas respondidas   : {perguntas_respondidas}")
            print(f"  Respostas certas        : {respostas_certas} ({taxa_acerto:.1f}%)")
            print(f"  Duelos iniciados        : {duelos_iniciados}")
            print(f"  Duelos aceites          : {duelos_aceites}")
            print(f"  Duelos ganhos           : {duelos_ganhos}")
            print(f"  Duelos perdidos         : {duelos_perdidos}")
            print(f"  Regressos à grelha      : {regressos}")
            print(f"  Quadrículas atuais      : {quadriculas}")
            print(f"  Nível de agressividade  : {agressividade}")
            if perguntas_cat:
                print(f"  Perguntas por categoria : {perguntas_cat}")
            return

    print(f"Jogador '{nome}' não encontrado.")


# Jogador mais rápido
def jogador_mais_rapido(jogadores):
    # filtra só jogadores com tempos registados
    jogadores_com_tempos = [j for j in jogadores if j.get("tempos_resposta")]

    if not jogadores_com_tempos:
        print("Sem tempos registados para calcular o jogador mais rápido.")
        return "", 0.0

    jogador_rapido = min(jogadores_com_tempos, key=lambda j: sum(j["tempos_resposta"]) / len(j["tempos_resposta"]))
    menor_tempo = sum(jogador_rapido["tempos_resposta"]) / len(jogador_rapido["tempos_resposta"])

    print(f"O jogador mais rápido é {jogador_rapido['nome']} com um tempo médio de {menor_tempo:.2f} segundos.")
    return jogador_rapido["nome"], menor_tempo


# Jogador mais agressivo
def jogador_mais_agressivo(jogadores):
    candidatos = [j for j in jogadores if j.get("duelos_iniciados", 0) > 0]

    if not candidatos:
        print("Informação insuficiente para calcular o jogador mais agressivo.")
        return "", 0

    jogador_agressivo = max(
        candidatos,
        key=lambda j: j.get("duelos_iniciados", 0) - j.get("regressos_grelha", 0)
    )
    agressividade = jogador_agressivo.get("duelos_iniciados", 0) - jogador_agressivo.get("regressos_grelha", 0)

    print(f"O jogador mais agressivo é {jogador_agressivo['nome']} com um nível de agressividade de {agressividade}.")
    return jogador_agressivo["nome"], agressividade


# Resumo dos duelos
def resumo_duelos(duelos):
    """Mostra um resumo dos duelos realizados."""
    if not duelos:
        print("Sem duelos registados.")
        return

    print(f"\nTotal de duelos realizados: {len(duelos)}")
    print(f"{'─'*55}")
    for d in duelos:
        print(f"  Duelo {d['id_duelo']}: {d['desafiante']} vs {d['desafiado']}")
        print(f"    Categoria : {d['categoria']}")
        print(f"    {d['desafiante']}: {d.get('acertos_desafiante', '-')} acertos "
              f"({d.get('tempo_medio_desafiante', 0):.2f}s médio)")
        print(f"    {d['desafiado']}: {d.get('acertos_desafiado', '-')} acertos "
              f"({d.get('tempo_medio_desafiado', 0):.2f}s médio)")
        print(f"    Vencedor  : {d['vencedor']}")
        print(f"{'─'*55}")


# MATPLOTLIB

def _cor_padrao(n):
    """Devolve uma lista de n cores no estilo da Aula 7 (tab10)."""
    cmap = plt.get_cmap("tab10")
    return [cmap(i % 10) for i in range(n)]


# Duelos ganhos vs perdidos por jogador
def grafico_duelos_ganhos_perdidos(jogadores):

    jogadores_ativos = [
        j for j in jogadores
        if j.get("duelos_iniciados", 0) > 0 or j.get("duelos_ganhos", 0) > 0
    ]
    if not jogadores_ativos:
        print("[Gráfico] Sem duelos registados para mostrar.")
        return

    nomes = [j["nome"] for j in jogadores_ativos]
    ganhos = [j.get("duelos_ganhos", 0) for j in jogadores_ativos]
    perdidos = [
        j.get("duelos_iniciados", 0) - j.get("duelos_ganhos", 0) for j in jogadores_ativos
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

    jogadores_com_tempos = [j for j in jogadores if j.get("tempos_resposta")]
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

    jogadores_com_vitorias = [j for j in jogadores if j.get("duelos_ganhos", 0) > 0]
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
        if j.get("duelos_iniciados", 0) > 0 or j.get("regressos_grelha", 0) > 0
    ]
    if not jogadores_ativos:
        print("[Gráfico] Sem dados de agressividade.")
        return

    nomes = [j["nome"] for j in jogadores_ativos]
    iniciados = [j.get("duelos_iniciados", 0) for j in jogadores_ativos]
    regressos = [j.get("regressos_grelha", 0) for j in jogadores_ativos]

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




# Taxa de acerto global (certas vs erradas)
def grafico_circular_taxa_acerto(jogadores):

    total_respondidas = sum(j.get("perguntas_respondidas", 0) for j in jogadores)
    total_certas = sum(j.get("respostas_certas", 0) for j in jogadores)
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

# menu de estatisticas

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
        print("6. Resumo dos duelos")
        print("─── Gráficos ───────────────────────────")
        print("7.  Duelos ganhos vs perdidos [barras]")
        print("8.  Tempo médio de resposta por jogador [barras horizontais]")
        print("9.  Distribuição de vitórias [circular]")
        print("10. Agressividade por jogador [barras]")
        print("11. Taxa de acerto global [circular]")
        print("12. Duelos por categoria [barras horizontais]")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            media = tempo_medio_resposta(jogadores)
            if media > 0:
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
            resumo_duelos(duelos)

        elif opcao == "7":
            grafico_duelos_ganhos_perdidos(jogadores)

        elif opcao == "8":
            grafico_tempo_medio_por_jogador(jogadores)

        elif opcao == "9":
            grafico_circular_vitorias(jogadores)

        elif opcao == "10":
            grafico_agressividade(jogadores)


        elif opcao == "11":
            grafico_circular_taxa_acerto(jogadores)

        elif opcao == "12":
            grafico_duelos_por_categoria(duelos)

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")