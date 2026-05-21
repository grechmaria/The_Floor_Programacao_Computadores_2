# gestao_jogadores_tkinter.py
# Versão gráfica (Tkinter) da gestão de jogadores.
# Substitui todas as interações shell de gestao_jogadores.py por janelas Tkinter.

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os

from gestao_jogadores import carregar_jogadores, guardar_jogadores

#  Estilo (igual ao duelos_tkinter) 

CORES = {
    "bg":       "#0d1b2a",
    "painel":   "#1b2a3b",
    "accent":   "#1976d2",
    "accent2":  "#1565c0",
    "texto":    "#ffffff",
    "titulo":   "#ffd600",
    "verde":    "#43a047",
    "vermelho": "#e53935",
    "amarelo":  "#ffd600",
    "cinza":    "#546e7a",
}

def _estilo_janela(janela, titulo, largura=680, altura=560):
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")
    janela.configure(bg=CORES["bg"])
    janela.resizable(True, True)

def _btn(pai, texto, comando, cor=None, largura=22, fonte_tam=11):
    cor = cor or CORES["accent"]
    return tk.Button(
        pai, text=texto, command=comando,
        font=("Impact", fonte_tam), width=largura,
        bg=cor, fg="white", relief="flat",
        activebackground=CORES["accent2"], activeforeground="white",
        cursor="hand2",
    )

def _label(pai, texto, cor=None, tam=11, bold=False):
    peso = "bold" if bold else "normal"
    cor = cor or CORES["texto"]
    return tk.Label(pai, text=texto, font=("Courier", tam, peso),
                    fg=cor, bg=CORES["bg"])

def _titulo(pai, texto, tam=22):
    return tk.Label(pai, text=texto, font=("Impact", tam),
                    fg=CORES["titulo"], bg=CORES["bg"])

def _entry(pai, var, largura=28):
    return tk.Entry(pai, textvariable=var, font=("Courier", 12), width=largura,
                    bg="#1b2a3b", fg="#ffffff", insertbackground="#ffd600",
                    relief="flat", bd=4)



#  1. JANELA PRINCIPAL DE GESTÃO DE JOGADORES


def menu_jogadores_tkinter():
    """Abre a janela principal de gestão de jogadores."""
    jogadores = carregar_jogadores()

    janela = tk.Toplevel()
    _estilo_janela(janela, "The Floor — Gestão de Jogadores", 620, 520)
    janela.grab_set()

    _titulo(janela, "GESTÃO DE JOGADORES").pack(pady=(14, 6))

    #  Tabela de jogadores 
    frame_tabela = tk.Frame(janela, bg=CORES["bg"])
    frame_tabela.pack(fill="both", expand=True, padx=16, pady=(0, 6))

    colunas = ("nome", "idade", "profissao", "cidade", "quadriculas")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=14)

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("Treeview",
                     background=CORES["painel"],
                     foreground=CORES["texto"],
                     rowheight=26,
                     fieldbackground=CORES["painel"],
                     font=("Courier", 11))
    estilo.configure("Treeview.Heading",
                     background=CORES["accent"],
                     foreground="white",
                     font=("Impact", 12))
    estilo.map("Treeview", background=[("selected", CORES["accent2"])])

    tabela.heading("nome",        text="Nome")
    tabela.heading("idade",       text="Idade")
    tabela.heading("profissao",   text="Profissão")
    tabela.heading("cidade",      text="Cidade")
    tabela.heading("quadriculas", text="Quadrículas")

    tabela.column("nome",        width=180)
    tabela.column("idade",       width=60,  anchor="center")
    tabela.column("profissao",   width=140)
    tabela.column("cidade",      width=130)
    tabela.column("quadriculas", width=90,  anchor="center")

    scroll = tk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)
    tabela.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    def _atualizar_tabela():
        tabela.delete(*tabela.get_children())
        for j in jogadores:
            tabela.insert("", "end", values=(
                j["nome"], j["idade"], j["profissao"],
                j["cidade"], len(j.get("quadriculas", []))
            ))

    _atualizar_tabela()

    # Botões de ação 
    frame_btns = tk.Frame(janela, bg=CORES["bg"])
    frame_btns.pack(pady=8)

    def abrir_adicionar():
        _janela_adicionar(jogadores, _atualizar_tabela)

    def abrir_detalhes():
        sel = tabela.focus()
        if not sel:
            messagebox.showwarning("Seleção", "Seleciona um jogador primeiro.")
            return
        nome = tabela.item(sel)["values"][0]
        jogador = next((j for j in jogadores if j["nome"] == nome), None)
        if jogador:
            _janela_detalhes(jogador)

    def remover_selecionado():
        sel = tabela.focus()
        if not sel:
            messagebox.showwarning("Seleção", "Seleciona um jogador primeiro.")
            return
        nome = tabela.item(sel)["values"][0]
        if messagebox.askyesno("Confirmar", f"Remover '{nome}'?"):
            jogadores[:] = [j for j in jogadores if j["nome"] != nome]
            guardar_jogadores(jogadores)
            _atualizar_tabela()
            messagebox.showinfo("Removido", f"Jogador '{nome}' removido.")

    def importar_txt():
        caminho = filedialog.askopenfilename(
            title="Selecionar ficheiro TXT",
            filetypes=[("Ficheiros TXT", "*.txt"), ("Todos", "*.*")]
        )
        if not caminho:
            return
        _importar_de_txt(caminho, jogadores, _atualizar_tabela)

    _btn(frame_btns, "➕  Adicionar",    abrir_adicionar,      cor=CORES["verde"],    largura=18).grid(row=0, column=0, padx=6, pady=3)
    _btn(frame_btns, "🔍  Detalhes",     abrir_detalhes,       cor=CORES["accent"],   largura=18).grid(row=0, column=1, padx=6, pady=3)
    _btn(frame_btns, "🗑  Remover",      remover_selecionado,  cor=CORES["vermelho"], largura=18).grid(row=0, column=2, padx=6, pady=3)
    _btn(frame_btns, "📂  Importar TXT", importar_txt,         cor=CORES["cinza"],    largura=18).grid(row=1, column=0, columnspan=3, pady=3)

    tk.Button(janela, text="Fechar", font=("Impact", 10), width=16,
              bg=CORES["cinza"], fg="white", relief="flat",
              command=janela.destroy).pack(pady=(0, 10))



