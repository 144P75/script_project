from src.pet import Pet, MoodTracker


def test_mood_tracker_initialization():
    tracker = MoodTracker(hunger=50, energy=50, happiness=50)
    assert tracker.get_mood() == "อารมณ์ดี 😺"


def test_pet_time_decay():
    pet = Pet("Milo", hunger=50, energy=50, happiness=50)
    # จำลองเวลาผ่านไป 20 วินาที
    pet.mood_tracker.update_decay(20)
    assert pet.mood_tracker.hunger > 50
    assert pet.mood_tracker.energy < 50


def test_pet_feed():
    pet = Pet("Milo", hunger=50, energy=50)
    msg = pet.feed()
    assert "คุณให้อาหาร" in msg