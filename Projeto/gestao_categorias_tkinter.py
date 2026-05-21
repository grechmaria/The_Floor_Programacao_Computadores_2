# gestao_categorias_tkinter.py
# Versão gráfica (Tkinter) da gestão de categorias e perguntas.
# Substitui todas as interações shell de gestao_categorias_perguntas.py por janelas Tkinter.

import tkinter as tk
from tkinter import messagebox, ttk
import os

from gestao_categorias_perguntas import (
    carregar_perguntas,
    guardar_perguntas,
    obter_categorias,
)

#  Estilo 

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

def _estilo_janela(janela, titulo, largura=780, altura=620):
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")
    janela.configure(bg=CORES["bg"])
    janela.resizable(True, True)

def _btn(pai, texto, comando, cor=None, largura=20, fonte_tam=11):
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

def _entry(pai, var, largura=32):
    return tk.Entry(pai, textvariable=var, font=("Courier", 12), width=largura,
                    bg="#1b2a3b", fg="#ffffff", insertbackground="#ffd600",
                    relief="flat", bd=4)



#  1. JANELA PRINCIPAL

def menu_categorias_tkinter():
    """Abre a janela principal de gestão de categorias e perguntas."""
    perguntas = carregar_perguntas()

    janela = tk.Toplevel()
    _estilo_janela(janela, "The Floor — Categorias e Perguntas", 720, 640)
    janela.grab_set()

    _titulo(janela, "CATEGORIAS E PERGUNTAS").pack(pady=(14, 6))

    #  Painel esquerdo: lista de categorias 
    frame_principal = tk.Frame(janela, bg=CORES["bg"])
    frame_principal.pack(fill="both", expand=True, padx=14, pady=(0, 4))

    frame_esq = tk.Frame(frame_principal, bg=CORES["bg"], width=240)
    frame_esq.pack(side="left", fill="y", padx=(0, 8))
    frame_esq.pack_propagate(False)

    _label(frame_esq, "CATEGORIAS", cor=CORES["titulo"], tam=11, bold=True).pack(pady=(4, 4))

    lb_cats = tk.Listbox(frame_esq, font=("Courier", 11),
                         bg=CORES["painel"], fg=CORES["texto"],
                         selectbackground=CORES["accent"],
                         selectforeground="white",
                         relief="flat", bd=0,
                         activestyle="none",
                         height=14)
    scroll_cats = tk.Scrollbar(frame_esq, orient="vertical", command=lb_cats.yview)
    lb_cats.configure(yscrollcommand=scroll_cats.set)
    lb_cats.pack(side="left", fill="both", expand=True)
    scroll_cats.pack(side="right", fill="y")

    #  Painel direito: perguntas da categoria selecionada 
    frame_dir = tk.Frame(frame_principal, bg=CORES["bg"])
    frame_dir.pack(side="left", fill="both", expand=True)

    _label(frame_dir, "PERGUNTAS", cor=CORES["titulo"], tam=11, bold=True).pack(pady=(4, 4))

    colunas = ("pergunta", "resposta")
    tabela = ttk.Treeview(frame_dir, columns=colunas, show="headings", height=16)

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("Treeview",
                     background=CORES["painel"],
                     foreground=CORES["texto"],
                     rowheight=28,
                     fieldbackground=CORES["painel"],
                     font=("Courier", 11))
    estilo.configure("Treeview.Heading",
                     background=CORES["accent"],
                     foreground="white",
                     font=("Impact", 12))
    estilo.map("Treeview", background=[("selected", CORES["accent2"])])

    tabela.heading("pergunta", text="Pergunta")
    tabela.heading("resposta", text="Resposta")
    tabela.column("pergunta", width=360)
    tabela.column("resposta", width=220)

    scroll_tab = tk.Scrollbar(frame_dir, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll_tab.set)
    tabela.pack(side="left", fill="both", expand=True)
    scroll_tab.pack(side="right", fill="y")

    # Funções de atualização 

    def _atualizar_categorias():
        lb_cats.delete(0, "end")
        for cat in obter_categorias(perguntas):
            total = sum(1 for p in perguntas if p["categoria"] == cat)
            lb_cats.insert("end", f"{cat}  ({total})")

    def _atualizar_perguntas(categoria):
        tabela.delete(*tabela.get_children())
        for p in perguntas:
            if p["categoria"] == categoria:
                tabela.insert("", "end", values=(p["pergunta"], p["resposta"]))

    def _ao_selecionar_categoria(event=None):
        sel = lb_cats.curselection()
        if not sel:
            return
        texto = lb_cats.get(sel[0])
        cat = texto.rsplit("  (", 1)[0]
        _atualizar_perguntas(cat)

    lb_cats.bind("<<ListboxSelect>>", _ao_selecionar_categoria)
    _atualizar_categorias()

    # Botões 
    frame_btns = tk.Frame(janela, bg=CORES["bg"])
    frame_btns.pack(pady=6)

    def _categoria_selecionada():
        sel = lb_cats.curselection()
        if not sel:
            messagebox.showwarning("Seleção", "Seleciona uma categoria primeiro.")
            return None
        texto = lb_cats.get(sel[0])
        return texto.rsplit("  (", 1)[0]

    def abrir_nova_categoria():
        _janela_nova_categoria(perguntas, _atualizar_categorias)

    def abrir_adicionar_pergunta():
        cat = _categoria_selecionada()
        if cat:
            _janela_adicionar_pergunta(cat, perguntas, _atualizar_categorias, lambda: _atualizar_perguntas(cat))

    def abrir_editar_pergunta():
        cat = _categoria_selecionada()
        if not cat:
            return
        sel_tab = tabela.focus()
        if not sel_tab:
            messagebox.showwarning("Seleção", "Seleciona uma pergunta primeiro.")
            return
        vals = tabela.item(sel_tab)["values"]
        pergunta_txt, resposta_txt = vals[0], vals[1]
        # encontra o objeto real
        p_obj = next((p for p in perguntas
                      if p["categoria"] == cat and p["pergunta"] == pergunta_txt), None)
        if p_obj:
            _janela_editar_pergunta(p_obj, perguntas, _atualizar_categorias, lambda: _atualizar_perguntas(cat))

    def remover_pergunta_sel():
        cat = _categoria_selecionada()
        if not cat:
            return
        sel_tab = tabela.focus()
        if not sel_tab:
            messagebox.showwarning("Seleção", "Seleciona uma pergunta primeiro.")
            return
        vals = tabela.item(sel_tab)["values"]
        pergunta_txt = vals[0]
        if not messagebox.askyesno("Confirmar", f"Remover a pergunta:\n'{pergunta_txt}'?"):
            return
        p_obj = next((p for p in perguntas
                      if p["categoria"] == cat and p["pergunta"] == pergunta_txt), None)
        if p_obj:
            perguntas.remove(p_obj)
            guardar_perguntas(perguntas)
            _atualizar_categorias()
            _atualizar_perguntas(cat)

    def abrir_pesquisar():
        _janela_pesquisar(perguntas)

    def remover_categoria_sel():
        cat = _categoria_selecionada()
        if not cat:
            return
        total = sum(1 for p in perguntas if p["categoria"] == cat)
        msg = (f"Remover a categoria '{cat}' e todas as suas {total} pergunta(s)?"
               if total else f"Remover a categoria '{cat}'?")
        if not messagebox.askyesno("Confirmar", msg):
            return
        perguntas[:] = [p for p in perguntas if p["categoria"] != cat]
        guardar_perguntas(perguntas)
        tabela.delete(*tabela.get_children())
        _atualizar_categorias()
        messagebox.showinfo("Removida", f"Categoria '{cat}' removida.")

    _btn(frame_btns, "➕  Nova Categoria",     abrir_nova_categoria,    cor=CORES["verde"],    largura=20).grid(row=0, column=0, padx=5, pady=3)
    _btn(frame_btns, "➕  Adicionar Pergunta",   abrir_adicionar_pergunta,cor=CORES["accent"],   largura=20).grid(row=0, column=1, padx=5, pady=3)
    _btn(frame_btns, "✏  Editar Pergunta",     abrir_editar_pergunta,   cor=CORES["amarelo"],  largura=20).grid(row=0, column=2, padx=5, pady=3)
    _btn(frame_btns, "🗑  Remover Pergunta",   remover_pergunta_sel,    cor=CORES["vermelho"], largura=20).grid(row=1, column=0, padx=5, pady=3)
    _btn(frame_btns, "🗑  Remover Categoria",  remover_categoria_sel,   cor=CORES["vermelho"], largura=20).grid(row=1, column=1, padx=5, pady=3)
    _btn(frame_btns, "🔍  Pesquisar",          abrir_pesquisar,         cor=CORES["cinza"],    largura=20).grid(row=1, column=2, padx=5, pady=3)
    tk.Button(frame_btns, text="Fechar", font=("Impact", 10), width=20,
              bg=CORES["cinza"], fg="white", relief="flat",
              command=janela.destroy).grid(row=2, column=0, columnspan=3, pady=4)



