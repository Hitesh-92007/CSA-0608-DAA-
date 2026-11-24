"""Same-size graph instances with very different backtracking effort."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "Task_B1_Graph_Colouring"))
from graph_colouring import colour_graph, _format_stats  # noqa: E402


def main():
    # Both graphs have six vertices and use three colours.
    easy = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
    # A wheel: an odd 5-cycle around a hub. It needs four colours.
    difficult = [(0, v) for v in range(1, 6)] + [
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 1)
    ]
    cases = [("A: six-vertex path", easy, True),
             ("B: odd wheel W6", difficult, False)]
    print("B2 ADVERSARIAL COMPARISON (n = 6, k = 3)")
    for label, edges, expected in cases:
        print(f"{label}; edges={len(edges)}")
        for heuristic in (False, True):
            colouring, stats = colour_graph(6, edges, 3, use_dsatur=heuristic)
            assert (colouring is not None) == expected
            print(f"  {'DSATUR' if heuristic else 'input order'}: "
                  f"{'colourable' if colouring is not None else 'not colourable'}; "
                  f"{_format_stats(stats)}")
    print("RESULT: same vertex count; the odd-wheel structure causes more search")


if __name__ == "__main__":
    main()
