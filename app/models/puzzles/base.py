import csv
from pathlib import Path

from app.models.search_tree.search_tree import SearchTree


class Puzzle:
    result_fieldnames = (
        "nome_instancia",
        "nome_algoritmo",
        "caminho_solucao",
        "custo_solucao",
        "profundidade_solucao",
        "tempo_execucao_segundos",
    )

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

    def save_results_to_csv(self, results: list[dict], output_path: str) -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        should_write_header = not path.exists() or path.stat().st_size == 0

        with path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.result_fieldnames)

            if should_write_header:
                writer.writeheader()

            writer.writerows(results)

    def solve(self, instance) -> None:
        raise NotImplementedError("Subclasses should implement this method.")
