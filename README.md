# Régua-Puzzle com Algoritmos Clássicos de Busca

## Descrição do problema

Este projeto resolve o problema do **Régua-Puzzle**, um problema clássico de Inteligência Artificial usado para comparar estratégias de busca em espaço de estados.

Um estado é representado por uma sequência de caracteres contendo peças dos tipos `A` e `B`, além de uma posição vazia representada por `-`. A cada movimento, uma peça pode trocar de lugar com o espaço vazio quando está a uma distância de 1 ou 2 posições. O custo do movimento é igual a essa distância.

O objetivo é encontrar uma sequência de movimentos que transforme o estado inicial em um estado final válido. Pela implementação atual, um estado é considerado solução quando não existe nenhuma peça `B` posicionada depois de uma peça `A`. Em outras palavras, todas as peças `B` devem ficar à esquerda das peças `A`; o espaço vazio pode estar em diferentes posições.

Exemplo:

```text
Estado inicial: AA-BB
Estados finais válidos: -BBAA, BB-AA, BBA-A
```

O trabalho tem como objetivo aplicar e comparar métodos de busca não informada e informada, observando caminho encontrado, custo, profundidade, quantidade de nós expandidos e tempo de execução.

## Descrição da implementação

A solução foi implementada em Python e organizada em módulos separados para problema, algoritmos, modelos e utilidades.

O fluxo principal de execução está em `main.py`:

1. Carrega as instâncias definidas em `instances/regua_puzzle.json`.
2. Converte cada entrada em um objeto `PuzzleInstance`.
3. Para cada instância, executa todos os algoritmos listados em `ALGORITHMS`.
4. Usa um timeout para limite de execução de tempo dos algoritmos.
5. Mede o tempo de execução com `perf_counter`.
6. Imprime o caminho da solução e as métricas da árvore de busca.
7. Salva os resultados em `results/regua_puzzle_results.csv`.

Estrutura principal do projeto:

```text
.
├── main.py
├── README.md
├── AGENTS.md
├── instances/
│   └── regua_puzzle.json
└── app/
    ├── algorithms/
    │   ├── a_star_search.py
    │   ├── backtracking_search.py
    │   ├── breadth_first_search.py
    │   ├── depth_first_search.py
    │   ├── greedy_search.py
    │   ├── ida_star_search.py
    │   └── ordered_search.py
    ├── models/
    │   ├── instance.py
    │   ├── move.py
    │   ├── search_node.py
    │   └── search_tree.py
    ├── problems/
    │   └── regua_puzzle.py
    └── utils/
        └── common.py
```

## Linguagens e tecnologias utilizadas

- **Linguagem:** Python.
- **Formato de dados:** JSON para as instâncias de entrada e CSV para o arquivo de resultados.

## Formato de entrada

As instâncias ficam no arquivo `instances/regua_puzzle.json`. O arquivo contém uma lista de objetos JSON, um para cada caso de teste.

Exemplo de instância:

```json
{
  "name": "regua_puzzle_001",
  "initial_state": "AA-BB",
  "move_priority": "shortest",
  "piece_priority": "A"
}
```

Campos utilizados:

- `name`: identificador da instância.
- `initial_state`: estado inicial do puzzle, representado por uma string com peças `A`, peças `B` e uma posição vazia `-`.
- `move_priority`: prioridade de movimento usada pelo algoritmo de backtracking. Os valores presentes nas instâncias são `shortest` e `longest`.
- `piece_priority`: peça priorizada na escolha de movimentos do backtracking. Os valores presentes nas instâncias são `A` e `B`.

## Principais estruturas e classes

`PuzzleInstance`: representa uma instância do problema, armazenando nome, estado inicial e prioridades de movimento e peça.

```python
@dataclass
class PuzzleInstance:
    name: str
    initial_state: tuple[str, ...]
    move_priority: str
    piece_priority: str

    @classmethod
    def from_dict(cls, data: dict) -> "PuzzleInstance":
        return cls(
            name=data["name"],
            initial_state=tuple(data["initial_state"]),
            move_priority=data["move_priority"],
            piece_priority=data["piece_priority"],
        )

    def get_priority(self) -> dict:
        return {
            "piece_priority": self.piece_priority,
            "move_priority": self.move_priority,
        }
```

`Move`: representa um movimento possível, contendo o novo estado, a peça movimentada e o custo do movimento.

```python
@dataclass(frozen=True)
class Move:
    state: Any
    movement: Any
    cost: int
```

`SearchNode`: representa um nó da árvore de busca. Armazena estado, nó pai, filhos, custo do movimento e custo acumulado do caminho.

```python
class SearchNode:
    def __init__(self, state: Any, parent: "SearchNode" = None, cost: int = 0):
        self.state = state
        self.parent = parent
        self.children: list["SearchNode"] = []
        self.cost = cost
        self.path_cost = cost if parent is None else parent.path_cost + cost

    def add_child(self, child_node: "SearchNode"):
        child_node.parent = self
        child_node.path_cost = self.path_cost + child_node.cost
        self.children.append(child_node)

    def get_path(self):
        path = []
        current_node = self
        while current_node is not None:
            path.append(current_node.state)
            current_node = current_node.parent
        return list(reversed(path))
```

