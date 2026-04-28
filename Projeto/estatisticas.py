#Ponto 2.4
# Estatísticas : duas estruturas
#Dois dicionários para o cálculo das estatísticas, um com informação dos jogadores, outro com informação dos duelos

from gestao_jogadores import carregar_jogadores  #importa o dicionário criado dos jogadores para ser usado nas estatísticas
  

from duelos import carregar_duelos



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





    

