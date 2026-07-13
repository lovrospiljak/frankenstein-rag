def graph_to_text(graph):
    """Convert a graph into prompt text."""

    lines = []

    # Describe graph nodes
    for node, data in graph.nodes(data=True):

        lines.append(f"{node} ({data['entity_type']})")

    lines.append("")

    # Describe graph edges
    for source, target, data in graph.edges(data=True):

        lines.append(f"{source} -- {target}")

    return "\n".join(lines)
