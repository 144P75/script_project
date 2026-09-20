import json
from src.pet import Pet

class PetManager:
    def __init__(self, data_file="pets.json", backup_file="pets_backup.json"):
        self.data_file = data_file
        self.backup_file = backup_file
        self.pets = self.load_pets()
        self.active_pet = next(iter(self.pets.values())) if self.pets else None

    def add_pet(self, name):
        if name not in self.pets:
            new_pet = Pet(name)
            self.pets[name] = new_pet
            self.active_pet = new_pet
            self.save_pets()
            return f"สัตว์เลี้ยงใหม่ชื่อ {name} ถูกเพิ่มเรียบร้อย!"
        return f"สัตว์เลี้ยงชื่อ {name} มีอยู่แล้ว"

    def switch_pet(self, name):
        if name in self.pets:
            self.active_pet = self.pets[name]
            return f"สลับไปยังสัตว์เลี้ยงชื่อ {name} เรียบร้อย!"
        return f"ไม่พบสัตว์เลี้ยงชื่อ {name}"

    def save_pets(self):
        data = {name: pet.to_dict() for name, pet in self.pets.items()}
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        with open(self.backup_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_pets(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {name: Pet.from_dict(pet_data) for name, pet_data in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                with open(self.backup_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {name: Pet.from_dict(pet_data) for name, pet_data in data.items()}
            except (FileNotFoundError, json.JSONDecodeError):
                return {"Buddy": Pet("Buddy")}
