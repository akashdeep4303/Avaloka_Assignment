# Assignment: LRU Cache and Event Scheduler

This assignment contains two Python implementations: a least-recently-used
(LRU) cache and utilities for checking event conflicts and assigning rooms.

## Contents

- `lru_cache.py` implements `LRUCache`, using a hash map and a doubly linked
  list to support `get` and `put` in O(1) time.
- `event_scheduler.py` implements `can_attend_all`, `min_rooms_required`, and
  `assign_rooms` for events represented as `(start, end)` pairs.
- `test_assignment.py` contains tests for the cache and scheduler.

## Usage

```python
from event_scheduler import assign_rooms, can_attend_all, min_rooms_required
from lru_cache import LRUCache

cache = LRUCache(2)
cache.put(1, 100)
print(cache.get(1))  # 100
print(cache.get(2))  # -1 (not found)

events = [(9, 10), (9, 11), (11, 12)]
print(can_attend_all(events))       # False
print(min_rooms_required(events))   # 2
print(assign_rooms(events))
```

`LRUCache(capacity)` accepts a non-negative capacity. `get(key)` returns the
value and refreshes the entry's recency, or returns `-1` when the key is absent.
`put(key, value)` inserts or updates an entry; when full, the least recently
used entry is evicted.

Events may share an endpoint: an event ending at time `t` does not overlap one
starting at time `t`. `can_attend_all` reports whether all events can be
attended by one person. `min_rooms_required` returns the minimum number of
rooms needed. `assign_rooms` returns `(event, room_name)` pairs in the same
order as the input and reuses rooms when available. An event whose end is
earlier than its start raises `ValueError`.

## Run the tests

From the project directory, run the built-in test runner (no additional
packages required):

```sh
python -m pytest -q
```

Alternatively, if `pytest` is installed:

```sh
python test_assignment.py
```
