# Ponto 2.2
import json
import os


FICHEIRO_PERGUNTAS = "categorias.json"


# Funções para carregar e guardar informação do ficheiro

def carregar_perguntas():
    if not os.path.exists(FICHEIRO_PERGUNTAS):  # verifica se ficheiro existe
        return []
    try:
        with open(FICHEIRO_PERGUNTAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):  # converte JSON numa lista/dicionários
        print("Erro ao ler o ficheiro de categorias/perguntas.")
        return []


def guardar_perguntas(perguntas):
    try:
        with open(FICHEIRO_PERGUNTAS, "w", encoding="utf-8") as f:
            json.dump(perguntas, f, indent=4, ensure_ascii=False)  # guarda com formatação legível
    except IOError:
        print("Erro ao guardar o ficheiro de categorias/perguntas.")


# Funções auxiliares

def obter_categorias(perguntas):
    return sorted(set(p["categoria"] for p in perguntas))  # extrai categorias e ordena alfabeticamente


# Funções de listagem

def listar_categorias(perguntas):
    categorias = obter_categorias(perguntas)
    if not categorias:
        print("Não há categorias registadas.")
        return

    print("\nCategorias registadas:")
    for i, cat in enumerate(categorias, start=1):  # numera categorias a partir de 1
        total = sum(1 for p in perguntas if p["categoria"] == cat)  # conta perguntas da categoria
        print(f"{i}. {cat} ({total} pergunta(s))")
    print()


def listar_perguntas_de_categoria(perguntas):
    categorias = obter_categorias(perguntas)
    if not categorias:
        print("Não há categorias registadas.")
        return

    listar_categorias(perguntas)
    categoria = input("Nome da categoria: ")

    perguntas_cat = [p for p in perguntas if p["categoria"].lower() == categoria.lower()]   # filtro 

    if not perguntas_cat:
        print(f"Categoria '{categoria}' não encontrada.")
        return

    print(f"\nPerguntas da categoria '{perguntas_cat[0]['categoria']}':")   # usa nome original
    for i, p in enumerate(perguntas_cat, start=1):
        print(f"  {i}. P: {p['pergunta']}")
        print(f"     R: {p['resposta']}")
    print()


# Funções para adicionar perguntas ou categorias
def adicionar_pergunta(perguntas):
    categorias = obter_categorias(perguntas)
    if not categorias:
        print("Não há categorias. Crie uma categoria primeiro.")
        return

    listar_categorias(perguntas)
    categoria = input("Nome da categoria: ")

    # Encontrar a categoria 
    cat_original = next((c for c in categorias if c.lower() == categoria.lower()), None)  # procura primeira correspondência
    if not cat_original:
        print(f"Categoria '{categoria}' não encontrada.")
        return

    pergunta = input("Nova pergunta: ")
    resposta = input("Resposta: ")

    if not pergunta or not resposta:
        print("Pergunta ou resposta inválida.")
        return

    perguntas.append({"categoria": cat_original, "pergunta": pergunta, "resposta": resposta})    # adiciona nova entrada
    guardar_perguntas(perguntas)
    print(f"Pergunta adicionada à categoria '{cat_original}'.")


# Funções de remoção

def remover_pergunta(perguntas):
    categorias = obter_categorias(perguntas)
    if not categorias:
        print("Não há categorias registadas.")
        return

    listar_categorias(perguntas)
    categoria = input("Nome da categoria: ")

    perguntas_cat = [p for p in perguntas if p["categoria"].lower() == categoria.lower()]  # filtra perguntas da categoria
    if not perguntas_cat:
        print(f"Categoria '{categoria}' não encontrada.")
        return

    print(f"\nPerguntas da categoria '{perguntas_cat[0]['categoria']}':")
    for i, p in enumerate(perguntas_cat, start=1):
        print(f"  {i}. {p['pergunta']}")

    try:
        escolha = int(input("Número da pergunta a remover (0 para cancelar): "))
        if escolha == 0:
            return
        if escolha < 1 or escolha > len(perguntas_cat):
            print("Número inválido.")
            return
    except ValueError:
        print("Número inválido.")
        return

    pergunta_remover = perguntas_cat[escolha - 1]   # índice começa em 0
    perguntas.remove(pergunta_remover)   # remove da lista principal
    guardar_perguntas(perguntas)
    print(f"Pergunta '{pergunta_remover['pergunta']}' removida.")


# Funções de edição

def editar_pergunta(perguntas):
    categorias = obter_categorias(perguntas)
    if not categorias:
        print("Não há categorias registadas.")
        return

    listar_categorias(perguntas)
    categoria = input("Nome da categoria: ").strip()

    perguntas_cat = [p for p in perguntas if p["categoria"].lower() == categoria.lower()]
    if not perguntas_cat:
        print(f"Categoria '{categoria}' não encontrada.")
        return

    print(f"\nPerguntas da categoria '{perguntas_cat[0]['categoria']}':")
    for i, p in enumerate(perguntas_cat, start=1):
        print(f"  {i}. P: {p['pergunta']}")
        print(f"     R: {p['resposta']}")

    try:
        escolha = int(input("Número da pergunta a editar (0 para cancelar): "))
        if escolha == 0:
            return
        if escolha < 1 or escolha > len(perguntas_cat):
            print("Número inválido.")
            return
    except ValueError:
        print("Número inválido.")
        return

    p = perguntas_cat[escolha - 1]
    print(f"\nEditar pergunta: '{p['pergunta']}'")
    nova_pergunta = input("Nova pergunta: ")
    nova_resposta = input("Nova resposta: ")

    idx = perguntas.index(p)  # encontra índice na lista original
    if nova_pergunta:
        perguntas[idx]["pergunta"] = nova_pergunta
    if nova_resposta:
        perguntas[idx]["resposta"] = nova_resposta

    guardar_perguntas(perguntas)
    print("Pergunta atualizada.")


# Função de pesquisa

def pesquisar_pergunta(perguntas):
    if not perguntas:
        print("Não há perguntas registadas.")
        return

    termo = input("Palavra-chave para pesquisar: ").lower()
    if not termo:
        print("Termo de pesquisa inválido.")
        return

    resultados = [p for p in perguntas if termo in p["pergunta"].lower() or termo in p["resposta"].lower()]

    if not resultados:
        print(f"Nenhuma pergunta encontrada com '{termo}'.")
        return

    print(f"\nResultados para '{termo}':")
    for i, p in enumerate(resultados, start=1):
        print(f"  {i}. [{p['categoria']}] P: {p['pergunta']}")
        print(f"       R: {p['resposta']}")
    print()


# Menu principal

def menu_categorias_perguntas():
    perguntas = carregar_perguntas()

    while True:
        print("\nGestão de Categorias e Perguntas")
        print("1. Listar categorias")
        print("2. Listar perguntas de uma categoria")
        print("3. Adicionar pergunta a categoria existente")
        print("4. Editar pergunta")
        print("5. Remover pergunta")
        print("6. Pesquisar pergunta")
        print("0. Voltar")

        opcao = input("Número da Opção: ")

        if opcao == "1":
            listar_categorias(perguntas)
        elif opcao == "2":
            listar_perguntas_de_categoria(perguntas)
        elif opcao == "3":
            adicionar_pergunta(perguntas)
        elif opcao == "4":
            editar_pergunta(perguntas)
        elif opcao == "5":
            remover_pergunta(perguntas)
        elif opcao == "6":
            pesquisar_pergunta(perguntas)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

    return perguntas


if __name__ == "__main__":    # para ao executar nas estatísticas não abrir o menu
    menu_categorias_perguntas()
