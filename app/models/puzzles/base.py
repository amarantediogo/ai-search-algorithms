from app.models.search_tree.search_tree import SearchTree


class Puzzle:
    def is_goal(self, state) -> bool:
        raise NotImplementedError("Subclasses should implement this method.")

    def next_moves(self, state) -> list:
        raise NotImplementedError("Subclasses should implement this method.")

    def select_priority_move(self, moves: list) -> any:
        raise NotImplementedError("Subclasses should implement this method.")

    def heuristic(self, state) -> float:
        raise NotImplementedError("Subclasses should implement this method.")

    def is_valid_state(self, state) -> bool:
        raise NotImplementedError("Subclasses should implement this method.")

    def create_search_tree(self) -> SearchTree:
        raise NotImplementedError("Subclasses should implement this method.")

    def generate_state_key(self, state) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    def get_initial_state(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def solve(self, instance) -> None:
        raise NotImplementedError("Subclasses should implement this method.")
