# AI Search Algorithms

Projeto em Python para resolver o problema da regua usando diferentes algoritmos de busca.

## Descrição dos Problemas

### Régua Puzzle

O problema modela uma regua com pecas `A`, pecas `B` e um espaco vazio `-`.
Em cada movimento, uma peca a ate duas posicoes de distancia pode ocupar o espaco vazio.

O objetivo e encontrar uma configuracao final em que nenhuma peca `B` apareca depois de uma peca `A`, ou seja, as pecas `B` devem ficar antes das pecas `A`.

Exemplo:

```text
Inicial: AA-BB
Objetivo valido: BBA-A
```

## Linguagem Utilizada

Python 3.

## Principais Estruturas

- `ReguaPuzzle`: define as regras do problema, os movimentos possiveis, o teste de objetivo, a heuristica e a execucao dos algoritmos.
- `ReguaPuzzleInstance`: carrega instancias a partir de `data/instances/regua_puzzle.json`.
- `Move`: representa uma transicao, com peca movida, custo, estado anterior e novo estado.
- `SearchNode`: representa um no da arvore de busca, com estado, pai, filhos, custo do movimento, custo acumulado, profundidade e caminho.
- `SearchTree`: representa a arvore de busca e calcula nos visitados, nos expandidos e fator medio de ramificacao.
- `Algorithm`: classe base para os algoritmos de busca.

## Algoritmos Implementados

- `Backtracking`
- `Breadth-First Search`
- `Depth-First Search` com limite de profundidade
- `Ordered Search`
- `Greedy Search`
- `A* Search`
- `IDA* Search`

## Exemplo de Operações e Métodos Importantes

- `Puzzle.next_moves(state)`: gera movimentos possiveis.
- `Puzzle.is_goal(state)`: verifica se o estado e objetivo.
- `Puzzle.heuristic(state)`: calcula a heuristica usada nas buscas informadas.
- `Puzzle.solve(instance)`: executa todos os algoritmos para uma instancia.
- `Puzzle.save_results_to_csv(results, output_path)`: salva resultados em CSV.
- `SearchTree.count_visited_nodes()`: retorna os nos visitados.
- `SearchTree.count_expanded_nodes()`: retorna os nos expandidos.
- `SearchTree.average_branching_factor()`: calcula o fator medio de ramificacao.
- `SearchNode.path`: retorna o caminho da raiz ate a solucao.
- `SearchNode.path_cost`: retorna o custo acumulado da solucao.
- `SearchNode.depth`: retorna a profundidade do no.

## Formato de Entrada

As instancias do problema sao carregadas a partir do arquivo `data/instances/regua_puzzle.json`, que contem uma lista de instancias, cada uma com um estado inicial e um estado objetivo.

```json
[
  {
    "name": "regua_puzzle_001",
    "initial_state": "AA-BB",
    "cost_priority": "min",
    "piece_priority": "A"
  },
  {
    "name": "regua_puzzle_002",
    "initial_state": "A-ABB",
    "cost_priority": "min",
    "piece_priority": "A"
  }
]
```

Os campos `cost_priority` e `piece_priority` sao usados para definir a prioridade de custo e a prioridade de peca na estratégia de seleção de estados.

## Como Executar

```bash
python3 main.py
```

Os resultados sao salvos em:

```text
data/results/regua_puzzle_results.csv
```

## Exemplo de Resultado

Exemplo retirado de `data/results/regua_puzzle_results.csv`:

| Instancia          | Algoritmo   | Caminho                                                                | Custo  | Profundidade | Tempo       |
| ------------------ | ----------- | ---------------------------------------------------------------------- | ------ | ------------ | ----------- |
| `regua_puzzle_001` | `A* Search` | `AA-BB -> A-ABB -> ABA-B -> ABAB- -> AB-BA -> -BABA -> B-ABA -> BBA-A` | `11.0` | `7`          | `0.000092s` |
