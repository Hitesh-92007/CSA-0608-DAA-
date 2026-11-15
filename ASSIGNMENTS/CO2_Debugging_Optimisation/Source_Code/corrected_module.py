"""Minimal correctness fixes to the four algorithms in the question."""
import math


def sort_alerts(alerts):
    """Stable insertion sort by descending severity; mutates and returns alerts."""
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j >= 0 and alerts[j][1] < key[1]:
            alerts[j + 1] = alerts[j]
            j -= 1
        alerts[j + 1] = key
    return alerts


def is_blocked(blocklist, ip):
    """Return True exactly when ip occurs in the blocklist (linear search)."""
    for address in blocklist:
        if address == ip:
            return True
    return False


def find_signature(log, pattern):
    """Return every start offset of pattern, including overlaps and end matches."""
    n, m = len(log), len(pattern)
    hits = []
    for start in range(n - m + 1):
        matched = True
        for offset in range(m):
            if log[start + offset] != pattern[offset]:
                matched = False
                break
        if matched:
            hits.append(start)
    return hits


def closest_logins(events):
    """Correct the original all-pairs method while retaining its simple structure."""
    if len(events) < 2:
        return None, math.inf

    min_dist = math.inf
    pair = None
    for i in range(len(events)):
        for j in range(len(events)):
            if i == j:
                continue
            dx = events[i][0] - events[j][0]
            dy = events[i][1] - events[j][1]
            distance = math.sqrt(dx * dx + dy * dy)
            candidate = (min(i, j), max(i, j))
            if distance < min_dist or (distance == min_dist and candidate < pair):
                min_dist = distance
                pair = candidate
    return pair, min_dist
