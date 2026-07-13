# Third-party imports
import networkx as nx


def build_graph(chunk_entities, chunks):
    """Build a bipartite knowledge graph from text chunks and entities."""

    graph = nx.Graph()

    # Process each text chunk
    for chunk, chunk_data in zip(chunks, chunk_entities):

        chunk_node = f"chunk_{chunk['chunk_id']}"

        # Add the chunk as a graph node
        graph.add_node(
            chunk_node,
            node_type="chunk",
            chunk_id=chunk["chunk_id"],
            section_id=chunk["section_id"],
            text=chunk["text"],
        )

        # Add entities connected to this chunk
        for entity in chunk_data["entities"]:

            entity_name = entity["name"]

            # Add the entity if it does not already exist
            if not graph.has_node(entity_name):

                graph.add_node(
                    entity_name,
                    node_type="entity",
                    entity_type=entity["type"],
                )

            # Connect the chunk to the entity
            graph.add_edge(
                chunk_node,
                entity_name,
            )

    return graph
