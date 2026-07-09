from dataclasses import dataclass

from app.models.search_tree.search_node import SearchNode


@dataclass
class SearchTree:
    root: SearchNode