#  2. JANELA ADICIONAR JOGADOR


def _janela_adicionar(jogadores, callback_atualizar):
    jan = tk.Toplevel()
    _estilo_janela(jan, "Adicionar Jogador", 400, 320)
    jan.grab_set()

    _titulo(jan, "NOVO JOGADOR", 16).pack(pady=(14, 8))

    frame = tk.Frame(jan, bg=CORES["bg"])
    frame.pack(padx=30)

    vars_ = {
        "nome":     tk.StringVar(),
        "idade":    tk.StringVar(),
        "profissao":tk.StringVar(),
        "cidade":   tk.StringVar(),
    }
    labels = ["Nome", "Idade", "Profissão", "Cidade"]
    campos = ["nome", "idade", "profissao", "cidade"]

    for i, (lab, campo) in enumerate(zip(labels, campos)):
        tk.Label(frame, text=lab, font=("Courier", 10), fg=CORES["texto"],
                 bg=CORES["bg"], anchor="w", width=10).grid(row=i, column=0, pady=5, sticky="w")
        _entry(frame, vars_[campo], largura=22).grid(row=i, column=1, pady=5, padx=(6, 0))

    def confirmar():
        nome     = vars_["nome"].get().strip()
        idade_s  = vars_["idade"].get().strip()
        profissao= vars_["profissao"].get().strip()
        cidade   = vars_["cidade"].get().strip()

        if not nome:
            messagebox.showerror("Erro", "Nome inválido.", parent=jan); return
        if any(j["nome"].lower() == nome.lower() for j in jogadores):
            messagebox.showerror("Erro", f"Jogador '{nome}' já existe.", parent=jan); return
        try:
            idade = int(idade_s)
        except ValueError:
            messagebox.showerror("Erro", "Idade inválida.", parent=jan); return
        if not profissao or not cidade:
            messagebox.showerror("Erro", "Preenche todos os campos.", parent=jan); return

        jogador = {
            "nome": nome, "idade": idade,
            "profissao": profissao, "cidade": cidade,
            "categoria": "", "quadriculas": [],
            "duelos_iniciados": 0, "duelos_aceites": 0,
            "duelos_ganhos": 0, "duelos_perdidos": 0,
            "regressos_grelha": 0, "perguntas_respondidas": 0,
            "respostas_certas": 0, "tempos_resposta": [],
            "perguntas_por_categoria": {}
        }
        jogadores.append(jogador)
        guardar_jogadores(jogadores)
        callback_atualizar()
        messagebox.showinfo("Sucesso", f"Jogador '{nome}' adicionado.", parent=jan)
        jan.destroy()

    frame_btn = tk.Frame(jan, bg=CORES["bg"])
    frame_btn.pack(pady=12)
    _btn(frame_btn, "Confirmar", confirmar, cor=CORES["verde"], largura=14).pack(side="left", padx=8)
    _btn(frame_btn, "Cancelar", jan.destroy, cor=CORES["cinza"], largura=14).pack(side="left", padx=8)



