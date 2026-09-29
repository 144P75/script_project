import json

import pytest

from src.exceptions import (
    DuplicatePetError,
    InvalidInputError,
    InvalidPetNameError,
    PetNotFoundError,
)


def test_create_and_persist(make_manager, paths):
    make_manager().add_pet("  Milo  ")
    reloaded = make_manager()
    assert list(reloaded.pets) == ["Milo"]
    assert reloaded.active_pet.name == "Milo"
    assert json.load(open(paths["data"], encoding="utf-8"))["version"] == 2


@pytest.mark.parametrize("name", ["", "   ", "a" * 21, "Milo!", "<script>", None])
def test_invalid_names_rejected(make_manager, name):
    with pytest.raises(InvalidPetNameError):
        make_manager().add_pet(name)


def test_thai_name_allowed(make_manager):
    assert make_manager().add_pet("มิโล่ 2").name == "มิโล่ 2"


def test_duplicate_name_case_insensitive(make_manager):
    manager = make_manager()
    manager.add_pet("Milo")
    with pytest.raises(DuplicatePetError):
        manager.add_pet("milo")


def test_switch_rename_delete(make_manager):
    manager = make_manager()
    manager.add_pet("Milo")
    manager.add_pet("Mimi")
    manager.switch_pet("milo")
    assert manager.active_name == "Milo"
    manager.rename_pet("Milo", "Momo")
    assert manager.active_name == "Momo" and "Milo" not in manager.pets
    manager.delete_pet("Momo")
    assert manager.active_name == "Mimi"
    assert list(make_manager().pets) == ["Mimi"]


def test_rename_to_existing_name_fails(make_manager):
    manager = make_manager()
    manager.add_pet("Milo")
    manager.add_pet("Mimi")
    with pytest.raises(DuplicatePetError):
        manager.rename_pet("Milo", "MIMI")
    manager.rename_pet("Milo", "MILO")  # เปลี่ยนตัวพิมพ์ของตัวเองได้


def test_missing_pet_raises_custom_exception(make_manager):
    manager = make_manager()
    for call in (manager.switch_pet, manager.delete_pet, lambda n: manager.rename_pet(n, "X")):
        with pytest.raises(PetNotFoundError):
            call("Ghost")


def test_delete_last_pet_leaves_no_active(make_manager):
    manager = make_manager()
    manager.add_pet("Milo")
    manager.delete_pet("Milo")
    assert manager.active_pet is None
    assert make_manager().active_pet is None


def test_list_pets_sorting(make_manager):
    manager = make_manager()
    for name, hunger in (("b", 10), ("A", 90), ("c", 50)):
        manager.add_pet(name).mood_tracker.hunger = hunger
    assert [p.name for p in manager.list_pets("name")] == ["A", "b", "c"]
    assert [p.name for p in manager.list_pets("hunger", "desc")] == ["A", "c", "b"]
    with pytest.raises(InvalidInputError):
        manager.list_pets("weight")


def test_missing_file_starts_empty(make_manager):
    manager = make_manager()
    assert manager.pets == {} and manager.pop_warning() is None


def test_corrupt_file_recovers_from_backup(make_manager, paths):
    make_manager().add_pet("Buddy")
    with open(paths["data"], "w", encoding="utf-8") as f:
        f.write("{ INVALID JSON")
    recovered = make_manager()
    assert "Buddy" in recovered.pets
    assert "เสียหาย" in recovered.pop_warning()


def test_corrupt_file_without_backup(make_manager, paths):
    with open(paths["data"], "w", encoding="utf-8") as f:
        f.write("not json")
    manager = make_manager()
    assert manager.pets == {}
    assert manager.pop_warning()


def test_backup_holds_previous_version(make_manager, paths):
    manager = make_manager()
    manager.add_pet("Milo")
    manager.add_pet("Mimi")
    backup = json.load(open(paths["backup"], encoding="utf-8"))
    assert list(backup["pets"]) == ["Milo"]


def test_bad_pet_entries_are_skipped(make_manager, paths):
    data = {"version": 2, "active": "Milo", "pets": {
        "Milo": {"name": "Milo", "hunger": 10},
        "Bad": {"name": "Bad", "hunger": "abc"},
        "Worse": "not a dict",
    }}
    with open(paths["data"], "w", encoding="utf-8") as f:
        json.dump(data, f)
    manager = make_manager()
    assert list(manager.pets) == ["Milo"]
    assert "2" in manager.pop_warning()


def test_reads_sprint2_legacy_format(make_manager, paths):
    with open(paths["data"], "w", encoding="utf-8") as f:
        json.dump({"Milo": {"name": "Milo", "hunger": 70, "energy": 40, "happiness": 60}}, f)
    manager = make_manager()
    assert manager.active_pet.mood_tracker.hunger == 70


def test_recovery_repairs_main_file(make_manager, paths):
    make_manager().add_pet("Buddy")
    with open(paths["data"], "w", encoding="utf-8") as f:
        f.write("garbage")
    make_manager()
    assert "Buddy" in json.load(open(paths["data"], encoding="utf-8"))["pets"]
