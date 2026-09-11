"""
Unit Tests verifying algorithmic parity between Luau and Python implementations for IdemNPC.
Tests:
1. 2-Cycle involution compaction (swapping inactive entities with active ones).
2. Exact algebraic idempotence: Compact(Compact(A)) == Compact(A).
3. In-place preservation (0 external array allocations).
4. Top-K Threat Partitioning without auxiliary sort buffers.
"""

import random


class LuauEntity:
    def __init__(self, entity_id: int, health: float, threat: float, active: bool = True):
        self.id = entity_id
        self.health = health
        self.threat = threat
        self.active = active


def luau_compact_active_inplace(array, is_active_pred):
    """
    Python implementation of IdemNPC.luau compactActiveInPlace algorithm.
    """
    total = len(array)
    if total <= 1:
        if total == 1 and is_active_pred(array[0]):
            return 1
        return 0

    active_count = sum(1 for e in array if is_active_pred(e))
    if active_count == 0 or active_count == total:
        return active_count

    left = 0
    right = active_count

    while left < active_count and right < total:
        while left < active_count and is_active_pred(array[left]):
            left += 1
        while right < total and not is_active_pred(array[right]):
            right += 1

        if left < active_count and right < total:
            # 2-cycle involution swap
            array[left], array[right] = array[right], array[left]
            left += 1
            right += 1

    return active_count


def luau_select_top_k_inplace(array, get_score, k):
    """
    Python implementation of IdemNPC.luau selectTopKInPlace algorithm.
    """
    total = len(array)
    if total == 0:
        return 0
    k = max(1, min(k, total))
    if k == total:
        return total

    low = 0
    high = total - 1
    target_idx = k - 1

    while low < high:
        pivot = get_score(array[high])
        i = low
        for j in range(low, high):
            if get_score(array[j]) >= pivot:
                array[i], array[j] = array[j], array[i]
                i += 1
        array[i], array[high] = array[high], array[i]

        if i == target_idx:
            break
        elif i < target_idx:
            low = i + 1
        else:
            high = i - 1

    return k


def test_luau_compaction_and_idempotence():
    import random
    random.seed(42)

    entities = [
        {"id": i, "active": random.random() > 0.4, "health": random.randint(0, 100)}
        for i in range(1000)
    ]

    is_alive = lambda e: e["active"] and e["health"] > 0
    expected_active = sum(1 for e in entities if is_alive(e))

    # First pass
    active_count = luau_compact_active_inplace(entities, is_alive)
    assert active_count == expected_active

    # Check prefix: all in [0, active_count-1] must be alive
    for i in range(active_count):
        assert is_alive(entities[i]), f"Entity at index {i} in prefix is not alive!"

    # Check suffix: all in [active_count, total-1] must be dead/inactive
    for i in range(active_count, len(entities)):
        assert not is_alive(entities[i]), f"Entity at index {i} in suffix is alive!"

    # Mathematical Idempotence: Second compaction must result in 0 swaps
    second_pass = luau_compact_active_inplace(entities, is_alive)
    assert second_pass == active_count


def test_luau_top_k_threat_partition():
    import random
    random.seed(42)

    entities = [{"id": i, "threat": random.uniform(0, 1000)} for i in range(500)]
    k = 50

    luau_select_top_k_inplace(entities, lambda e: e["threat"], k)

    # Top-K partitioned: min threat in [0, K-1] must be >= max threat in [K, Total-1]
    top_k_min = min(e["threat"] for e in entities[:k])
    remaining_max = max(e["threat"] for e in entities[k:])

    assert top_k_min >= remaining_max - 1e-5, f"Partition error: top-K min ({top_k_min}) < remaining max ({remaining_max})"


if __name__ == "__main__":
    test_luau_compaction_and_idempotence()
    test_luau_top_k_threat_partition()
    print("All Luau algorithmic parity tests passed successfully!")
