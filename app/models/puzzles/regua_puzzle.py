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
        return SearchTree(root)

    def generate_state_key(self, state: list[str]) -> str:
        return "".join(state)

    def get_initial_state(self) -> list[str]:
        return list(self.instance.initial_state)

    def solve(self, instance: ReguaPuzzleInstance) -> None:
        self.instance = instance
        for algorithm in ALGORITHMS:
            print(f"Solving {instance.initial_state} using {algorithm.name}...")
            solution = algorithm.search(self)
            print(f"Solution found: {solution}" if solution else "No solution found.")
