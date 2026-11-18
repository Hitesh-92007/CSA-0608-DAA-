"""Greedy job sequencing with deadlines; one unit-time slot per job."""
def schedule_jobs(jobs):
    if any(d < 1 for _, d, _ in jobs): raise ValueError("Deadlines must be positive")
    slots = [None] * max((d for _, d, _ in jobs), default=0)
    trace, total = [], 0
    for job, deadline, profit in sorted(jobs, key=lambda x: (-x[2], x[0])):
        placed = None
        for t in range(min(deadline, len(slots)) - 1, -1, -1):
            if slots[t] is None:
                slots[t] = job; placed = t + 1; total += profit; break
        trace.append((job, deadline, profit, placed))
    return slots, total, trace

def main():
    jobs = [("A",2,80),("B",1,35),("C",2,60),("D",3,40),("E",1,25)]
    slots, total, trace = schedule_jobs(jobs)
    print("CO4A Task 2: Job sequencing")
    for j,d,p,s in trace: print(f"{j}: profit={p}, deadline={d} -> slot {s if s else 'rejected'}")
    print("Schedule:", slots); print("Maximum profit:", total)
    assert total == 180 and slots == ["C", "A", "D"]
    assert schedule_jobs([])[1] == 0
    changed=[("A",1,80),("B",1,35),("C",2,60),("D",3,40),("E",1,25)]
    changed_slots,changed_total,_=schedule_jobs(changed)
    print("Changed case (A deadline 1):",changed_slots,"profit:",changed_total)
    assert changed_slots == ["A","C","D"] and changed_total==180
    print("Checks: passed (given instance, empty input, changed deadline)")

if __name__ == "__main__": main()
