"""Retest the original module after correcting one function at a time."""
import math
import original_module as active
import corrected_module as fixes


ALERTS = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
EXPECTED_ALERTS = [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)]
BLOCKLIST = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
QUERIES = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
EXPECTED_BLOCKED = [True, True, False]
LOG, PATTERN = "FAILFAIXFAIL", "FAIL"
EVENTS = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
EXPECTED_PAIR, EXPECTED_DISTANCE = (0, 5), math.sqrt(2)


def run_stage(label):
    sorted_alerts = active.sort_alerts(ALERTS.copy())
    blocked = [active.is_blocked(BLOCKLIST, ip) for ip in QUERIES]
    hits = active.find_signature(LOG, PATTERN)
    pair, distance = active.closest_logins(EVENTS)
    checks = {
        "sort": sorted_alerts == EXPECTED_ALERTS,
        "blocklist": blocked == EXPECTED_BLOCKED,
        "signature": hits == [0, 8],
        "closest": pair == EXPECTED_PAIR and abs(distance - EXPECTED_DISTANCE) < 1e-12,
    }
    print(label)
    print(f"  sort:      {'PASS' if checks['sort'] else 'FAIL'} {sorted_alerts}")
    print(f"  blocklist: {'PASS' if checks['blocklist'] else 'FAIL'} {blocked}")
    print(f"  signature: {'PASS' if checks['signature'] else 'FAIL'} {hits}")
    print(f"  closest:   {'PASS' if checks['closest'] else 'FAIL'} {pair}, {distance:.4f} km")
    return checks


def main():
    run_stage("Stage 0 - original module")
    active.sort_alerts = fixes.sort_alerts
    run_stage("Stage 1 - repair and retest sort_alerts")
    active.is_blocked = fixes.is_blocked
    run_stage("Stage 2 - repair and retest is_blocked")
    active.find_signature = fixes.find_signature
    run_stage("Stage 3 - repair and retest find_signature")
    active.closest_logins = fixes.closest_logins
    final = run_stage("Stage 4 - repair and retest closest_logins")
    if not all(final.values()):
        raise SystemExit("A corrected sample function did not pass.")


if __name__ == "__main__":
    main()
