import tempfile
from src.pet_manager import PetManager


def test_add_pet_auto_save():
    """add_pet() should create the pet and write it to data_file immediately."""
    tmp_data = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    tmp_backup = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

    manager = PetManager(data_file=tmp_data.name, backup_file=tmp_backup.name)
    manager.add_pet("Buddy")

    with open(tmp_data.name, "r", encoding="utf-8") as f:
        data = f.read()
    assert "Buddy" in data


def test_backup_recovery():
    """If the main data file is corrupted, PetManager should recover from the backup."""
    tmp_data = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    tmp_backup = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

    manager = PetManager(data_file=tmp_data.name, backup_file=tmp_backup.name)
    manager.add_pet("Buddy")  

    
    with open(tmp_data.name, "w", encoding="utf-8") as f:
        f.write("INVALID JSON")

    recovered = PetManager(data_file=tmp_data.name, backup_file=tmp_backup.name)
    assert "Buddy" in recovered.pets