#  3. JANELA DETALHES DO JOGADOR


def _janela_detalhes(jogador):
    jan = tk.Toplevel()
    _estilo_janela(jan, f"Detalhes — {jogador['nome']}", 520, 560)
    jan.grab_set()

    _titulo(jan, jogador["nome"], 18).pack(pady=(14, 6))

    frame = tk.Frame(jan, bg=CORES["painel"], padx=16, pady=12)
    frame.pack(fill="x", padx=20)

    campos = [
        ("Idade",               jogador["idade"]),
        ("Profissão",           jogador["profissao"]),
        ("Cidade",              jogador["cidade"]),
        ("Categoria",           jogador["categoria"] or "—"),
        ("Quadrículas",         len(jogador.get("quadriculas", []))),
        ("Duelos iniciados",    jogador.get("duelos_iniciados", 0)),
        ("Duelos aceites",      jogador.get("duelos_aceites", 0)),
        ("Duelos ganhos",       jogador.get("duelos_ganhos", 0)),
        ("Duelos perdidos",     jogador.get("duelos_perdidos", 0)),
        ("Regressos à grelha",  jogador.get("regressos_grelha", 0)),
        ("Perguntas respondidas", jogador.get("perguntas_respondidas", 0)),
        ("Respostas certas",    jogador.get("respostas_certas", 0)),
    ]

    for i, (label, valor) in enumerate(campos):
        tk.Label(frame, text=f"{label}:", font=("Courier", 11, "bold"),
                 fg=CORES["titulo"], bg=CORES["painel"], anchor="w", width=24
                 ).grid(row=i, column=0, sticky="w", pady=2)
        tk.Label(frame, text=str(valor), font=("Courier", 11),
                 fg=CORES["texto"], bg=CORES["painel"], anchor="w"
                 ).grid(row=i, column=1, sticky="w", pady=2, padx=(8, 0))

    tempos = jogador.get("tempos_resposta", [])
    tempo_med = round(sum(tempos) / len(tempos), 2) if tempos else "—"
    tk.Label(frame, text="Tempo médio (s):", font=("Courier", 11, "bold"),
             fg=CORES["titulo"], bg=CORES["painel"], anchor="w", width=24
             ).grid(row=len(campos), column=0, sticky="w", pady=2)
    tk.Label(frame, text=str(tempo_med), font=("Courier", 11),
             fg=CORES["texto"], bg=CORES["painel"], anchor="w"
             ).grid(row=len(campos), column=1, sticky="w", pady=2, padx=(8, 0))

    _btn(jan, "◀  Voltar", jan.destroy, cor=CORES["cinza"], largura=14).pack(pady=12)


#  4. IMPORTAR DE TXT


def _importar_de_txt(caminho, jogadores, callback_atualizar):
    adicionados = duplicados = erros = 0
    nomes_existentes = {j["nome"].lower() for j in jogadores}

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split(";")
                if len(partes) != 4:
                    erros += 1
                    continue
                nome, idade_str, profissao, cidade = [p.strip() for p in partes]
                if nome.lower() in nomes_existentes:
                    duplicados += 1
                    continue
                try:
                    idade = int(idade_str)
                except ValueError:
                    erros += 1
                    continue
                jogador = {
                    "nome": nome, "idade": idade,
                    "profissao": profissao, "cidade": cidade,
                    "categoria": "", "quadriculas": [],
                    "duelos_iniciados": 0, "duelos_aceites": 0,
                    "duelos_ganhos": 0, "duelos_perdidos": 0,
                    "regressos_grelha": 0, "perguntas_respondidas": 0,
                    "respostas_certas": 0, "tempos_resposta": [],
                    "perguntas_por_categoria": {}
                }
                jogadores.append(jogador)
                nomes_existentes.add(nome.lower())
                adicionados += 1
    except IOError:
        messagebox.showerror("Erro", "Não foi possível ler o ficheiro.")
        return

    guardar_jogadores(jogadores)
    callback_atualizar()
    messagebox.showinfo(
        "Importação Concluída",
        f"Adicionados: {adicionados}\nDuplicados ignorados: {duplicados}\nErros: {erros}"
    )


#  Teste isolado 
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    raiz = tk.Tk()
    raiz.withdraw()
    menu_jogadores_tkinter()
    raiz.mainloop()
