# 🏆 The Floor — Implementação em Python

> Trabalho Prático desenvolvido no âmbito da unidade curricular **Programação de Computadores II**

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
| 4 | Os duelos são resolvidos através de **perguntas de escolha múltipla** por categoria |
| 5 | Quem vence o duelo **conquista todas as quadrículas** do adversário |
| 6 | O adversário derrotado é **eliminado** do jogo |
| 7 | Ganha quem **conquistar o tabuleiro inteiro**, ficando como o único jogador em jogo |

---

## 🗂️ Estrutura do Projeto

```
📁 projeto/
│
├── 📄 gestao_jogadores.py            # Gestão dos jogadores (criar, listar, consultar)
├── 📄 gestao_jogo.py                 # Lógica principal do jogo (tabuleiro, duelos)
├── 📄 estatisticas.py                # Estatísticas globais e por jogador
├── 📄 duelos.py                      # Registo e gestão do histórico de duelos
├── 📄 gestao_categorias_perguntas.py # Gestão das perguntas por categoria
│
├── 📄 jogadores.json                 # Base de dados dos jogadores (gerada automaticamente)
├── 📄 categorias.json                # Base de dados das perguntas (gerada automaticamente)
└── 📄 duelos.json                    # Histórico de duelos (gerado automaticamente)
```

---

## 📝 Módulos

### `gestao_jogadores.py`
Tudo o que diz respeito aos jogadores **fora do jogo**:
- Carregar e guardar jogadores em `jogadores.json`
- Listar todos os jogadores
- Consultar detalhes de um jogador específico
- Eliminar um jogador específico

### `gestao_jogo.py`
O **coração do jogo**. Contém toda a lógica de uma partida:
- Inicializar o tabuleiro e distribuir jogadores pelas quadrículas
- Selecionar jogador para jogar no turno atual
- Selecionar vizinho a desafiar
- Executar duelos (com perguntas e verificação de respostas)
- Transferir quadrículas após vitória
- Verificar fim do jogo
- Exibir o tabuleiro no ecrã

### `estatisticas.py`
Registo e apresentação de **estatísticas**:
- Estatísticas globais da partida (total de duelos, respostas corretas, etc.)
- Estatísticas por jogador (duelos ganhos/perdidos, quadrículas conquistadas, etc.)
- Funções para encontrar o jogador mais agressivo e com melhor tempo de resposta

### `duelos.py`
Gestão do **histórico de duelos**:
- Registar cada duelo (quem desafiou, quem foi desafiado, vencedor...)
- Guardar e carregar o histórico em `duelos.json`

### `gestao_categorias_perguntas.py`
Gestão das **perguntas**:
- Criar, editar e eliminar perguntas de escolha múltipla com categoria
- Listar perguntas por categoria
- Carregar e guardar perguntas em `categorias.json`
- Pesquisa de perguntas específicas

---

## 🗄️ Modelo de Dados

Os dados são persistidos em ficheiros **JSON** com codificação UTF-8.

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

---

*Desenvolvido para a UC de Programação de Computadores II — Universidade do Minho*
