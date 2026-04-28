
#Visualização em tkinter
#Comandos Principais
#import tkinter as tk  #importa a biblioteca. 
#tk.Tk()  #cria a janela principal. É sempre a primeira coisa a fazer.
#tk.Label(janela, text="...") #— mostra texto na janela.
#tk.Button(janela, text="...", command=funcao) #— botão clicável. O command= é o que acontece ao clicar.
#.pack(pady=10) #— coloca o elemento na janela com um espaço vertical (pady).
#janela.mainloop() #— obrigatório no final. Mantém a janela aberta e à espera de ações do utilizador. Sem isto, a janela abre e fecha imediatamente.

#Janela para Iniciar o Jogo
#janela.destroy() #fecha a janela atual.
#tk.Toplevel() #abre uma segunda janela por cima. Usa-se para navegar entre ecrãs.
import tkinter as tk
def abrir_menu_jogo():
    janela_inicial.destroy()  # fecha a janela inicial


    menu = tk.Tk()
    menu.title("The Floor - Menu")
    menu.geometry("400x300")
    menu.configure(bg="black")

    tk.Label(menu, text="THE FLOOR", font=("Impact", 30), fg="blue", bg="black").pack(pady=20)

    tk.Button(menu, text="Novo Jogo",      font=("Impact", 12), width=20, command=lambda: print("Novo Jogo")).pack(pady=8)
    tk.Button(menu, text="Carregar Jogo",  font=("Impact", 12), width=20, command=lambda: print("Carregar Jogo")).pack(pady=8)
    tk.Button(menu, text="Estatísticas",   font=("Impact", 12), width=20, command=lambda: print("Estatísticas")).pack(pady=8)
    tk.Button(menu, text="Sair",           font=("Impact", 12), width=20, command=menu.destroy).pack(pady=8)

    menu.mainloop()


def sair():
    janela_inicial.destroy()

janela_inicial = tk.Tk()
janela_inicial.title("The Floor")
janela_inicial.geometry("400x300")
janela_inicial.configure(bg="black")

tk.Label(janela_inicial, text="THE FLOOR",font=("Impact", 28), fg="blue", bg="black").pack(pady=40)
tk.Label(janela_inicial, text="Queres começar o jogo?", font=("Impact", 13), fg="blue", bg="black").pack(pady=10)

tk.Button(janela_inicial, text="Começar Jogo", font=("Impact", 12), width=20, command=abrir_menu_jogo).pack(pady=10)
tk.Button(janela_inicial, text="Sair",font=("Impact", 12), width=20, command=sair).pack(pady=5)

janela_inicial.mainloop()

#necssario defenir cada botao com funcoes!!
#def abrir_menu_jogo():
 
#def abrir_novo_jogo():

#def abrir_estatisticas():
  
#def abrir_carregar_jogo():
 