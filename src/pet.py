"""Business Logic Layer: Domain model ของสัตว์เลี้ยง"""
import random
import time

import requests

STAT_MIN, STAT_MAX = 0, 100
DECAY_INTERVAL = 10  # วินาทีต่อ 1 หน่วย decay
DECAY_PER_UNIT = {"hunger": 5, "energy": -3, "happiness": -2}

OFFLINE_FACTS = [
    "Cats sleep for around 12 to 16 hours a day.",
    "A group of cats is called a clowder.",
    "Cats have five toes on their front paws but only four on the back paws.",
]


def clamp(value):
    """บังคับค่าสถานะให้อยู่ระหว่าง 0-100"""
    return max(STAT_MIN, min(STAT_MAX, int(value)))


class MoodTracker:
    """เก็บค่าสถานะ คำนวณ decay และประเมินอารมณ์"""

    MOODS = {
        "hungry": "หิวมากๆ 😿",
        "sleepy": "ง่วงนอนสุดๆ 💤",
        "happy": "มีความสุขมาก! 😸",
        "ok": "อารมณ์ดี 😺",
    }

    def __init__(self, hunger=50, energy=50, happiness=50):
        self.hunger = clamp(hunger)
        self.energy = clamp(energy)
        self.happiness = clamp(happiness)

    def change(self, hunger=0, energy=0, happiness=0):
        """ปรับค่าสถานะแบบสัมพัทธ์ โดยไม่ให้หลุดช่วง 0-100"""
        self.hunger = clamp(self.hunger + hunger)
        self.energy = clamp(self.energy + energy)
        self.happiness = clamp(self.happiness + happiness)

    def decay(self, units):
        """ลดสถานะตามจำนวนหน่วยเวลาที่ผ่านไป"""
        if units > 0:
            self.change(**{k: v * units for k, v in DECAY_PER_UNIT.items()})

    def update_decay(self, time_passed_seconds):
        """คำนวณ decay จากจำนวนวินาที คืนจำนวนหน่วยที่ใช้ไป"""
        units = int(max(0, time_passed_seconds) // DECAY_INTERVAL)
        self.decay(units)
        return units

    def get_mood_key(self):
        if self.hunger > 80:
            return "hungry"
        if self.energy < 20:
            return "sleepy"
        if self.happiness > 70:
            return "happy"
        return "ok"

    def get_mood(self):
        return self.MOODS[self.get_mood_key()]


class Interaction:
    """เชื่อมต่อ External API (Cat Facts API)"""

    URL = "https://catfact.ninja/fact"

    @staticmethod
    def fetch_cat_fact():
        """คืนเกร็ดความรู้แมว ถ้า API ใช้ไม่ได้จะใช้ข้อมูลสำรองในเครื่อง"""
        try:
            response = requests.get(Interaction.URL, timeout=5)
            response.raise_for_status()
            fact = response.json().get("fact")
            if fact:
                return f"🐱 เกร็ดความรู้แมว: {fact}"
        except (requests.RequestException, ValueError):
            pass
        return f"🐱 เกร็ดความรู้แมว (ออฟไลน์): {random.choice(OFFLINE_FACTS)}"


class Pet:
    """สัตว์เลี้ยง 1 ตัว รวม MoodTracker และ Interaction"""

    def __init__(self, name, hunger=50, energy=50, happiness=50, last_updated=None, created_at=None):
        now = time.time()
        self.name = name
        self.mood_tracker = MoodTracker(hunger, energy, happiness)
        self.last_updated = float(last_updated) if last_updated is not None else now
        self.created_at = float(created_at) if created_at is not None else now

    def apply_time_decay(self, now=None):
        """ลดสถานะตามเวลาจริง เศษวินาทีที่ยังไม่ครบหน่วยจะถูกเก็บไว้คิดรอบถัดไป"""
        now = time.time() if now is None else now
        elapsed = now - self.last_updated
        if elapsed < 0:  # นาฬิกาเครื่องถูกย้อน
            self.last_updated = now
            return
        units = self.mood_tracker.update_decay(elapsed)
        self.last_updated += units * DECAY_INTERVAL

    def feed(self):
        self.apply_time_decay()
        if self.mood_tracker.energy <= 0:
            return f"{self.name} เหนื่อยเกินกว่าจะกิน! ต้องให้นอนพักก่อน"
        if self.mood_tracker.hunger <= 10:
            return f"{self.name} ยังอิ่มอยู่เลย ไม่อยากกินตอนนี้"
        self.mood_tracker.change(hunger=-30, energy=10)
        return f"คุณให้อาหาร {self.name} แล้ว! ความหิวลดลง"

    def play(self):
        self.apply_time_decay()
        if self.mood_tracker.hunger >= 90:
            return f"{self.name} หิวเกินกว่าจะเล่น!"
        if self.mood_tracker.energy < 20:
            return f"{self.name} เหนื่อยเกินกว่าจะเล่น!"
        self.mood_tracker.change(hunger=15, energy=-20, happiness=25)
        return f"คุณเล่นกับ {self.name} สนุกมากๆ!"

    def sleep(self):
        self.apply_time_decay()
        self.mood_tracker.energy = STAT_MAX
        self.mood_tracker.change(hunger=20)
        return f"{self.name} ได้นอนหลับเต็มอิ่มและฟื้นฟูพลังงานเต็มที่!"

    def interact_api(self):
        self.apply_time_decay()
        self.mood_tracker.change(happiness=10)
        return f"คุณใช้เวลาร่วมกับ {self.name}!\n> {Interaction.fetch_cat_fact()}"

    def to_dict(self):
        return {
            "name": self.name,
            "hunger": self.mood_tracker.hunger,
            "energy": self.mood_tracker.energy,
            "happiness": self.mood_tracker.happiness,
            "last_updated": self.last_updated,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        """สร้าง Pet จาก dict — raise ValueError/TypeError ถ้าข้อมูลผิดรูปแบบ"""
        return cls(
            name=str(data["name"]),
            hunger=int(data.get("hunger", 50)),
            energy=int(data.get("energy", 50)),
            happiness=int(data.get("happiness", 50)),
            last_updated=data.get("last_updated"),
            created_at=data.get("created_at"),
        )
