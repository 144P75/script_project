"""Business Logic Layer: จัดการสัตว์เลี้ยงหลายตัว (CRUD) และบันทึกลงไฟล์"""
import re

from src.exceptions import (
    DuplicatePetError,
    InvalidInputError,
    InvalidPetNameError,
    PetNotFoundError,
)
from src.pet import Pet
from src.storage import JsonStore

SCHEMA_VERSION = 2
MAX_NAME_LENGTH = 20
NAME_PATTERN = re.compile(r"^[A-Za-z0-9\u0E00-\u0E7F _-]+$")
PET_SORT_KEYS = {
    "name": lambda p: p.name.casefold(),
    "hunger": lambda p: p.mood_tracker.hunger,
    "energy": lambda p: p.mood_tracker.energy,
    "happiness": lambda p: p.mood_tracker.happiness,
    "created": lambda p: p.created_at,
}


class PetManager:
    """เก็บสัตว์เลี้ยงเป็น dict[name, Pet] และจำตัวที่กำลังใช้งาน

    ทุกเมธอดที่เปลี่ยนข้อมูล (add/switch/rename/delete) จะบันทึกลงไฟล์ทันที
    """

    def __init__(self, data_file="pets.json", backup_file="pets_backup.json"):
        self.store = JsonStore(data_file, backup_file, default_factory=dict)
        self.pets = {}
        self.active_name = None
        self.load_warning = None
        self.reload()

    # ---------- Persistence ----------
    def reload(self):
        """โหลดข้อมูลล่าสุดจากไฟล์ (ใช้ก่อนทุกคำสั่ง เพื่อให้ CLI และเว็บเห็นข้อมูลตรงกัน)"""
        data, warning = self.store.load()
        # รองรับไฟล์รูปแบบเดิมของ Sprint 2 ที่เก็บ {ชื่อ: ข้อมูล} ตรงๆ
        raw_pets = data.get("pets") if isinstance(data.get("pets"), dict) else data
        self.pets = {}
        skipped = 0
        for key, pet_data in raw_pets.items():
            try:
                pet = Pet.from_dict(pet_data)
                self.pets[pet.name] = pet
            except (KeyError, TypeError, ValueError, AttributeError):
                skipped += 1
        if skipped:
            warning = f"ข้ามข้อมูลสัตว์เลี้ยงที่เสียหาย {skipped} รายการ"
        active = data.get("active") if isinstance(data.get("pets"), dict) else None
        self.active_name = active if active in self.pets else next(iter(self.pets), None)
        if warning:
            self.load_warning = warning
            self.save()  # ซ่อมไฟล์หลักทันทีหลังกู้คืน

    def save(self):
        self.store.save({
            "version": SCHEMA_VERSION,
            "active": self.active_name,
            "pets": {name: pet.to_dict() for name, pet in self.pets.items()},
        })

    save_pets = save  # ชื่อเดิมจาก Sprint 2

    def pop_warning(self):
        warning, self.load_warning = self.load_warning, None
        return warning

    # ---------- Validation / lookup ----------
    @staticmethod
    def validate_name(name):
        """ตรวจสอบและคืนชื่อที่ตัดช่องว่างแล้ว"""
        if not isinstance(name, str) or not name.strip():
            raise InvalidPetNameError("ชื่อสัตว์เลี้ยงต้องไม่ว่าง")
        name = name.strip()
        if len(name) > MAX_NAME_LENGTH:
            raise InvalidPetNameError(f"ชื่อสัตว์เลี้ยงยาวได้ไม่เกิน {MAX_NAME_LENGTH} ตัวอักษร")
        if not NAME_PATTERN.match(name):
            raise InvalidPetNameError("ชื่อใช้ได้เฉพาะตัวอักษรไทย/อังกฤษ ตัวเลข ช่องว่าง - และ _")
        return name

    def _find_key(self, name):
        """หาชื่อจริงใน dict โดยไม่สนตัวพิมพ์เล็ก-ใหญ่"""
        target = str(name).strip().casefold()
        return next((key for key in self.pets if key.casefold() == target), None)

    def get_pet(self, name):
        key = self._find_key(name)
        if key is None:
            raise PetNotFoundError(name)
        return self.pets[key]

    @property
    def active_pet(self):
        return self.pets.get(self.active_name)

    # ---------- CRUD ----------
    def add_pet(self, name):
        name = self.validate_name(name)
        if self._find_key(name) is not None:
            raise DuplicatePetError(name)
        pet = Pet(name)
        self.pets[name] = pet
        self.active_name = name
        self.save()
        return pet

    def list_pets(self, sort_by="name", order="asc"):
        if sort_by not in PET_SORT_KEYS:
            raise InvalidInputError(f"เรียงได้ตาม: {', '.join(PET_SORT_KEYS)}")
        if order not in ("asc", "desc"):
            raise InvalidInputError("order ต้องเป็น asc หรือ desc")
        for pet in self.pets.values():
            pet.apply_time_decay()
        return sorted(self.pets.values(), key=PET_SORT_KEYS[sort_by], reverse=(order == "desc"))

    def switch_pet(self, name):
        pet = self.get_pet(name)
        self.active_name = pet.name
        self.save()
        return pet

    def rename_pet(self, old_name, new_name):
        pet = self.get_pet(old_name)
        new_name = self.validate_name(new_name)
        other = self._find_key(new_name)
        if other is not None and other != pet.name:
            raise DuplicatePetError(new_name)
        old_key = pet.name
        pet.name = new_name
        # สร้าง dict ใหม่เพื่อคงลำดับเดิม
        self.pets = {(new_name if k == old_key else k): v for k, v in self.pets.items()}
        if self.active_name == old_key:
            self.active_name = new_name
        self.save()
        return pet

    def delete_pet(self, name):
        pet = self.get_pet(name)
        del self.pets[pet.name]
        if self.active_name == pet.name:
            self.active_name = next(iter(self.pets), None)
        self.save()
        return pet
