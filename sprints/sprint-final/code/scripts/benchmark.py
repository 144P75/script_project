"""วัดความเร็วการค้นหา/กรอง/เรียงลำดับ สำหรับเดโม

python -m scripts.benchmark            วัดผลกับข้อมูล 1,000 รายการ
python -m scripts.benchmark --n 5000   กำหนดจำนวนข้อมูลเอง
python -m scripts.benchmark --write    เขียนข้อมูลชุดทดสอบลง interaction_history.json ด้วย
"""
import argparse
import random
import time
from datetime import datetime, timedelta

from src.history import filter_history, search_history, sort_history
from src.storage import JsonStore

PETS = ["Milo", "Mimi", "Coco", "Buddy"]
KINDS = {"User": ["feed", "play", "sleep"], "Cat Facts API": ["fact"], "System": ["create"]}
TEXT = {
    "feed": "ให้อาหาร", "play": "เล่นด้วย", "sleep": "นอนหลับ",
    "fact": "Cats sleep a lot", "create": "เพิ่มสัตว์เลี้ยง",
}


def make_entries(n, seed=42):
    rng = random.Random(seed)
    start = datetime(2026, 9, 1)
    entries = []
    for _ in range(n):
        source = rng.choice(list(KINDS))
        kind = rng.choice(KINDS[source])
        pet = rng.choice(PETS)
        ts = start + timedelta(minutes=rng.randint(0, 60 * 24 * 28))
        entries.append({
            "timestamp": ts.isoformat(timespec="seconds"),
            "source": source,
            "kind": kind,
            "pet": pet,
            "content": f"{TEXT[kind]} {pet}",
        })
    return entries


def timed(label, func):
    start = time.perf_counter()
    result = func()
    ms = (time.perf_counter() - start) * 1000
    print(f"{label:<40} {len(result):>6} รายการ  {ms:7.2f} ms")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    data = make_entries(args.n)
    print(f"ชุดข้อมูลทดสอบ {args.n:,} รายการ\n")
    timed("ค้นหา 'sleep'", lambda: search_history(data, "sleep"))
    timed("กรอง source=User, pet=Milo", lambda: filter_history(data, source="User", pet="Milo"))
    timed("เรียง timestamp (ใหม่→เก่า)", lambda: sort_history(data, "timestamp", "desc"))
    timed("เรียงหลายคีย์ pet,kind,timestamp", lambda: sort_history(data, "pet,kind,timestamp", "asc"))
    timed("ค้นหา + กรอง + เรียง", lambda: sort_history(
        filter_history(search_history(data, "milo"), source="User"), "kind,timestamp", "asc"))

    if args.write:
        JsonStore("interaction_history.json", "interaction_history_backup.json", list).save(data)
        print("\nเขียนข้อมูลลง interaction_history.json แล้ว")


if __name__ == "__main__":
    main()
