# Third-party imports
import networkx as nx


def save_graph(graph, path):
    """Save the knowledge graph."""

    nx.write_graphml(
        graph,
        path,
    )


def load_graph(path):
    """Load the knowledge graph."""

    return nx.read_graphml(path)