`SearchTree`: armazena a raiz da busca, o nó solução e calcula métricas como caminho, profundidade, custo, nós expandidos, nós visitados e fator médio de ramificação.

```python
class SearchTree:
    def __init__(self, root: SearchNode):
        self.root = root
        self.goal = None

    def add_node(self, node: SearchNode, parent: SearchNode):
        parent.add_child(node)

    def set_solution(self, node: SearchNode):
        self.goal = node

    def get_solution_path(self):
        return self.goal.get_path() if self.goal is not None else None

    def get_solution_depth(self):
        if self.goal is None:
            return None
        return len(self.goal.get_path()) - 1

    def get_solution_cost(self):
        if self.goal is None:
            return None
        return self.goal.path_cost

    def get_expanded_nodes(self):
        return sum(1 for node in self._get_nodes() if node.children)

    def get_visited_nodes(self):
        return sum(1 for _ in self._get_nodes())

    def get_average_branching_factor(self):
        expanded_nodes = self.get_expanded_nodes()
        if expanded_nodes == 0:
            return 0

        total_children = sum(len(node.children) for node in self._get_nodes())
        return total_children / expanded_nodes

    def _get_nodes(self):
        stack = [self.root]
        while stack:
            node = stack.pop()
            yield node
            stack.extend(reversed(node.children))
```

Módulo `regua_puzzle`: concentra as regras do problema, como teste de objetivo, geração de sucessores, heurística e carregamento das instâncias.

```python
def is_goal(state: tuple[str]) -> bool:
    seen_a = False
    for piece in state:
        if piece == "A":
            seen_a = True
        if seen_a and piece == "B":
            return False
    return True


def get_successors(state: tuple[str]) -> list[Move]:
    empty_index = state.index("-")
    successors = []
    for i in range(len(state)):
        distance = abs(i - empty_index)
        if distance in MOVES:
            new_state = list(state)
            new_state[empty_index], new_state[i] = new_state[i], new_state[empty_index]
            successors.append(Move(tuple(new_state), state[i], distance))
    return successors


def heuristic(state: tuple[str]) -> int:
    inversions = 0
    pieces_a = 0
    for piece in state:
        if piece == "A":
            pieces_a += 1
        elif piece == "B":
            inversions += pieces_a
    return inversions


def load_instances(path: str) -> list[PuzzleInstance]:
    file_path = Path(path)
    with file_path.open(encoding="utf-8") as file:
        raw_instances = json.load(file)

    return [PuzzleInstance.from_dict(instance) for instance in raw_instances]
```

## Métodos de busca implementados

- **Backtracking Search:** percorre um caminho por vez, escolhendo sucessores conforme prioridade configurada e retornando ao nó pai quando não há sucessores válidos.
- **Breadth-First Search:** utiliza uma fila (`deque`) para expandir primeiro os estados em menor profundidade.
- **Depth-First Search:** utiliza uma pilha (`deque`) para explorar caminhos em profundidade antes de retornar a outros ramos.
- **Ordered Search:** utiliza uma fila de prioridade (`heapq`) ordenada pelo custo acumulado do caminho, funcionando como uma busca de custo uniforme.
- **Greedy Search:** utiliza apenas a heurística para priorizar os estados considerados mais próximos do objetivo.
- **A\* Search:** combina custo acumulado e heurística, usando a função `f(n) = g(n) + h(n)`.
- **IDA\* Search:** aplica aprofundamento iterativo com limite baseado em `f(n) = g(n) + h(n)`.

## Exemplos de execução

Para executar o projeto com as instâncias disponíveis:

```bash
python3 main.py
```

Entrada usada pelo programa:

```text
instances/regua_puzzle.json
```

Recorte esperado da saída para a instância `regua_puzzle_001`:

```text
Instance: regua_puzzle_001
Initial state: AA-BB
Backtracking Search execution time: 0.000198 seconds
Solution path:
AA-BB
A-ABB
...
BBA-A
Solution metrics:
Solution depth: 12
Solution cost: 17
Expanded nodes: 16
Visited nodes: 22
Average branching factor: 1.31
```

Ao final da execução completa, o programa também grava um arquivo CSV:

```text
results/regua_puzzle_results.csv
```

## Principais dificuldades encontradas

1. Definir a função de heurística adequada para o problema, garantindo que ela seja admissível e consistente.

2. Implementar corretamente os algoritmos de busca, especialmente o Backtracking e o IDA\*, que exigem controle cuidadoso da expansão de nós e do gerenciamento de memória.

## Resultados e Desafios

Os resultados das execuções são consolidados no arquivo:

```text
results/regua_puzzle_results.csv
```

![alt text](/docs/images/exemplo001.png)

![alt text](/docs/images/exemplo002.png)

![alt text](/docs/images/exemplo003.png)
