"""Functional and boundary tests for corrected and optimized algorithms."""
import math
import random
import unittest

import corrected_module as corrected
import optimized_module as optimized


class SentinelOpsTests(unittest.TestCase):
    def test_sort_order_stability_and_in_place_contract(self):
        data = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
        expected = [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)]
        original_id = id(data)
        self.assertEqual(corrected.sort_alerts(data), expected)
        self.assertEqual(id(data), original_id)
        other = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
        self.assertEqual(optimized.sort_alerts(other), expected)
        self.assertEqual(corrected.sort_alerts([]), [])
        self.assertEqual(optimized.sort_alerts([("only", 1)]), [("only", 1)])
        equal = [("first", 7), ("second", 7), ("third", 7)]
        self.assertEqual(optimized.sort_alerts(equal), [("first", 7), ("second", 7), ("third", 7)])

    def test_blocklist_and_empty_blocklist(self):
        data = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
        index = optimized.build_blocklist_index(data)
        for ip, expected in [("10.0.0.9", True), ("10.0.0.5", True),
                             ("172.16.4.2", True), ("8.8.8.8", False)]:
            self.assertEqual(corrected.is_blocked(data, ip), expected)
            self.assertEqual(optimized.is_blocked(index, ip), expected)
        self.assertFalse(corrected.is_blocked([], "8.8.8.8"))
        self.assertFalse(optimized.is_blocked(optimized.build_blocklist_index([]), "8.8.8.8"))

    def test_signature_sample_boundaries_and_overlaps(self):
        self.assertEqual(corrected.find_signature("FAILFAIXFAIL", "FAIL"), [0, 8])
        self.assertEqual(optimized.find_signature("FAILFAIXFAIL", "FAIL"), [0, 8])
        self.assertEqual(corrected.find_signature("ABC", "ABCD"), [])
        self.assertEqual(optimized.find_signature("ABCEND", "END"), [3])
        self.assertEqual(optimized.find_signature("ABC", "ABCD"), [])
        self.assertEqual(optimized.find_signature("AAAA", "AA"), [0, 1, 2])
        self.assertEqual(optimized.find_signature("ABC", ""), [0, 1, 2, 3])

    def test_closest_pair_sample_and_boundaries(self):
        events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        expected_pair, expected_distance = (0, 5), math.sqrt(2)
        self.assertEqual(corrected.closest_logins(events)[0], expected_pair)
        actual_pair, actual_distance = optimized.closest_logins(events)
        self.assertEqual(actual_pair, expected_pair)
        self.assertAlmostEqual(actual_distance, expected_distance)
        self.assertEqual(corrected.closest_logins([]), (None, math.inf))
        self.assertEqual(corrected.closest_logins([(4, 5)]), (None, math.inf))
        self.assertEqual(optimized.closest_logins([]), (None, math.inf))
        self.assertEqual(optimized.closest_logins([(2, 3)]), (None, math.inf))
        self.assertEqual(optimized.closest_logins([(0, 0), (3, 4)]), ((0, 1), 5.0))
        self.assertEqual(optimized.closest_logins([(0, 0), (1, 1), (0, 0)]), ((0, 2), 0.0))
        self.assertEqual(optimized.closest_logins([(0, 0), (1, 0), (0, 1)])[0], (0, 1))

    def test_randomized_optimized_results_match_corrected_baselines(self):
        rng = random.Random(62026)
        for _ in range(250):
            n = rng.randrange(0, 18)
            events = [(rng.randrange(-5, 6), rng.randrange(-5, 6)) for _ in range(n)]
            self.assertEqual(optimized.closest_logins(events), corrected.closest_logins(events))

        alphabet = "ABCFX"
        for _ in range(500):
            log = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 45)))
            pattern = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 12)))
            self.assertEqual(optimized.find_signature(log, pattern), corrected.find_signature(log, pattern))

        for _ in range(100):
            values = [(str(i), rng.randrange(0, 8)) for i in range(rng.randrange(0, 40))]
            a, b = values.copy(), values.copy()
            self.assertEqual(optimized.sort_alerts(a), corrected.sort_alerts(b))


if __name__ == "__main__":
    unittest.main(verbosity=2)
