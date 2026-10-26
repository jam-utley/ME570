import me570_graph
import numpy as np
import matplotlib as plt

def graph_search_test():
    """
    Call graph_search to find a path between the bottom left node and the
    top right node of the   graphVectorMedium graph from the
    graph_test_data_load function (see Question~ q:graph test data). Then
    use Graph.plot to visualize the result.
    """
    pass  # Substitute with your code
    # Question 1.1 REPORT
    graph = me570_graph.graph_test_data_load('graphVectorMedium')
    # loader may return raw data or a Graph
    if not isinstance(graph, me570_graph.Graph):  
        graph = me570_graph.Graph(graph)
    
    # Node coordinates as an (N, 2) array
    coords = np.array([np.asarray(v['x']).flatten() for v in graph.graph_vector])
    
    # Bottom-left / top-right = nodes nearest the bounding-box corners
    idx_start = int(np.argmin(np.linalg.norm(coords - coords.min(axis=0), axis=1)))
    idx_goal = int(np.argmin(np.linalg.norm(coords - coords.max(axis=0), axis=1)))
    
    # ASSUMED signature -- adjust to match your graph_search
    x_path = graph.search(idx_start, idx_goal)
    x_path = np.asarray(x_path)  # assumed 2 x N (one column per node)
    
    plt.figure()
    graph.plot(flag_heuristic=True, idx_goal=idx_goal)
    plt.plot(x_path[0, :], x_path[1, :], 'r-', linewidth=2, label='path')
    plt.plot(*coords[idx_start], 'gs', markersize=10, label='start')
    plt.plot(*coords[idx_goal], 'r*', markersize=14, label='goal')
    plt.legend()
    plt.title(f'graphVectorMedium: node {idx_start} -> node {idx_goal}')
    plt.show()
