import tempfile
import os
from src.pet_manager import PetManager

def test_feed_auto_save():
    tmp_data = tempfile.NamedTemporaryFile(delete=False)
    tmp_backup = tempfile.NamedTemporaryFile(delete=False)

    manager = PetManager(data_file=tmp_data.name, backup_file=tmp_backup.name)
    manager.add_pet("Buddy")
    manager.feed("Buddy")

    with open(tmp_data.name, "r", encoding="utf-8") as f:
        data = f.read()
    assert "Buddy" in data

def test_backup_recovery():
    tmp_data = tempfile.NamedTemporaryFile(delete=False)
    tmp_backup = tempfile.NamedTemporaryFile(delete=False)

    manager = PetManager(data_file=tmp_data.name, backup_file=tmp_backup.name)
    manager.pets = {"Buddy": {"hunger": 5, "mood": 5, "energy": 5}}
    manager.save()
    
    with open(tmp_data.name, "w") as f:
        f.write("INVALID JSON")

    recovered = manager.load()
    assert "Buddy" in recovered
