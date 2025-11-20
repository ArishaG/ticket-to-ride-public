from math import sqrt
import sys
from typing import Dict, List, Set, Tuple
from priority_queue import PriorityQueue
from graph_base_class import Edge

# You do not need to change this class.  It is used as the return type for get_minimum_path
class RouteInfo:
    def __init__(self, 
                 route: List[Tuple[str, str]], # list of tuples of friendly names for the start and destination cities
                 route_ids: List[Tuple[int, int]], # list of tuples of ids for the start and destination cities
                 cost: int) -> None: # the total cost of the route from start to destination
        self.route = route
        self.route_ids = route_ids
        self.cost = cost

# TODO: Implement the methods on the PathFinder class using an underlying graph representation
# of your choice. Feel free to use your graph classes from the practice exercises; copy the appropriate
# files into your project and import the classes at the top of this file.
# NOTE: You can assume that graphs are directed
class PathFinder:
    def __init__(self, is_directed:bool) -> None:
        self.edges: Dict[int, Set[Edge]] = {}
        self.node_info: Dict[int, Tuple[str, Tuple[float, float]]] = {}

    # TODO: adds an edge to the graph, using a the id of the start node and id of the finish node
    # NOTE: You can assume that graphs are directed and do not have to add multiple edges here (extra edges should be added by the caller)
    def add_edge(self, start_id: int, finish_id:int , cost: float) -> None:
        edge = Edge(start_id, finish_id, cost)
        
        if start_id not in self.edges:
            self.edges[start_id] = set()
        
        if finish_id not in self.edges:
            self.edges[finish_id] = set()

        self.edges[start_id].add(edge)
    

    # TODO: adds a node to the graph, passing in the id, friendly name, and location of the node.
    # location is a tuple with the x and y coordinates of the location
    def add_node(self, id: int, name: str, location: Tuple[float, float]) -> None:
        if id not in self.node_info:
            self.node_info[id] = (name, location)

    # TODO: calculates the minimum path using the id of the start city and id of the destination city, using A*
    # Returns a RouteInfo object that contains the edges for the route.  See RouteInfo above for attributes
    # Note: This implementation must use A* to get full credit. 
    def get_minimum_path(self, start_city_id: int, destination_id: int) -> RouteInfo:
        frontier = PriorityQueue()
        frontier.enqueue(0, start_city_id)

        came_from: Dict[int, int] = {}
        cost_so_far: Dict[int, float] = {start_city_id: 0}

        while not frontier.is_empty():
            current_id = frontier.dequeue()

            if current_id == destination_id:
                
                current = destination_id
                path_ids: List[Tuple[int, int]] = []

                while current != start_city_id:
                    prev = came_from[current]
                    path_ids.append((prev, current))
                    current = prev

                path_ids.reverse()
                path_names: List[Tuple[str, str]] = [
                    (self.node_info[start][0], self.node_info[end][0]) for start, end in path_ids
                ]

                return RouteInfo(route=path_names, route_ids=path_ids, cost=cost_so_far[destination_id])

            for edge in self.edges.get(current_id, set()):
                neighbor_id = edge.finish
                new_cost = cost_so_far[current_id] + edge.weight

                if neighbor_id not in cost_so_far or new_cost < cost_so_far[neighbor_id]:
                    cost_so_far[neighbor_id] = new_cost

                    
                    loc1 = self.node_info[neighbor_id][1]
                    loc2 = self.node_info[destination_id][1]
                    heuristic = sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)

                    priority = new_cost + heuristic
                    frontier.enqueue(priority, neighbor_id)
                    came_from[neighbor_id] = current_id

        raise Exception("Path not found.")