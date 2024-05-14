import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class Graph:
	"""Graph class to represent a graph using the adjacency matrix and features

    :param adj_matrix: Adjacency matrix of the graph of shape (n, n) where n is the number of nodes in the graph
    :type adj_matrix: np.ndarray
    :param edge_index: Edge index of the graph of shape (2, e) where e is the number of edges in the graph
    :type edge_index: np.ndarray
    :param edge_weight: Edge weight of the graph of shape (e,) where e is the number of edges in the graph
    :type edge_weight: np.ndarray
    :param directed: Boolean flag to indicate if the graph is directed or undirected
    :type directed: bool
    :param graph: NetworkX graph object
    :type graph: nx.Graph | nx.DiGraph
    :param features: Features of the nodes in the graph of shape (n, f) where f is the number of features per node
    :type features: np.ndarray

    """

	def __init__(self, adj_matrix: np.ndarray, directed: bool = False, features: np.ndarray = None):
		"""Constructor method
		"""
		self.adj_matrix: np.ndarray = adj_matrix
		self.edge_index: np.ndarray = np.argwhere(adj_matrix).transpose()
		self.edge_weight: np.ndarray = adj_matrix[self.edge_index.transpose()[:, 0], self.edge_index.transpose()[:, 1]]
		self.directed: bool = directed
		self.graph: nx.Graph | nx.DiGraph = nx.DiGraph() if directed else nx.Graph()
		self._create_nx_graph()

		self.features: np.ndarray = features if features is not None else np.ones((adj_matrix.shape[0], 1))

	def _create_nx_graph(self) -> None:
		"""Adds nodes and edges to the NetworkX graph object
		"""
		self.graph.add_nodes_from(range(self.features.shape[0]), features=self.features)
		self.graph.add_edges_from(self.edge_index.transpose())
		for i, (u, v) in enumerate(self.edge_index.transpose()):
			self.graph[u][v]['weight'] = self.edge_weight[i]

	def draw(self) -> None:
		"""Draws the graph using the NetworkX draw method
		"""
		pos = nx.spring_layout(self.graph)
		nx.draw_networkx_nodes(self.graph, pos, node_size=700)
		nx.draw_networkx_edges(self.graph, pos)
		nx.draw_networkx_labels(self.graph, pos)
		plt.show()

	def __str__(self):
		"""Returns the string representation of the graph object
		:return: String representation of the graph object (number of nodes and edges)
		:rtype: str
		"""
		return f"Graph with {self.adj_matrix.shape[0]} nodes and {self.edge_index.shape[1]} edges."

	def __repr__(self):
		"""Returns the string representation of the graph object
		:return: String representation of the graph object (number of nodes and edges)
		:rtype: str
		"""
		return self.__str__()

	def __getitem__(self, key: int) -> np.ndarray:
		"""Returns the adjacency matrix of the graph for the given key
		:param key: Key to access the adjacency matrix
		:type key: int
		:return: Adjacency matrix of the graph for the given key
		:rtype: np.ndarray
		"""
		return self.adj_matrix[key]


if __name__ == "__main__":
	adj = np.array([
		[0, 1, 1, 0],
		[1, 0, 1, 1],
		[1, 1, 0, 1],
		[0, 1, 1, 0]
	])

	graph = Graph(adj, directed=False)
	nx.draw(graph.graph, with_labels=True)
	plt.show()