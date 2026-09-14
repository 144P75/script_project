import time
import requests


class MoodTracker:
    """จัดการอารมณ์และคำนวณ Decay over time ของสัตว์เลี้ยง"""

    def __init__(self, hunger: int = 50, energy: int = 50, happiness: int = 50):
        self.hunger = min(max(hunger, 0), 100)
        self.energy = min(max(energy, 0), 100)
        self.happiness = min(max(happiness, 0), 100)

    def update_decay(self, time_passed_seconds: float):
        """คำนวณค่าสเตตัสที่ลดลงตามเวลาจริง"""
        decay_units = int(time_passed_seconds // 10)  
        if decay_units > 0:
            self.hunger = min(100, self.hunger + (decay_units * 5))
            self.energy = max(0, self.energy - (decay_units * 3))
            self.happiness = max(0, self.happiness - (decay_units * 2))

    def get_mood(self) -> str:
        if self.hunger > 80:
            return "หิวมากๆ 😿"
        elif self.energy < 20:
            return "ง่วงนอนสุดๆ 💤"
        elif self.happiness > 70:
            return "มีความสุขมาก! 😸"
        return "อารมณ์ดี 😺"


class Interaction:
    """จัดการ External API (Cat Facts API)"""

    @staticmethod
    def fetch_cat_fact() -> str:
        try:
            response = requests.get("https://catfact.ninja/fact", timeout=5)
            if response.status_code == 200:
                return f"🐱 เกร็ดความรู้แมว: {response.json().get('fact')}"
            return "ไม่สามารถดึงเกร็ดความรู้แมวได้ในขณะนี้"
        except Exception:
            return "ไม่สามารถเชื่อมต่อ API ได้ (ตรวจสอบอินเทอร์เน็ต)"


class Pet:
    """Class หลักของสัตว์เลี้ยง รวมระบบ MoodTracker และ Interaction"""

    def __init__(self, name: str, hunger: int = 50, energy: int = 50, happiness: int = 50, last_updated: float = None):
        self.name = name
        self.mood_tracker = MoodTracker(hunger, energy, happiness)
        self.last_updated = last_updated or time.time()

    def apply_time_decay(self):
        now = time.time()
        elapsed = now - self.last_updated
        self.mood_tracker.update_decay(elapsed)
        self.last_updated = now

    def feed(self) -> str:
        self.apply_time_decay()
        if self.mood_tracker.energy <= 0:
            return f"{self.name} เหนื่อยเกินกว่าจะกิน! ต้องให้นอนพักก่อน"
        self.mood_tracker.hunger = max(0, self.mood_tracker.hunger - 30)
        self.mood_tracker.energy = min(100, self.mood_tracker.energy + 10)
        return f"คุณให้อาหาร {self.name} แล้ว! ความหิวยานลง"

    def play(self) -> str:
        self.apply_time_decay()
        if self.mood_tracker.hunger >= 90:
            return f"{self.name} หิวเกินกว่าจะเล่น!"
        if self.mood_tracker.energy < 20:
            return f"{self.name} เหนื่อยเกินกว่าจะเล่น!"
        self.mood_tracker.happiness = min(100, self.mood_tracker.happiness + 25)
        self.mood_tracker.hunger = min(100, self.mood_tracker.hunger + 15)
        self.mood_tracker.energy = max(0, self.mood_tracker.energy - 20)
        return f"คุณเล่นกับ {self.name} สนุกมากๆ!"

    def sleep(self) -> str:
        self.apply_time_decay()
        self.mood_tracker.energy = 100
        self.mood_tracker.hunger = min(100, self.mood_tracker.hunger + 20)
        return f"{self.name} ได้นอนหลับเต็มอิ่มและฟื้นฟูพลังงานเต็มที่!"

    def interact_api(self) -> str:
        self.apply_time_decay()
        self.mood_tracker.happiness = min(100, self.mood_tracker.happiness + 10)
        fact = Interaction.fetch_cat_fact()
        return f"คุณใช้เวลาร่วมกับ {self.name}!\n> {fact}"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "hunger": self.mood_tracker.hunger,
            "energy": self.mood_tracker.energy,
            "happiness": self.mood_tracker.happiness,
            "last_updated": self.last_updated
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name", "Buddy"),
            hunger=data.get("hunger", 50),
            energy=data.get("energy", 50),
            happiness=data.get("happiness", 50),
            last_updated=data.get("last_updated", time.time())
        )