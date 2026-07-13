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
        "nos_visitados",
        "nos_explorados",
        "fator_medio_ramificacao",
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

        if not should_write_header:
            self.__migrate_result_file(path)

        with path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.result_fieldnames)

            if should_write_header:
                writer.writeheader()

            writer.writerows(results)

    def __migrate_result_file(self, path: Path) -> None:
        with path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            current_fieldnames = tuple(reader.fieldnames or ())

            if current_fieldnames == self.result_fieldnames:
                return

            unknown_fieldnames = set(current_fieldnames) - set(self.result_fieldnames)
            if unknown_fieldnames:
                unknown_fields = ", ".join(sorted(unknown_fieldnames))
                raise ValueError(
                    f"The result CSV contains unknown columns: {unknown_fields}"
                )

            rows = list(reader)

        temporary_path = path.with_name(f".{path.name}.tmp")

        try:
            with temporary_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.result_fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            temporary_path.replace(path)
        finally:
            temporary_path.unlink(missing_ok=True)

    def solve(self, instance) -> None:
        raise NotImplementedError("Subclasses should implement this method.")
