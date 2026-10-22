from event_scheduler import assign_rooms, can_attend_all, min_rooms_required
from lru_cache import LRUCache


def test_lru_basic() -> None:
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # evicts key 2
    assert cache.get(2) == -1
    cache.put(4, 4)  # evicts key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4


def test_lru_update_existing() -> None:
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)
    cache.put(3, 3)
    assert cache.get(1) == 10
    assert cache.get(2) == -1
    assert cache.get(3) == 3


def test_lru_get_refreshes_recency() -> None:
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)
    assert cache.get(1) == 1
    assert cache.get(2) == -1


def test_scheduler_can_attend() -> None:
    assert can_attend_all([(9, 10), (10, 11), (11, 12)]) is True
    assert can_attend_all([(9, 11), (10, 12)]) is False
    assert can_attend_all([]) is True
    assert can_attend_all([(5, 5)]) is True


def test_scheduler_min_rooms() -> None:
    assert min_rooms_required([(9, 10), (10, 11), (11, 12)]) == 1
    assert min_rooms_required([(9, 11), (10, 12)]) == 2
    assert min_rooms_required([(1, 5), (2, 6), (3, 7), (8, 9)]) == 3
    assert min_rooms_required([]) == 0
    assert min_rooms_required([(1, 2), (1, 2), (1, 2)]) == 3


def test_assign_rooms_reuses_when_possible() -> None:
    events = [(9, 10), (10, 11), (11, 12)]
    assigned = assign_rooms(events)
    rooms = {room for _, room in assigned}
    assert rooms == {"Room A"}
    assert [event for event, _ in assigned] == events

    overlapping = [(9, 11), (10, 12)]
    assigned = assign_rooms(overlapping)
    rooms = {room for _, room in assigned}
    assert rooms == {"Room A", "Room B"}


if __name__ == "__main__":
    test_lru_basic()
    test_lru_update_existing()
    test_lru_get_refreshes_recency()
    test_scheduler_can_attend()
    test_scheduler_min_rooms()
    test_assign_rooms_reuses_when_possible()
    print("All tests passed.")
