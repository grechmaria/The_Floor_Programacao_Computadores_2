# Pontos 2.3. Dinâmica de jogo e gestão de tabuleiro
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))  #garante que independetemente de onde é executado o python procura os ficheiros json na pasta correta

from gestao_jogadores import carregar_jogadores
from gestao_jogadores import menu_jogadores
from gestao_categorias_perguntas import menu_categorias_perguntas
from estatisticas import mostrar_estatisticas
from duelos import iniciar_jogo      


FICHEIRO_JOGADORES = "jogadores.json"
FICHEIRO_PERGUNTAS = "categorias.json"

jogadores = carregar_jogadores()

#Inicializar categorias (atribuição de uma categoria a um jogador)
def inicializar_categoria(lista_jogadores):
    with open(FICHEIRO_PERGUNTAS, encoding="utf-8") as f:
        perguntas = json.load(f)

    categorias_vistas = []
    for p in perguntas:
        if p["categoria"] not in categorias_vistas:
            categorias_vistas.append(p["categoria"])

    
    for i, jogador in enumerate(lista_jogadores):
        jogador["categoria"] = categorias_vistas[i]

    # Guarda a lista atualizada no ficheiro de jogadores
    with open(FICHEIRO_JOGADORES, "w", encoding="utf-8") as f:
        json.dump(lista_jogadores, f, ensure_ascii=False, indent=4)

    print("Categorias inicializadas com sucesso!")
    return lista_jogadores


 
# Guardar o estado dos jogadores no ficheiro dos jogadores 
def guardar_jogadores(jogadores):
    with open("jogadores.json", "w", encoding="utf-8") as f:
        json.dump(jogadores, f, ensure_ascii=False, indent=4) #ensure_ascii=False=guarda acentos, indent=4=formata com 4 espaços (padrão)

 
inicializar_categoria(jogadores)

#Menu princial para aceder aos menus do jogadores, perguntas, o jogo em si e estatísticas. O jogo é executado por esta função.
def menu_principal():
    while True:
        print("\n---THE FLOOR ---")
        print("1. Gerir Jogadores")
        print("2. Gerir Perguntas")
        print("3. Iniciar Jogo")
        print("4. Mostar Estatísticas")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")
    
        if opcao == "1":
            menu_jogadores()
        elif opcao == "2":
            menu_categorias_perguntas()
        elif opcao == "3":
            iniciar_jogo()           
        elif opcao == "4":
            mostrar_estatisticas()    
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

menu_principal()



