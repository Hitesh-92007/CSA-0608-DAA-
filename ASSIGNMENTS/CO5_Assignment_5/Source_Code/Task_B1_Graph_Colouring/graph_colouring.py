"""Instrumented backtracking for the graph-colouring task."""
from dataclasses import dataclass


@dataclass
class SearchStats:
    nodes_visited: int = 0
    candidate_assignments: int = 0
    rejected_candidates: int = 0
    backtracks: int = 0
    maximum_depth: int = 0


def colour_graph(vertex_count, edges, colour_count, use_dsatur=False):
    """Return (colouring, stats); colouring is None when no assignment exists.

    DSATUR ordering chooses the uncoloured vertex with the most distinct
    neighbouring colours, then the highest degree, then the lowest index.
    """
    if vertex_count < 0 or colour_count < 0:
        raise ValueError("vertex_count and colour_count must be non-negative")
    adjacency = [set() for _ in range(vertex_count)]
    for u, v in edges:
        if not (0 <= u < vertex_count and 0 <= v < vertex_count):
            raise ValueError("edge endpoint is outside the vertex range")
        if u == v:
            raise ValueError("self-loops cannot be coloured")
        adjacency[u].add(v)
        adjacency[v].add(u)

    colours = [-1] * vertex_count
    stats = SearchStats()
    fixed_order = list(range(vertex_count))

    def select_vertex(depth):
        if not use_dsatur:
            return fixed_order[depth]
        uncoloured = [v for v in range(vertex_count) if colours[v] == -1]
        return min(
            uncoloured,
            key=lambda v: (
                -len({colours[n] for n in adjacency[v] if colours[n] != -1}),
                -len(adjacency[v]),
                v,
            ),
        )

    def search(depth):
        stats.nodes_visited += 1
        stats.maximum_depth = max(stats.maximum_depth, depth)
        if depth == vertex_count:
            return True
        vertex = select_vertex(depth)
        for colour in range(colour_count):
            stats.candidate_assignments += 1
            if any(colours[n] == colour for n in adjacency[vertex]):
                stats.rejected_candidates += 1
                continue
            colours[vertex] = colour
            if search(depth + 1):
                return True
            colours[vertex] = -1
            stats.backtracks += 1
        return False

    if search(0):
        return colours, stats
    return None, stats


def _format_stats(stats):
    return (
        f"nodes={stats.nodes_visited}, candidates={stats.candidate_assignments}, "
        f"rejected={stats.rejected_candidates}, backtracks={stats.backtracks}, "
        f"max_depth={stats.maximum_depth}"
    )


def run_tests():
    tests = [
        ("triangle, 3 colours", 3, [(0, 1), (1, 2), (0, 2)], 3, True),
        ("K4, 3 colours", 4, list(__import__("itertools").combinations(range(4), 2)), 3, False),
        ("empty graph boundary", 0, [], 3, True),
        ("five-vertex backtracking trace", 5, [(0, 3), (0, 4), (1, 2), (2, 3), (2, 4), (3, 4)], 3, True),
    ]
    print("B1 GRAPH COLOURING TESTS (k = 3)")
    for label, n, edges, k, expected in tests:
        outcomes = []
        for heuristic in (False, True):
            colouring, stats = colour_graph(n, edges, k, use_dsatur=heuristic)
            ok = colouring is not None
            assert ok == expected, f"{label}: wrong decision"
            if ok:
                assert all(colouring[u] != colouring[v] for u, v in edges)
            outcomes.append(("DSATUR" if heuristic else "input", ok, colouring, stats))
        print(f"{label}; n={n}; edges={len(edges)}")
        for name, ok, colouring, stats in outcomes:
            print(f"  {name}: {'colourable' if ok else 'not colourable'}; "
                  f"colours={colouring}; {_format_stats(stats)}")
    print("RESULT: 4/4 graph cases passed under both selection rules")


if __name__ == "__main__":
    run_tests()
