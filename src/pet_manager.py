# [Sprint 2] เพิ่มระบบ Multi-Pet Management
import json
import os
from src.pet import Pet

DATA_FILE = "pets.json"

class PetManager:
    def __init__(self):
        self.pets = {}
        self.active_pet = None
        self.load_pets()

    def load_pets(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for name, pet_data in data.items():
                    self.pets[name] = Pet.from_dict(pet_data)
        if self.pets:
            self.active_pet = list(self.pets.values())[0]

    def save_pets(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({name: pet.to_dict() for name, pet in self.pets.items()}, f, indent=4, ensure_ascii=False)
        # [Sprint 2] Auto-backup
        with open("pets_backup.json", "w", encoding="utf-8") as f:
            json.dump({name: pet.to_dict() for name, pet in self.pets.items()}, f, indent=4, ensure_ascii=False)

    def add_pet(self, name: str):
        if name not in self.pets:
            self.pets[name] = Pet(name=name)
            self.active_pet = self.pets[name]
            self.save_pets()
            return f"เพิ่มสัตว์เลี้ยงใหม่ชื่อ {name} เรียบร้อย!"
        return f"มีสัตว์เลี้ยงชื่อ {name} อยู่แล้ว"

    def switch_pet(self, name: str):
        if name in self.pets:
            self.active_pet = self.pets[name]
            return f"สลับไปยังสัตว์เลี้ยงชื่อ {name}"
        return f"ไม่พบสัตว์เลี้ยงชื่อ {name}"
