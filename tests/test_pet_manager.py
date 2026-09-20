# [Sprint 2] Unit tests สำหรับ PetManager
import os
from src.pet_manager import PetManager

def test_add_and_switch_pet(tmp_path, monkeypatch):
    monkeypatch.setattr("src.pet_manager.DATA_FILE", str(tmp_path / "pets.json"))
    manager = PetManager()
    msg = manager.add_pet("Milo")
    assert "Milo" in msg
    assert "Milo" in manager.pets

    msg2 = manager.switch_pet("Milo")
    assert "Milo" in msg2
    assert manager.active_pet.name == "Milo"

def test_save_and_load_pets(tmp_path, monkeypatch):
    monkeypatch.setattr("src.pet_manager.DATA_FILE", str(tmp_path / "pets.json"))
    manager = PetManager()
    manager.add_pet("Buddy")
    manager.save_pets()

    new_manager = PetManager()
    assert "Buddy" in new_manager.pets
