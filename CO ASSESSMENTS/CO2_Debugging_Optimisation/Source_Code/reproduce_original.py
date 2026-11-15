"""Run the supplied test data against the original, defective functions."""
from original_module import closest_logins, find_signature, is_blocked, sort_alerts


ALERTS = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
BLOCKLIST = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
QUERIES = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
LOG, PATTERN = "FAILFAIXFAIL", "FAIL"
EVENTS = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]


def main():
    alerts = ALERTS.copy()
    print("Original program on the supplied data")
    print("Sort expected:", [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)])
    print("Sort actual:  ", sort_alerts(alerts))
    print("Blocklist expected:", [True, True, False])
    print("Blocklist actual:  ", [is_blocked(BLOCKLIST, ip) for ip in QUERIES])
    print("Signature expected:", [0, 8])
    print("Signature actual:  ", find_signature(LOG, PATTERN))
    pair, distance = closest_logins(EVENTS)
    print("Closest expected:  (0, 5), 1.4142 km")
    print(f"Closest actual:    {pair}, {distance:.4f} km")


if __name__ == "__main__":
    main()
