"""
Embedding-based entity clustering using Union-Find.
"""

from knowledge.similarity import combined_similarity

# ------------------------------------------------------------
# Union Find
# ------------------------------------------------------------


class UnionFind:
    """
    Disjoint Set Union.
    """

    def __init__(self, n):

        self.parent = list(range(n))

        self.rank = [0] * n

    def find(self, x):

        if self.parent[x] != x:

            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, a, b):

        root_a = self.find(a)

        root_b = self.find(b)

        if root_a == root_b:
            return

        if self.rank[root_a] < self.rank[root_b]:

            self.parent[root_a] = root_b

        elif self.rank[root_a] > self.rank[root_b]:

            self.parent[root_b] = root_a

        else:

            self.parent[root_b] = root_a

            self.rank[root_a] += 1


# ------------------------------------------------------------
# Cluster entities
# ------------------------------------------------------------


def cluster_entities(
    entities,
    threshold=0.88,
):
    """
    Cluster entities using pairwise similarity.

    Parameters
    ----------
    entities : list

        [
            {
                "name": ...,
                "type": ...,
                "embedding": [...]
            }
        ]

    Returns
    -------
    list[list]
    """

    n = len(entities)

    uf = UnionFind(n)

    for i in range(n):

        for j in range(i + 1, n):

            score = combined_similarity(
                entities[i],
                entities[j],
            )

            if score >= threshold:

                uf.union(i, j)

    clusters = {}

    for i in range(n):

        root = uf.find(i)

        if root not in clusters:

            clusters[root] = []

        clusters[root].append(entities[i])

    return list(clusters.values())