#  2. NOVA CATEGORIA

def _janela_nova_categoria(perguntas, callback):
    jan = tk.Toplevel()
    _estilo_janela(jan, "Nova Categoria", 440, 280)
    jan.grab_set()

    _titulo(jan, "NOVA CATEGORIA", 16).pack(pady=(14, 8))

    frame = tk.Frame(jan, bg=CORES["bg"])
    frame.pack(padx=30)

    v_nome = tk.StringVar()
    v_perg = tk.StringVar()
    v_resp = tk.StringVar()

    for i, (lab, var) in enumerate([("Nome da categoria", v_nome),
                                     ("Pergunta inicial",  v_perg),
                                     ("Resposta",          v_resp)]):
        tk.Label(frame, text=lab, font=("Courier", 10), fg=CORES["texto"],
                 bg=CORES["bg"], anchor="w", width=18).grid(row=i, column=0, pady=6, sticky="w")
        _entry(frame, var, largura=24).grid(row=i, column=1, pady=6, padx=(6, 0))

    def confirmar():
        nome  = v_nome.get().strip()
        perg  = v_perg.get().strip()
        resp  = v_resp.get().strip()

        if not nome:
            messagebox.showerror("Erro", "Nome inválido.", parent=jan); return
        if any(c.lower() == nome.lower() for c in obter_categorias(perguntas)):
            messagebox.showerror("Erro", f"A categoria '{nome}' já existe.", parent=jan); return
        if not perg or not resp:
            messagebox.showerror("Erro", "É obrigatório ter uma pergunta inicial.", parent=jan); return

        perguntas.append({"categoria": nome, "pergunta": perg, "resposta": resp})
        guardar_perguntas(perguntas)
        callback()
        messagebox.showinfo("Sucesso", f"Categoria '{nome}' criada.", parent=jan)
        jan.destroy()

    frame_btn = tk.Frame(jan, bg=CORES["bg"])
    frame_btn.pack(pady=12)
    _btn(frame_btn, "Confirmar", confirmar,  cor=CORES["verde"], largura=14).pack(side="left", padx=8)
    _btn(frame_btn, "Cancelar",  jan.destroy, cor=CORES["cinza"], largura=14).pack(side="left", padx=8)



