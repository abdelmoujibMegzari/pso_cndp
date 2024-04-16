#!/usr/bin/env python3
import random
import sys
import time

from Pso import SwarmSystem
from Graph import Graph
from Pso.pso_constants import REPLACEMENT_NULL_INIT_INERTIA, SET_RANDOM_INIT
from Pso.pso_cndp_operations import REPLACEMENT_OPERATIONS


def goal_function_pairwise_connectivity_continuous(graph, position):  # normal notation
    position = [round(i) for i in position.vector]
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
    print("please input the number of swarms")
    number_of_swarms = int(input())
    print("please input the number of steps")
    number_of_steps = int(input())

    # PSO consts

    w = 0.2  # inertia
    c1 = 0.2  # cognitive
    c2 = 0.4  # social
    graph1 = Graph(0, fileName)
    print("initial Pairwise Connectivity", graph1.pairwise_connectivity())

    begin = time.time()

    swarm_system = SwarmSystem(
        number_of_nodes_to_be_deleted,
        graph1.number_of_nodes,
        lambda x: goal_function_pairwise_connectivity_continuous(graph1, x),
        number_of_swarms,
        w,
        c1,
        c2,
        lambda: random.random(),
        lambda: random.random(),
        REPLACEMENT_OPERATIONS,
        SET_RANDOM_INIT,
        REPLACEMENT_NULL_INIT_INERTIA,
        mutation=False,
    )
    swarm_system.run(
        number_of_steps, lambda x, step: step - x.more_than_10_per_cent_moving_step > 20
    )
    end = time.time()
    print(
        "exxecution time: ",
        end - begin,
    )
    print("The achieved Pairwise Connectivity:", -swarm_system.social_value)
