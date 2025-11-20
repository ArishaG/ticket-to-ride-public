import json
from typing import List, Set, Tuple, Dict

from path_finding import PathFinder, RouteInfo


class TicketToRide:
    def __init__(self) -> None:
        self.path_finder = PathFinder(is_directed=False)
        self._load_map_data()

    def get_minimum_path_for_ticket(self, start: int, finish: int) -> RouteInfo:
        return self.path_finder.get_minimum_path(start, finish)

    
    def _load_map_data(self):
        with open("game_city_locations.json", "r", encoding="utf-8") as file_data:
            path_data = json.loads(file_data.read())
            for node in path_data["cities"]:
                self.path_finder.add_node(node["id"], node["name"], node["location"])

                city_name_to_id = {node["name"]: node["id"] for node in path_data["cities"]}

            # TODO: Update load_map_data to load the tracks into your graph
            # Use the example for cities above, and open game_city_locations.json to see the fields for "tracks"
            # IMPORTANT: TicketToRide is an undirected graph, so add edges accordingly!
            for edge in path_data["tracks"]:
                id1 = city_name_to_id[edge["city_1"]]
                id2 = city_name_to_id[edge["city_2"]]
                self.path_finder.add_edge(id1, id2, edge["distance"])
                self.path_finder.add_edge(id2, id1, edge["distance"])