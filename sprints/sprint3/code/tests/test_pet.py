from src.pet import DECAY_INTERVAL, MoodTracker, Pet


def test_mood_rules():
    assert MoodTracker(50, 50, 50).get_mood_key() == "ok"
    assert MoodTracker(hunger=85).get_mood_key() == "hungry"
    assert MoodTracker(energy=10).get_mood_key() == "sleepy"
    assert MoodTracker(happiness=90).get_mood_key() == "happy"
    assert MoodTracker(50, 50, 50).get_mood() == "อารมณ์ดี 😺"


def test_stats_are_clamped():
    tracker = MoodTracker(hunger=150, energy=-20, happiness=50)
    assert (tracker.hunger, tracker.energy) == (100, 0)
    tracker.change(hunger=50, happiness=-500)
    assert (tracker.hunger, tracker.happiness) == (100, 0)


def test_decay_over_time():
    pet = Pet("Milo", hunger=50, energy=50, happiness=50, last_updated=0)
    pet.apply_time_decay(now=20)  # 2 หน่วย
    assert pet.mood_tracker.hunger == 60
    assert pet.mood_tracker.energy == 44
    assert pet.mood_tracker.happiness == 46


def test_decay_keeps_leftover_seconds():
    """กดคำสั่งถี่ๆ ทุก 6 วินาที ต้องยังเกิด decay (บั๊กเดิมของ Sprint 2)"""
    pet = Pet("Milo", hunger=50, last_updated=0)
    for now in (6, 12, 18):
        pet.apply_time_decay(now=now)
    assert pet.mood_tracker.hunger == 50 + 5
    assert pet.last_updated == DECAY_INTERVAL


def test_decay_ignores_clock_going_backwards():
    pet = Pet("Milo", hunger=50, last_updated=100)
    pet.apply_time_decay(now=50)
    assert pet.mood_tracker.hunger == 50


def test_feed_play_sleep_effects():
    pet = Pet("Milo", hunger=50, energy=50, happiness=50)
    assert "ให้อาหาร" in pet.feed()
    assert pet.mood_tracker.hunger == 20
    pet.play()
    assert pet.mood_tracker.happiness == 75
    pet.sleep()
    assert pet.mood_tracker.energy == 100


def test_actions_refused_in_bad_state():
    assert "เหนื่อยเกินกว่าจะกิน" in Pet("A", hunger=50, energy=0).feed()
    assert "ยังอิ่มอยู่" in Pet("B", hunger=5).feed()
    assert "หิวเกินกว่าจะเล่น" in Pet("C", hunger=95).play()
    assert "เหนื่อยเกินกว่าจะเล่น" in Pet("D", energy=10).play()


def test_fact_uses_api_and_raises_happiness():
    pet = Pet("Milo", happiness=50)
    assert "test fact" in pet.interact_api()
    assert pet.mood_tracker.happiness == 60


def test_dict_round_trip():
    pet = Pet("Milo", hunger=10, energy=20, happiness=30)
    copy = Pet.from_dict(pet.to_dict())
    assert copy.to_dict() == pet.to_dict()
