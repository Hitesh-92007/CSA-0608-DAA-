## 2. Task 1 — Algorithm design

### Approach A: iterative linear search

**Strategy:** sequential search. Inspect records in their existing order and stop at the first matching registration number. No preprocessing is required. It is useful as a simple baseline and works even when the data is unsorted.

```text
LINEAR-SEARCH(records, target)
    for each record in records
        if record.registration_number = target
            return record
    return NOT_FOUND
```

### Approach B: recursive binary search

**Strategy:** divide and conquer. Sort records by registration number once, compare the target with the middle record, and recursively continue in only the half that can contain the target. The sorted copy is required preprocessing. This approach is selected to investigate logarithmic search after ordering the data.

```text
RECURSIVE-BINARY-SEARCH(sorted_records, target, low, high)
    if low > high
        return NOT_FOUND
    middle = floor((low + high) / 2)
    if sorted_records[middle].registration_number = target
        return sorted_records[middle]
    if target < sorted_records[middle].registration_number
        return RECURSIVE-BINARY-SEARCH(sorted_records, target, low, middle - 1)
    return RECURSIVE-BINARY-SEARCH(sorted_records, target, middle + 1, high)
```

### Approach C: hash-table lookup

**Strategy:** hashing/indexing. Build a map from each registration number to its record, then use the key to retrieve the record directly. Index construction is preprocessing. It is selected because the application performs many exact-key lookups and the records change infrequently.

```text
BUILD-HASH-INDEX(records)
    index = empty hash table
    for each record in records
        index[record.registration_number] = record
    return index

HASH-LOOKUP(index, target)
    return index.get(target, NOT_FOUND)
```

The three strategies are different: sequential scanning, divide-and-conquer on ordered data, and key indexing by hashing. The implementation is in [`student_record_search.py`](../Task_8_Implementation_Testing/Source_Code/student_record_search.py).

See the [complete assignment report](../Report/Documentation/CO1_Assignment_Report.md) for the full analysis and evidence.
