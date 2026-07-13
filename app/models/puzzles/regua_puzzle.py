from time import perf_counter

from app.algorithms.a_star import AStar
from app.algorithms.backtracking import Backtracking
from app.algorithms.base import Algorithm
from app.algorithms.bfs import BFS
from app.algorithms.dfs import DFS
from app.algorithms.greedy import Greedy
from app.algorithms.ida_star import IDAStar
from app.algorithms.ordered import Ordered
from app.models.instances.regua_puzzle_instance import ReguaPuzzleInstance
from app.models.move import Move
from app.models.puzzles.base import Puzzle
from app.models.search_tree.search_node import SearchNode
from app.models.search_tree.search_tree import SearchTree

ALGORITHMS: tuple[Algorithm] = (
    Backtracking,
    BFS,
    DFS,
    Ordered,
    Greedy,
    AStar,
    IDAStar,
)


class ReguaPuzzle(Puzzle):
    instance: ReguaPuzzleInstance

    def __init__(self) -> None:
        self.search_trees: list[SearchTree] = []

    def is_goal(self, state: list[str]) -> bool:
        seen_a = False
        for piece in state:
            if piece == "A":
                seen_a = True
            elif piece == "B" and seen_a:
                return False
        return True

    def next_moves(self, state: list[str]) -> list[Move]:
        empty_index = state.index("-")
        next_moves = []
        for i in range(len(state)):
            distance = abs(i - empty_index)
            if 0 < distance <= 2:
                new_state = list(state)
                new_state[empty_index] = new_state[i]
                new_state[i] = "-"
                next_moves.append(
                    Move(
                        piece=state[i],
                        cost=distance,
                        new_state=new_state,
                        old_state=state,
                    )
                )
        return next_moves

    def select_priority_move(self, moves: list[Move]) -> Move:
        if self.instance.cost_priority == "min":
            return min(
                moves,
                key=lambda move: (
                    move.cost,
                    move.piece != self.instance.piece_priority,
                ),
            )
        elif self.instance.cost_priority == "max":
            return max(
                moves,
                key=lambda move: (
                    move.cost,
                    move.piece != self.instance.piece_priority,
                ),
            )
        return moves[0] if moves else None

    def heuristic(self, state: list[str]) -> float:
        inversions = 0
        pieces_a = 0
        for piece in state:
            if piece == "A":
                pieces_a += 1
            elif piece == "B":
                inversions += pieces_a
        return inversions

    def is_valid_state(self, state: list[str]) -> bool:
        count_a = state.count("A")
        count_b = state.count("B")
        return count_a == 3 and count_b == 3 and state.count("-") == 1

    def create_search_tree(self) -> SearchTree:
        root = SearchNode(list(self.instance.initial_state))
        search_tree = SearchTree(root)
        self.search_trees.append(search_tree)
        return search_tree

    def generate_state_key(self, state: list[str]) -> str:
        return "".join(state)

    def get_initial_state(self) -> list[str]:
        return list(self.instance.initial_state)

    def save_results_to_csv(
        self,
        results: list[dict],
        output_path: str = "data/results/regua_puzzle_results.csv",
    ) -> None:
        super().save_results_to_csv(results, output_path)

    def solve(self, instance: ReguaPuzzleInstance) -> None:
        self.instance = instance
        results = []

        for algorithm in ALGORITHMS:
            print(f"Solving {instance.initial_state} using {algorithm.name}...")
            self.search_trees = []
            start_time = perf_counter()
            solution = algorithm.search(self)
            execution_time = perf_counter() - start_time

            if not self.search_trees:
                raise RuntimeError(
                    f"{algorithm.name} did not create a search tree."
                )

            results.append(
                self.__build_result_row(
                    instance=instance,
                    algorithm_name=algorithm.name,
                    solution=solution,
                    execution_time=execution_time,
                    search_trees=self.search_trees,
                )
            )

            print(
                f"Solution found: {solution.value}"
                if solution
                else "No solution found."
            )

        self.save_results_to_csv(results)

    @staticmethod
    def __format_state(state: list[str]) -> str:
        return "".join(state)

    def __format_solution_path(self, solution: SearchNode) -> str:
        return " -> ".join(
            self.__format_state(node.value)
            for node in solution.path
        )

    def __build_result_row(
        self,
        instance: ReguaPuzzleInstance,
        algorithm_name: str,
        solution: SearchNode | None,
        execution_time: float,
        search_trees: list[SearchTree],
    ) -> dict:
        search_metrics = self.__calculate_search_metrics(search_trees)

        if solution is None:
            return {
                "nome_instancia": instance.name,
                "nome_algoritmo": algorithm_name,
                "caminho_solucao": "",
                "custo_solucao": "",
                "profundidade_solucao": "",
                "tempo_execucao_segundos": f"{execution_time:.6f}",
                **search_metrics,
            }

        return {
            "nome_instancia": instance.name,
            "nome_algoritmo": algorithm_name,
            "caminho_solucao": self.__format_solution_path(solution),
            "custo_solucao": solution.path_cost,
            "profundidade_solucao": solution.depth,
            "tempo_execucao_segundos": f"{execution_time:.6f}",
            **search_metrics,
        }

    @staticmethod
    def __calculate_search_metrics(
        search_trees: list[SearchTree],
    ) -> dict:
        visited_count = 0
        explored_count = 0
        children_count = 0

        for search_tree in search_trees:
            visited_nodes = search_tree.get_visited_nodes()
            visited_count += len(visited_nodes)

            for node in visited_nodes:
                if node.children:
                    explored_count += 1
                    children_count += len(node.children)

        average_branching_factor = (
            children_count / explored_count
            if explored_count
            else 0.0
        )

        return {
            "nos_visitados": visited_count,
            "nos_explorados": explored_count,
            "fator_medio_ramificacao": f"{average_branching_factor:.6f}",
        }
