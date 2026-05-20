# 🏆 The Floor — Implementação em Python

> Trabalho Prático desenvolvido no âmbito da unidade curricular **Programação de Computadores II**
> Universidade do Minho — Licenciatura em Engenharia e Gestão Industrial — 2025/2026

---

## 📺 Sobre o Jogo

**The Floor** é um jogo de conquista de território inspirado no programa de televisão homónimo. O objetivo é simples: ser o **último jogador a sobrar no tabuleiro**.

---

## 📋 Regras Gerais

| # | Regra |
|---|-------|
| 1 | O tabuleiro é uma grelha de **10×10** com 100 quadrículas |
| 2 | Cada quadrícula **pertence a um jogador** no início da partida |
| 3 | Um jogador pode **desafiar um vizinho** (jogador adjacente na grelha) para um duelo |
| 4 | Os duelos têm a duração de **45 segundos** e são resolvidos através de perguntas por categoria |
| 5 | A categoria do duelo é determinada pela **casa do jogador desafiado** |
| 6 | Quem vence o duelo **conquista uma quadrícula** do adversário |
| 7 | O adversário sem quadrículas é **eliminado** do jogo |
| 8 | O vencedor pode **regressar à grelha** ou **continuar a jogar** no turno seguinte |
| 9 | Ganha quem **conquistar o tabuleiro inteiro**, ficando como o único jogador em jogo |

---

## 🗂️ Estrutura do Projeto

```
📁 Projeto/
│
├── 📄 gestao_jogo.py                  # Menu principal — ponto de entrada (modo consola)
├── 📄 gestao_jogadores.py             # Gestão dos jogadores (listar, ver detalhes, remover)
├── 📄 gestao_categorias_perguntas.py  # Gestão das categorias e perguntas
├── 📄 duelos.py                       # Lógica do jogo: tabuleiro, duelos, transferências
├── 📄 estatisticas.py                 # Estatísticas numéricas e gráficos (Matplotlib)
│
├── 📄 Projeto_Tkinter.py              # Ponto de entrada — interface gráfica (modo Tkinter)
├── 📄 duelos_tkinter.py               # Duelos em janelas Tkinter com cronómetro visual
├── 📄 gestao_jogadores_tkinter.py     # Gestão de jogadores em interface gráfica
├── 📄 gestao_categorias_tkinter.py    # Gestão de categorias e perguntas em interface gráfica
├── 📄 tabuleiro_tkinter.py            # Visualização gráfica do tabuleiro 10×10 a cores
├── 📄 graficos_the_floor.py           # Janela de estatísticas gráficas (Matplotlib + Tkinter)
│
├── 📄 jogadores.json                  # Base de dados dos jogadores (gerada automaticamente)
├── 📄 categorias.json                 # Base de dados das perguntas (gerada automaticamente)
└── 📄 duelos.json                     # Histórico de duelos (gerado automaticamente)
```

---

## 📝 Módulos — Modo Consola

### `gestao_jogo.py`
Ponto de entrada da aplicação em modo consola. Apresenta o **menu principal** e dá acesso a todas as funcionalidades: gestão de jogadores, perguntas, jogo e estatísticas.

### `gestao_jogadores.py`
Tudo o que diz respeito aos jogadores **fora do jogo**:
- Carregar e guardar jogadores em `jogadores.json`
- Listar todos os jogadores
- Consultar detalhes de um jogador específico
- Eliminar um jogador

### `gestao_categorias_perguntas.py`
Gestão completa das **perguntas e categorias**:
- Listar categorias e perguntas
- Adicionar, editar e remover perguntas
- Pesquisar perguntas por palavra-chave
- Guardar tudo em `categorias.json`

### `duelos.py`
O **coração do jogo** em modo consola. Contém toda a lógica de uma partida:
- Inicializar o tabuleiro e distribuir jogadores pelas quadrículas
- Detetar vizinhos adjacentes na grelha
- Executar duelos de 45 segundos com cronómetro real
- Transferir quadrículas após vitória
- Gerir o desempate por tempo médio de resposta
- Verificar a condição de fim do jogo
- Exibir o tabuleiro em consola com formatação de caracteres