#  3. ADICIONAR PERGUNTA

def _janela_adicionar_pergunta(categoria, perguntas, cb_cats, cb_tab):
    jan = tk.Toplevel()
    _estilo_janela(jan, f"Adicionar Pergunta — {categoria}", 440, 240)
    jan.grab_set()

    _titulo(jan, f"ADD PERGUNTA", 15).pack(pady=(14, 2))
    _label(jan, f"Categoria: {categoria}", cor=CORES["amarelo"], tam=10).pack()

    frame = tk.Frame(jan, bg=CORES["bg"])
    frame.pack(padx=30, pady=10)

    v_perg = tk.StringVar()
    v_resp = tk.StringVar()

    for i, (lab, var) in enumerate([("Pergunta", v_perg), ("Resposta", v_resp)]):
        tk.Label(frame, text=lab, font=("Courier", 10), fg=CORES["texto"],
                 bg=CORES["bg"], anchor="w", width=10).grid(row=i, column=0, pady=6, sticky="w")
        _entry(frame, var, largura=28).grid(row=i, column=1, pady=6, padx=(6, 0))

    def confirmar():
        perg = v_perg.get().strip()
        resp = v_resp.get().strip()
        if not perg or not resp:
            messagebox.showerror("Erro", "Preenche pergunta e resposta.", parent=jan); return
        perguntas.append({"categoria": categoria, "pergunta": perg, "resposta": resp})
        guardar_perguntas(perguntas)
        cb_cats(); cb_tab()
        messagebox.showinfo("Sucesso", "Pergunta adicionada.", parent=jan)
        jan.destroy()

    frame_btn = tk.Frame(jan, bg=CORES["bg"])
    frame_btn.pack(pady=8)
    _btn(frame_btn, "Confirmar", confirmar,  cor=CORES["verde"], largura=14).pack(side="left", padx=8)
    _btn(frame_btn, "Cancelar",  jan.destroy, cor=CORES["cinza"], largura=14).pack(side="left", padx=8)


