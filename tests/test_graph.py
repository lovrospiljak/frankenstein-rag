from knowledge.graph_storage import load_graph

GRAPH_PATH = "data/processed/graph.graphml"


def main():
    """Load and inspect the knowledge graph."""

    graph = load_graph(GRAPH_PATH)

    print()

    print(f"Nodes : {graph.number_of_nodes()}")
    print(f"Edges : {graph.number_of_edges()}")

    print()

    print("First 10 nodes:\n")

    for node in list(graph.nodes())[:10]:
        print(node)

    print()

    print("Victor:", graph.has_node("Victor"))
    print("Victor Frankenstein:", graph.has_node("Victor Frankenstein"))
    print("Frankenstein:", graph.has_node("Frankenstein"))


if __name__ == "__main__":
    main()
