from Graph import Graph


def greedy2(graph: Graph, number_of_deleted_nodes, goal_function):
    _, s = graph.vertex_cover()
    while len(s) > number_of_deleted_nodes:
        keep = None
        best_value = float("-inf")
        for element in s:
            residual = graph.clone_graph()
            residual.delete_nodes(s - {element})
            val = goal_function(residual)
            if val > best_value:
                best_value = val
                keep = element
        s.remove(keep)
    return list(s)
