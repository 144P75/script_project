"""Service Layer: จุดเดียวที่ Presentation Layer (CLI และ Web) เรียกใช้ Business Logic

ทุกเมธอดจะ reload ข้อมูลจากไฟล์ก่อน และบันทึกทันทีหลังเปลี่ยนแปลง
ทำให้ข้อมูลในหน่วยความจำ ไฟล์ JSON และหน้าจอ ตรงกันเสมอ (State Consistency)
"""
import functools
import threading

from src.exceptions import InvalidActionError, NoActivePetError
from src.history import InteractionHistory
from src.pet_manager import PetManager

# action -> (source ที่บันทึกลงประวัติ, ชื่อเมธอดของ Pet)
ACTIONS = {
    "feed": ("User", "feed"),
    "play": ("User", "play"),
    "sleep": ("User", "sleep"),
    "fact": ("Cat Facts API", "interact_api"),
}


def synchronized(method):
    """ให้คำสั่งทำทีละคำสั่ง: กันกรณีเว็บส่งหลาย request พร้อมกันแล้วเขียนไฟล์ทับกัน"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        with self.lock:
            return method(self, *args, **kwargs)
    return wrapper


def pet_view(pet, active_name=None):
    """แปลง Pet เป็น dict สำหรับแสดงผล"""
    data = pet.to_dict()
    data["mood"] = pet.mood_tracker.get_mood()
    data["mood_key"] = pet.mood_tracker.get_mood_key()
    data["active"] = pet.name == active_name
    return data


class PetService:
    def __init__(self, manager=None, history=None):
        self.manager = manager or PetManager()
        self.history = history or InteractionHistory()
        self.lock = threading.RLock()

    def _active(self):
        self.manager.reload()
        pet = self.manager.active_pet
        if pet is None:
            raise NoActivePetError()
        return pet

    def _view(self, pet):
        return pet_view(pet, self.manager.active_name)

    @synchronized
    def pop_warning(self):
        return self.manager.pop_warning()

    @synchronized
    def has_pet(self):
        self.manager.reload()
        return self.manager.active_pet is not None

    # ---------- สถานะและการโต้ตอบ ----------
    @synchronized
    def status(self):
        pet = self._active()
        pet.apply_time_decay()
        return self._view(pet)

    @synchronized
    def perform(self, action):
        action = str(action).strip().lower()
        if action not in ACTIONS:
            raise InvalidActionError(action)
        pet = self._active()
        source, method = ACTIONS[action]
        message = getattr(pet, method)()
        self.manager.save()
        self.history.add(source, action, message, pet=pet.name)
        return {"message": message, "pet": self._view(pet)}

    # ---------- CRUD ----------
    @synchronized
    def create_pet(self, name):
        self.manager.reload()
        pet = self.manager.add_pet(name)
        self.history.add("System", "create", f"เพิ่มสัตว์เลี้ยง {pet.name}", pet=pet.name)
        return self._view(pet)

    @synchronized
    def list_pets(self, sort_by="name", order="asc"):
        self.manager.reload()
        return [self._view(p) for p in self.manager.list_pets(sort_by, order)]

    @synchronized
    def select_pet(self, name):
        self.manager.reload()
        return self._view(self.manager.switch_pet(name))

    @synchronized
    def rename_pet(self, old_name, new_name):
        self.manager.reload()
        old = self.manager.get_pet(old_name).name
        pet = self.manager.rename_pet(old_name, new_name)
        self.history.rename_pet(old, pet.name)
        self.history.add("System", "rename", f"เปลี่ยนชื่อ {old} เป็น {pet.name}", pet=pet.name)
        return self._view(pet)

    @synchronized
    def delete_pet(self, name):
        self.manager.reload()
        pet = self.manager.delete_pet(name)
        self.history.remove_pet(pet.name)  # ลบสัตว์เลี้ยงแล้ว ประวัติของตัวนั้นหายไปด้วย
        return {"deleted": pet.name, "active": self.manager.active_name}

    # ---------- ประวัติ ----------
    @synchronized
    def query_history(self, keyword="", source=None, kind=None, pet=None,
                      sort_by="timestamp", order="desc", limit=None):
        results = self.history.query(keyword, source, kind, pet, sort_by, order)
        return results[:limit] if limit else results

    @synchronized
    def history_filters(self):
        return {field + "s": self.history.distinct(field) for field in ("source", "kind", "pet")}