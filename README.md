# AI Search Algorithms

Projeto em Python para resolver o problema da regua usando diferentes algoritmos de busca.

## Descrição Do Problemas

### Regua Puzzle

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

## Exemplo De Operacoes E Metodos Importantes

- `Puzzle.next_moves(state)`: gera movimentos possiveis.
- `Puzzle.is_goal(state)`: verifica se o estado e objetivo.
- `Puzzle.heuristic(state)`: calcula a heuristica usada nas buscas informadas.
- `Puzzle.solve(instance)`: executa todos os algoritmos para uma instancia.
- `Puzzle.save_results_to_csv(results, output_path)`: salva resultados em CSV.
- `SearchNode.path`: retorna o caminho da raiz ate a solucao.
- `SearchNode.path_cost`: retorna o custo acumulado da solucao.
- `SearchNode.depth`: retorna a profundidade do no.

## Como Executar

```bash
python3 main.py
```

Os resultados sao salvos em:

```text
data/results/regua_puzzle_results.csv
```

## Exemplo De Resultado

Exemplo retirado de `data/results/regua_puzzle_results.csv`:

| Instancia          | Algoritmo   | Caminho                                                                | Custo  | Profundidade | Tempo       |
| ------------------ | ----------- | ---------------------------------------------------------------------- | ------ | ------------ | ----------- |
| `regua_puzzle_001` | `A* Search` | `AA-BB -> A-ABB -> ABA-B -> ABAB- -> AB-BA -> -BABA -> B-ABA -> BBA-A` | `11.0` | `7`          | `0.000092s` |
