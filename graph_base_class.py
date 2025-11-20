from abc import ABC, abstractmethod
from typing import Set


class Edge:
    def __init__(self, start, finish, weight) -> None:
        self.start = start
        self.finish = finish
        self.weight = weight

class GraphBaseClass(ABC):
    def __init__(self, is_directed: bool) -> None:
        self.is_directed = is_directed
        self.adjacency_list = {}
        super().__init__()

    @abstractmethod
    def add_node(self, name:any) -> None:
        if name not in self.adjacency_list:
            self.adjacency_list[name] = {}

    @abstractmethod
    def remove_node(self, name:any) -> None:
        if name in self.adjacency_list:
            del self.adjacency_list[name]
        for neighbors in self.adjacency_list.values():
            if name in neighbors:
                del neighbors[name]

    @abstractmethod
    # return True if the node name1 is connected to the node name2 and False otherwise
    def is_connected(self, name1:any, name2:any) -> bool:
        return name2 in self.adjacency_list.get(name1, {})

    @abstractmethod
    def add_edge(self, start:any, finish:any, weight:int) -> None:
        self.add_node(start)
        self.add_node(finish)
        self.adjacency_list[start][finish] = weight
        if not self.is_directed:
            self.adjacency_list[finish][start] = weight

    @abstractmethod
    # Returns a set of node names adjacent to the given node (i.e. there's an arc from the node to the neighbor)
    def get_neighbors(self, name:any) -> Set[any]:
        return set(self.adjacency_list.get(name, {}).keys())
    
    @abstractmethod
    # Gets a set of arcs leading out of the given node
    def get_edges(self, name:any) -> Set[Edge]:
        edges = set()
        for neighbor, weight in self.adjacency_list.get(name, {}).items():
            edges.add(Edge(name, neighbor, weight))
        return edges
    
    @abstractmethod
    # Gets a set of arcs leading out of the given node
    def get_nodes(self, name:str) -> Set[str]:
        return set(self.adjacency_list.keys())