### `estatisticas.py`
Registo e apresentação de **estatísticas**, numéricas e gráficas:
- Tempo médio de resposta global
- Média de duelos e regressos à grelha por jogador
- Estatísticas detalhadas por jogador (acertos, agressividade, categorias)
- Jogador mais rápido e mais agressivo
- Resumo de todos os duelos realizados
- **6 gráficos Matplotlib**: barras, barras horizontais e circulares

---

## 🖥️ Módulos — Modo Gráfico (Tkinter)

### `Projeto_Tkinter.py`
Ponto de entrada da **interface gráfica**. Apresenta um ecrã de boas-vindas e dá acesso ao menu principal com todos os botões de navegação.

### `duelos_tkinter.py`
Versão gráfica completa da dinâmica de jogo:
- Janela de seleção de vizinho com lista interativa
- Janela de duelo com **cronómetro visual a contagem decrescente**
- Campo de resposta com tecla Enter e botão de submissão
- Feedback imediato de acerto/erro com cores
- Placar atualizado em tempo real
- Janela de resultado final com vencedor destacado
- Popup para decisão do vencedor (continuar ou sortear novo jogador)

### `tabuleiro_tkinter.py`
Visualização gráfica do **tabuleiro 10×10**:
- Cada jogador tem uma cor única na grelha (paleta de 100 cores)
- As iniciais de cada jogador aparecem na sua quadrícula
- Painel lateral com ranking de jogadores por número de quadrículas
- Rodapé com contagem de jogadores ativos e eliminados
- Botão de atualização para refletir o estado mais recente

### `gestao_jogadores_tkinter.py`
Interface gráfica para gestão de jogadores:
- Tabela com todos os jogadores e os seus dados principais
- Janela para adicionar novos jogadores com validação de campos
- Janela de detalhes completos de cada jogador
- Remoção com confirmação
- Importação de jogadores a partir de ficheiro TXT (formato `nome;idade;profissão;cidade`)

### `gestao_categorias_tkinter.py`
Interface gráfica para gestão de categorias e perguntas:
- Painel lateral com lista de categorias e contagem de perguntas
- Tabela de perguntas da categoria selecionada
- Janelas para criar nova categoria, adicionar, editar e remover perguntas
- Pesquisa de perguntas por palavra-chave em todas as categorias

### `graficos_the_floor.py`
Janela de **estatísticas visuais** integrada no Tkinter:
- Duelos ganhos vs. perdidos por jogador (barras agrupadas)
- Tempo médio de resposta por jogador (barras horizontais ordenadas)
- Distribuição de vitórias (gráfico circular)
- Agressividade: duelos iniciados vs. regressos à grelha (barras)
- Taxa de acerto global (gráfico circular)
- Duelos realizados por categoria (barras horizontais)

---

## 🗄️ Modelo de Dados

Os dados são persistidos em ficheiros **JSON** com codificação UTF-8, gerados automaticamente na primeira execução.

### Jogador (`jogadores.json`)

```json
{
  "nome": "João Silva",
  "idade": 21,
  "profissao": "Estudante",
  "cidade": "Braga",
  "categoria": "Capitais do mundo",
  "quadriculas": [[0, 0]],
  "duelos_iniciados": 0,
  "duelos_aceites": 0,
  "duelos_ganhos": 0,
  "duelos_perdidos": 0,
  "regressos_grelha": 0,
  "perguntas_respondidas": 0,
  "respostas_certas": 0,
  "tempos_resposta": [],
  "perguntas_por_categoria": {}
}
```

### Pergunta (`categorias.json`)

```json
{
  "categoria": "Capitais do mundo",
  "pergunta": "Qual é a Capital de França?",
  "resposta": "Paris"
}
```

### Duelo (`duelos.json`)

```json
{
  "id_duelo": 1,
  "desafiante": "João Silva",
  "desafiado": "Maria Costa",
  "categoria": "Capitais do mundo",
  "acertos_desafiante": 2,
  "tempo_medio_desafiante": 4.35,
  "acertos_desafiado": 1,
  "tempo_medio_desafiado": 6.12,
  "vencedor": "João Silva",
  "quadriculas_transferidas": [[0, 1]]
}
```

---

## Como Executar

**Modo Consola:**
```bash
python gestao_jogo.py
```

**Modo Gráfico (Tkinter):**
```bash
python Projeto_Tkinter.py
```

> Requisitos: Python 3.x com `tkinter` e `matplotlib` instalados.


*Desenvolvido para a UC de Programação de Computadores II — Universidade do Minho*