from collections import defaultdict



def compute_elimination_order(bnet):
    """Computes a low-width elimination order for a Bayesian network.

    YOU DO NOT NEED TO UNDERSTAND HOW THIS FUNCTION WORKS.

    Parameters
    ----------
    bnet : BayesianNetwork
        the Bayesian network for which to compute the elimination order

    Returns
    -------
    list[str]
        the elimination order (a list of the variables of the Bayesian network)
    """

    def build_moral_graph(bnet):
        node_labels = [var for var in bnet.variables]
        edges = []
        for factor in bnet.factors:
            vars = [v for v in factor.variables]
            for i, var in enumerate(vars):
                edges += [(var, neighbor) for neighbor in vars[:i] + vars[i + 1:]]
        return UndirectedGraph(len(node_labels), edges, node_labels)

    def min_degree_elim_order(moral_graph):
        def min_degree_node(adjacency):
            best, best_degree = None, float("inf")
            for node in adjacency:
                if len(adjacency[node]) < best_degree:
                    best, best_degree = node, len(adjacency[node])
            return best

        adjacencies = moral_graph.get_adjacencies()
        elim_order = []
        while len(adjacencies) > 0:
            min_degree = min_degree_node(adjacencies)
            adjacencies = {n: adjacencies[n] - {min_degree} for n in adjacencies if n != min_degree}
            elim_order.append(min_degree)
        return elim_order
    moral_graph = build_moral_graph(bnet)
    return min_degree_elim_order(moral_graph), moral_graph


class UndirectedGraph:
    """A undirected graph."""

    def __init__(self, num_nodes, edges, node_labels=None):
        self.num_nodes = num_nodes
        if node_labels is None:
            node_labels = [None for _ in range(num_nodes)]
        self.node_labels = node_labels
        self.adjacency = defaultdict(set)
        for (node1, node2) in edges:
            self.adjacency[node1].add(node2)
            self.adjacency[node2].add(node1)
        self.adjacency = dict(self.adjacency)

    def get_neighbors(self, node):
        return list(self.adjacency[node])

    def is_leaf(self, node):
        return len(self.get_neighbors(node)) == 1

    def are_adjacent(self, node1, node2):
        return node2 in self.adjacency[node1]

    def get_adjacencies(self):
        return self.adjacency

    def get_num_nodes(self):
        return self.num_nodes

    def get_node_label(self, index):
        return self.node_labels[index]

    def prune_leaf(self, index):
        assert self.is_leaf(index)
        new_edges = []
        for (x, y) in self.get_edges():
            if x != index and y != index:
                new_edge = [x, y]
                if x > index:
                    new_edge[0] -= 1
                if y > index:
                    new_edge[1] -= 1
                new_edges.append(tuple(new_edge))
        return UndirectedGraph(self.num_nodes-1, new_edges, self.node_labels[:index] + self.node_labels[index+1:])

    def get_edges(self):
        result = set()
        for node in self.adjacency:
            for neighbor in self.adjacency[node]:
                edge = tuple(sorted([node, neighbor]))
                result.add(edge)
        return sorted(result)

    def sprout_leaf(self, node, node_label=None):
        new_node = self.num_nodes
        new_edge = (new_node, node)
        return new_node, UndirectedGraph(self.num_nodes+1,
                                         self.get_edges() + [new_edge],
                                         self.node_labels + [node_label])


    def __str__(self):
        return str(self.get_edges())

