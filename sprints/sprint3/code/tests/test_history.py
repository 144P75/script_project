import random
import time

import pytest

from src.exceptions import InvalidInputError
from src.history import InteractionHistory, filter_history, search_history, sort_history

ENTRIES = [
    {"timestamp": "2026-09-20T10:00:00", "source": "User", "kind": "feed", "pet": "Milo", "content": "ให้อาหาร Milo"},
    {"timestamp": "2026-09-21T09:00:00", "source": "Cat Facts API", "kind": "fact", "pet": "Mimi",
     "content": "Cats sleep 16 hours"},
    {"timestamp": "2026-09-19T08:00:00", "source": "User", "kind": "sleep", "pet": "Mimi", "content": "Mimi นอนหลับ"},
]


def test_search_is_case_insensitive_and_checks_many_fields():
    assert len(search_history(ENTRIES, "SLEEP")) == 2  # content + kind
    assert len(search_history(ENTRIES, "mimi")) == 2  # pet
    assert search_history(ENTRIES, "zzz") == []


def test_empty_search_returns_everything():
    assert len(search_history(ENTRIES, "   ")) == 3
    assert len(search_history(ENTRIES, None)) == 3


def test_filter_by_several_attributes():
    assert len(filter_history(ENTRIES, source="user")) == 2
    assert len(filter_history(ENTRIES, source="User", pet="Mimi")) == 1
    assert len(filter_history(ENTRIES, since="2026-09-20")) == 2
    assert len(filter_history(ENTRIES, until="2026-09-20")) == 2
    assert len(filter_history(ENTRIES)) == 3


def test_sort_by_multiple_keys():
    by_time = sort_history(ENTRIES, "timestamp", "asc")
    assert [e["kind"] for e in by_time] == ["sleep", "feed", "fact"]
    by_pet = sort_history(ENTRIES, "pet,timestamp", "asc")
    assert [(e["pet"], e["kind"]) for e in by_pet] == [("Milo", "feed"), ("Mimi", "sleep"), ("Mimi", "fact")]


@pytest.mark.parametrize("sort_by, order", [("weight", "asc"), ("timestamp", "up")])
def test_sort_rejects_invalid_options(sort_by, order):
    with pytest.raises(InvalidInputError):
        sort_history(ENTRIES, sort_by, order)


def test_add_and_query_from_file(paths):
    history = InteractionHistory(paths["history"], paths["history_backup"])
    history.add("User", "feed", "ให้อาหาร", pet="Milo")
    history.add("User", "play", "เล่น", pet="Mimi")
    assert len(history.load()) == 2
    assert history.query(pet="Mimi")[0]["kind"] == "play"
    assert history.distinct("pet") == ["Milo", "Mimi"]


def test_corrupt_history_file_does_not_crash(paths):
    with open(paths["history"], "w", encoding="utf-8") as f:
        f.write("[broken")
    history = InteractionHistory(paths["history"], paths["history_backup"])
    assert history.load() == []
    history.add("User", "feed", "ok")
    assert len(history.load()) == 1


def test_1000_entries_processed_quickly():
    rng = random.Random(1)
    data = [{
        "timestamp": f"2026-09-{rng.randint(1, 28):02d}T{rng.randint(0, 23):02d}:00:00",
        "source": rng.choice(["User", "Cat Facts API", "System"]),
        "kind": rng.choice(["feed", "play", "sleep", "fact"]),
        "pet": rng.choice(["Milo", "Mimi", "Coco"]),
        "content": rng.choice(["ให้อาหาร", "เล่นด้วย", "นอนหลับ", "Cats sleep a lot"]),
    } for _ in range(1000)]
    start = time.perf_counter()
    result = sort_history(filter_history(search_history(data, "sleep"), source="User"), "pet,timestamp", "asc")
    assert time.perf_counter() - start < 0.5
    assert all(e["source"] == "User" for e in result)
