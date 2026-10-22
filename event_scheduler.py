"""
Problem 2: Event Scheduler

Events are (start, end) pairs. Adjacent events that touch at an endpoint
(end == next start) are allowed and are not treated as overlaps.
"""

from __future__ import annotations

import heapq
from typing import List, Sequence, Tuple

Event = Tuple[int, int]


def _valid_events(events: Sequence[Event]) -> List[Event]:
    cleaned: List[Event] = []
    for start, end in events:
        if end < start:
            raise ValueError(f"invalid event ({start}, {end}): end is before start")
        cleaned.append((start, end))
    return cleaned


def can_attend_all(events: Sequence[Event]) -> bool:
    """True if one person can attend every event with no overlap."""
    if not events:
        return True

    ordered = sorted(_valid_events(events), key=lambda e: (e[0], e[1]))
    previous_end = ordered[0][1]
    for start, end in ordered[1:]:
        if start < previous_end:
            return False
        previous_end = end
    return True


def min_rooms_required(events: Sequence[Event]) -> int:
    """
    Minimum rooms needed so every event can run.

    Sweep the timeline: increment a counter at each start, decrement at
    each end. Because touching events are allowed, ends are processed
    before starts at the same timestamp.
    """
    if not events:
        return 0

    cleaned = _valid_events(events)
    starts = sorted(start for start, _ in cleaned)
    ends = sorted(end for _, end in cleaned)

    rooms = 0
    peak = 0
    i = 0
    j = 0
    n = len(cleaned)

    while i < n:
        if starts[i] < ends[j]:
            rooms += 1
            peak = max(peak, rooms)
            i += 1
        else:
            # start == end or start > end: a room frees first
            rooms -= 1
            j += 1

    return peak


def assign_rooms(events: Sequence[Event]) -> List[Tuple[Event, str]]:
    """
    Future-proofing helper: assign a named room to each event.

    Returns a list aligned with the original input order:
    [((start, end), "Room A"), ...]
    """
    cleaned = _valid_events(events)
    if not cleaned:
        return []

    indexed = sorted(enumerate(cleaned), key=lambda item: (item[1][0], item[1][1], item[0]))

    # available: min-heap of freed room indexes
    available: List[int] = []
    # occupied: min-heap of (end_time, room_index)
    occupied: List[Tuple[int, int]] = []
    room_count = 0
    assignment_by_index = [""] * len(cleaned)

    def room_name(index: int) -> str:
        # Room A, Room B, ... Room Z, Room AA, ...
        n = index + 1
        letters: List[str] = []
        while n:
            n, rem = divmod(n - 1, 26)
            letters.append(chr(ord("A") + rem))
        return "Room " + "".join(reversed(letters))

    for original_index, (start, end) in indexed:
        while occupied and occupied[0][0] <= start:
            _, freed = heapq.heappop(occupied)
            heapq.heappush(available, freed)

        if available:
            room_index = heapq.heappop(available)
        else:
            room_index = room_count
            room_count += 1

        heapq.heappush(occupied, (end, room_index))
        assignment_by_index[original_index] = room_name(room_index)

    return [(cleaned[i], assignment_by_index[i]) for i in range(len(cleaned))]
