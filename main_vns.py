#!/usr/bin/env python3

import random
import sys

from greedy_CNDP import greedy2
from Graph.Graph import Graph
from vns import VNS
import time


def goal_function_pairwise_connectivity_continuous(graph, position):
    position = [round(i) for i in position]
    graph_copy = graph.clone_graph()
    graph_copy.delete_nodes(position)
    return -graph_copy.pairwise_connectivity()


if __name__ == "__main__":
    seed1 = random.randrange(sys.maxsize)
    # seed1 = 8908450424969941461
    random.seed(seed1)
    print("seed:", seed1)

    # problem input

    print("please input graph file name")
    fileName = input()
    print("please input the number of nodes to be deleted")
    number_of_nodes_to_be_deleted = int(input())
    print("please input tmax")
    t_max = int(input())
    print("please input h_max")
    h_max = int(input())
    graph1 = Graph(0, fileName)
    print("original pairwise connectivity", graph1.pairwise_connectivity())

    start_time = time.time()
    greedy_solution = greedy2(
        graph1, number_of_nodes_to_be_deleted, lambda x: -x.pairwise_connectivity()
    )
    print("the greedy solution is:", greedy_solution)
    print(
        "The pairwise connectivity of the greedy solution is:",
        -goal_function_pairwise_connectivity_continuous(graph1, greedy_solution),
    )
    print("the greedy solution execution time is:", (time.time() - start_time))
    best_solution = VNS(
        graph1,
        goal_function_pairwise_connectivity_continuous,
        t_max,
        h_max,
        greedy_solution,
    )
    print("the VNS solution is: ", best_solution)
    print(
        "the pairwise connectivity of the VNS solution is",
        -goal_function_pairwise_connectivity_continuous(graph1, best_solution),
    )
    print("the VNS solution execution time is:", (time.time() - start_time))
