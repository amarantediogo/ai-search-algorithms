from app.models.puzzles.base import Puzzle


class Algorithm:
    name: str

    @staticmethod
    def search(problem: Puzzle):
        raise NotImplementedError("Subclasses should implement this method.")
