"""
Problem 1: LRU Cache

get(key) and put(key, value) both run in O(1) time by combining:
  - a hash map for instant node lookup
  - a doubly linked list that stores recency order
"""

from __future__ import annotations

from typing import Dict, Optional


class _Node:
    """A doubly linked list node holding one cache entry."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int, value: int) -> None:
        self.key = key
        self.value = value
        self.prev: Optional[_Node] = None
        self.next: Optional[_Node] = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        self.capacity = capacity
        self.map: Dict[int, _Node] = {}

        # Sentinel nodes so insert/remove never need None checks.
        self.head = _Node(0, 0)  # most recently used sits after head
        self.tail = _Node(0, 0)  # least recently used sits before tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        self._move_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return

        node = self.map.get(key)
        if node is not None:
            node.value = value
            self._move_to_front(node)
            return

        if len(self.map) == self.capacity:
            lru = self.tail.prev
            assert lru is not None and lru is not self.head
            self._remove(lru)
            del self.map[lru.key]

        new_node = _Node(key, value)
        self.map[key] = new_node
        self._insert_after_head(new_node)

    def _insert_after_head(self, node: _Node) -> None:
        first = self.head.next
        node.prev = self.head
        node.next = first
        self.head.next = node
        if first is not None:
            first.prev = node

    def _remove(self, node: _Node) -> None:
        prev_node = node.prev
        next_node = node.next
        if prev_node is not None:
            prev_node.next = next_node
        if next_node is not None:
            next_node.prev = prev_node
        node.prev = None
        node.next = None

    def _move_to_front(self, node: _Node) -> None:
        self._remove(node)
        self._insert_after_head(node)