#  4. EDITAR PERGUNTA


def _janela_editar_pergunta(p_obj, perguntas, cb_cats, cb_tab):
    jan = tk.Toplevel()
    _estilo_janela(jan, "Editar Pergunta", 440, 240)
    jan.grab_set()

    _titulo(jan, "EDITAR PERGUNTA", 15).pack(pady=(14, 8))

    frame = tk.Frame(jan, bg=CORES["bg"])
    frame.pack(padx=30)

    v_perg = tk.StringVar(value=p_obj["pergunta"])
    v_resp = tk.StringVar(value=p_obj["resposta"])

    for i, (lab, var) in enumerate([("Pergunta", v_perg), ("Resposta", v_resp)]):
        tk.Label(frame, text=lab, font=("Courier", 10), fg=CORES["texto"],
                 bg=CORES["bg"], anchor="w", width=10).grid(row=i, column=0, pady=6, sticky="w")
        _entry(frame, var, largura=28).grid(row=i, column=1, pady=6, padx=(6, 0))

    def confirmar():
        nova_perg = v_perg.get().strip()
        nova_resp = v_resp.get().strip()
        if not nova_perg or not nova_resp:
            messagebox.showerror("Erro", "Preenche pergunta e resposta.", parent=jan); return
        idx = perguntas.index(p_obj)
        perguntas[idx]["pergunta"] = nova_perg
        perguntas[idx]["resposta"] = nova_resp
        guardar_perguntas(perguntas)
        cb_cats(); cb_tab()
        messagebox.showinfo("Sucesso", "Pergunta atualizada.", parent=jan)
        jan.destroy()

    frame_btn = tk.Frame(jan, bg=CORES["bg"])
    frame_btn.pack(pady=12)
    _btn(frame_btn, "Guardar", confirmar,  cor=CORES["verde"], largura=14).pack(side="left", padx=8)
    _btn(frame_btn, "Cancelar", jan.destroy, cor=CORES["cinza"], largura=14).pack(side="left", padx=8)

#  5. PESQUISAR PERGUNTA


def _janela_pesquisar(perguntas):
    jan = tk.Toplevel()
    _estilo_janela(jan, "Pesquisar Perguntas", 600, 400)
    jan.grab_set()

    _titulo(jan, "PESQUISAR", 16).pack(pady=(14, 6))

    frame_pesq = tk.Frame(jan, bg=CORES["bg"])
    frame_pesq.pack(padx=20, pady=(0, 6))

    v_termo = tk.StringVar()
    _entry(frame_pesq, v_termo, largura=34).pack(side="left", padx=(0, 8))

    colunas = ("categoria", "pergunta", "resposta")
    tabela = ttk.Treeview(jan, columns=colunas, show="headings", height=14)
    tabela.heading("categoria", text="Categoria")
    tabela.heading("pergunta",  text="Pergunta")
    tabela.heading("resposta",  text="Resposta")
    tabela.column("categoria",  width=130)
    tabela.column("pergunta",   width=260)
    tabela.column("resposta",   width=160)

    estilo = ttk.Style()
    estilo.configure("Treeview",
                     background=CORES["painel"], foreground=CORES["texto"],
                     rowheight=22, fieldbackground=CORES["painel"],
                     font=("Courier", 9))
    estilo.configure("Treeview.Heading",
                     background=CORES["accent"], foreground="white",
                     font=("Impact", 10))

    scroll = tk.Scrollbar(jan, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    frame_tab = tk.Frame(jan, bg=CORES["bg"])
    frame_tab.pack(fill="both", expand=True, padx=20)
    tabela.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    def pesquisar():
        termo = v_termo.get().lower().strip()
        tabela.delete(*tabela.get_children())
        if not termo:
            return
        for p in perguntas:
            if termo in p["pergunta"].lower() or termo in p["resposta"].lower():
                tabela.insert("", "end", values=(p["categoria"], p["pergunta"], p["resposta"]))

    _btn(frame_pesq, "Pesquisar", pesquisar, cor=CORES["accent"], largura=12).pack(side="left")
    _btn(jan, "Fechar", jan.destroy, cor=CORES["cinza"], largura=14).pack(pady=8)


# Teste isolado
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    raiz = tk.Tk()
    raiz.withdraw()
    menu_categorias_tkinter()
    raiz.mainloop()
