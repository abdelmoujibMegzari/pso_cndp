from collections import defaultdict
import random
import time

from Graph.Graph import Graph


freq = defaultdict(lambda: 0)


def shake(S, h, v):
    # Replace h most frequent nodes in S with h least frequent nodes in V \ S
    if h == 0:
        return S
    s = set(S)
    v = set(v)
    least_freq_nodes = list(v - s)
    most_freq_nodes = list(s)
    least_freq_nodes.sort(key=lambda node: freq[node])
    most_freq_nodes.sort(key=lambda node: freq[node])
    least_freq_nodes = least_freq_nodes[:h]
    most_freq_nodes = most_freq_nodes[-h:]
    new_s = (s - set(most_freq_nodes)).union(set(least_freq_nodes))
    new_S = list(new_s)
    return new_S


def first_improvement(graph: Graph, solution, goal_function):
    # Perform first improvement exploration of the neighborhood N
    best_solution = solution
    random.shuffle(
        best_solution
    )  # we first shuffle the solution to avoid local optima and add randomness
    best_f = goal_function(graph, best_solution)
    for u in solution:
        for v in graph.adjacency_list.keys():
            if v not in best_solution:
                new_S = [node if node != u else v for node in best_solution]
                new_f = goal_function(graph, new_S)
                if new_f > best_f:
                    u = v
                    best_solution = new_S
                    best_f = new_f
    return best_solution


def VNS(
    graph: Graph, goal_function, tmax, hmax, initial_solution
):  # hmax should not exeed the size of solution
    best_S = initial_solution
    best_f = goal_function(graph, best_S)
    t = 0
    while t < tmax:
        best_solution_time = time.time()
        iteration_strat_time = time.time()
        h = 2
        while h <= hmax:
            if time.time() - iteration_strat_time > 82800:
                break
            S_prime = shake(best_S, h, graph.adjacency_list.keys())
            # S_prime = best_S
            S_double_prime = first_improvement(
                graph, S_prime, goal_function
            )  # Use N1 as the neighborhood
            for node in S_double_prime:
                if node not in S_prime:
                    freq[node] += 1
            f_double_prime = goal_function(graph, S_double_prime)
            if f_double_prime > best_f:
                best_S = S_double_prime
                best_f = f_double_prime
                best_solution_time = time.time()
                h = 2
                for node in S_double_prime:
                    freq[node] += 1
            else:
                h += 1
        print("in iteration ", t, " we have got a value of ", -best_f)
        print(
            "the execution time of this iteration is: ",
            time.time() - iteration_strat_time,
        )
        print(
            "the best solution so far was found in: ",
            best_solution_time - iteration_strat_time,
        )
        t += 1
    return best_S
