import sys
import numpy as np
from math import sqrt
from pandas import read_csv
from networkx import DiGraph

sys.path.append("../../")
sys.path.append("../../../cspy")
from vrpy.main import VehicleRoutingProblem

import logging

logger = logging.getLogger(__name__)


class SolomonNode:
    """Stores attributes of a node of Solomon's instances."""

    def __init__(self, values):
        # Node ID
        self.name = np.uint32(values[1]).item()
        if self.name == 0:
            self.name = "Source"
        # x coordinate
        self.x = np.float64(values[2]).item()
        # y coordinate
        self.y = np.float64(values[3]).item()
        self.demand = np.uint32(values[4]).item()
        self.inf_time_window = np.uint32(values[5]).item()
        self.sup_time_window = np.uint32(values[6]).item()
        self.service_time = np.uint32(values[7]).item()


class DataSet:
    """Reads a Solomon instance and stores the network as DiGraph.

    Args:
        path (str) : Path to data folder.
        instance_name (str) : Name of Solomon instance to read.
        n_vertices (int, optional):
            Only first n_vertices are read.
            Defaults to None.
    """

    def __init__(self, path, instance_name, n_vertices=None):

        # Read vehicle capacity
        with open(path + instance_name) as fp:
            for i, line in enumerate(fp):
                if i == 4:
                    self.max_load = int(line.split()[1])
        fp.close()

        # Create network and store name + capacity
        self.G = DiGraph(
            name=instance_name[:-4] + "." + str(n_vertices),
            vehicle_capacity=self.max_load,
        )

        # Read nodes from txt file
        df_solomon = read_csv(
            path + instance_name,
            sep="\s+",
            skip_blank_lines=True,
            skiprows=7,
            nrows=n_vertices,
        )
        # Scan each line of the file and add nodes to the network
        for line in df_solomon.itertuples():
            node = SolomonNode(line)
            self.G.add_node(
                node.name,
                x=node.x,
                y=node.y,
                demand=node.demand,
                lower=node.inf_time_window,
                upper=node.sup_time_window,
                service_time=node.service_time,
            )
            # Add Sink as copy of Source
            if node.name == "Source":
                self.G.add_node(
                    "Sink",
                    x=node.x,
                    y=node.y,
                    demand=node.demand,
                    lower=node.inf_time_window,
                    upper=node.sup_time_window,
                    service_time=node.service_time,
                )

        # Add the edges, the graph is complete
        for u in self.G.nodes():
            if u != "Sink":
                for v in self.G.nodes():
                    if v != "Source":
                        if u != v:
                            self.G.add_edge(
                                u, v, cost=self.distance(u, v), time=self.distance(u, v)
                            )

    def distance(self, u, v):
        """2D Euclidian distance between two nodes.

        Args:
            u (Node) : tail node.
            v (Node) : head node.

        Returns:
            float : Euclidian distance between u and v
        """
        delta_x = self.G.nodes[u]["x"] - self.G.nodes[v]["x"]
        delta_y = self.G.nodes[u]["y"] - self.G.nodes[v]["y"]
        return sqrt(delta_x ** 2 + delta_y ** 2)

    def solve(
        self,
        initial_routes=None,
        num_stops=None,
        cspy=False,
        exact=False,
        pricing_strategy="PrunePaths",
        time_limit=None,
        solver="cbc",
    ):
        """Instantiates instance as VRP and solves."""
        if cspy:
            self.G.graph["subproblem"] = "cspy"
        else:
            self.G.graph["subproblem"] = "lp"
        print(self.G.graph["name"], self.G.graph["subproblem"])
        print("===========")
        prob = VehicleRoutingProblem(
            self.G, num_stops=num_stops, load_capacity=self.max_load, time_windows=True,
        )
        prob.solve(
            initial_routes=initial_routes,
            cspy=cspy,
            exact=exact,
            pricing_strategy=pricing_strategy,
            time_limit=time_limit,
            solver=solver,
        )
        self.best_value, self.best_routes = prob.best_value, prob.best_routes
