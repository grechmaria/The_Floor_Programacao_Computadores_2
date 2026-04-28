#Ponto 2.1
import json
import os


FICHEIRO_JOGADORES = "jogadores.json"


#funções para carregar informação do ficheiro

def carregar_jogadores():
    if not os.path.exists(FICHEIRO_JOGADORES):
        return []
    try:
        with open(FICHEIRO_JOGADORES, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Erro ao ler o ficheiro de jogadores.")
        return []


def guardar_jogadores(jogadores):
    try:
        with open(FICHEIRO_JOGADORES, "w", encoding="utf-8") as f:
            json.dump(jogadores, f, indent=4, ensure_ascii=False)
    except IOError:
        print("Erro ao guardar o ficheiro de jogadores.")



# Funções
 
def listar_jogadores(jogadores):
    if not jogadores:
        print("Não há jogadores registados.")
        return
 
    print("\nJogadores registados")
    for i, j in enumerate(jogadores, start=1):
        print(f"{i}. {j['nome']} ({j['cidade']})")
    print()
 
 
def remover_jogador(jogadores):
    # remove um jogador da lista e guarda o ficheiro atualizado
    if not jogadores:
        return
 
    nome = input("Nome do jogador a remover: ")
 
    for j in jogadores:
        if j["nome"].lower() == nome.lower():
            jogadores.remove(j)
            guardar_jogadores(jogadores)
            print(f"Jogador '{nome}' removido.")
            return
 
    print(f"Jogador '{nome}' não encontrado.")
 
 
def ver_detalhes_jogador(jogadores):
    if not jogadores:
        return
 
    nome = input("Nome do jogador que pretende ver detalhes: ")
 
    for j in jogadores:
        if j["nome"].lower() == nome.lower():
            print(f"\nDetalhes de {j['nome']}")
            print(f"Idade: {j['idade']}")
            print(f"Profissão: {j['profissao']}")
            print(f"Cidade: {j['cidade']}")
            print(f"Categoria: {j['categoria']}")
            print(f"Quadrículas: {j['quadriculas']}")
            print(f"Duelos iniciados: {j['duelos_iniciados']}")
            print(f"Duelos aceites: {j['duelos_aceites']}")
            print(f"Duelos ganhos: {j['duelos_ganhos']}")
            print(f"Duelos perdidos: {j['duelos_perdidos']}")
            print(f"Regressos à grelha: {j['regressos_grelha']}")
            print(f"Perguntas respondidas: {j['perguntas_respondidas']}")
            print(f"Respostas certas: {j['respostas_certas']}")
            print(f"Tempos de resposta: {j['tempos_resposta']}")
            print(f"Perguntas por categoria: {j['perguntas_por_categoria']}")
            return
 
    print(f"Jogador '{nome}' não encontrado.")
 
 
# menu
 
def menu_jogadores():
    jogadores = carregar_jogadores()
 
    while True:
        print("\nGestão de Jogadores")

        print("1. Listar jogadores")
        print("2. Ver detalhes de jogador")
        print("3. Remover jogador")
        print("0. Voltar")
 
        opcao = input("Número da Opção: ")
 
        if opcao == "1":
            listar_jogadores(jogadores)
        elif opcao == "2":
            ver_detalhes_jogador(jogadores)
        elif opcao == "3":
            remover_jogador(jogadores)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
 
    return jogadores
 
 
if __name__ == "__main__":    #para ao executar nas estatisticas nao abrir o menu jogadores
    menu_jogadores()
 
