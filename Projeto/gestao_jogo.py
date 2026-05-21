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

if __name__ == "__main__":
    menu_principal()

