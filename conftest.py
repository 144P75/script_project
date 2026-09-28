"""Fixtures กลางของชุดทดสอบ — ทุกเทสต์ใช้ไฟล์ชั่วคราวและไม่เรียกอินเทอร์เน็ตจริง"""
import pytest

from src.pet import Interaction
from src.history import InteractionHistory
from src.pet_manager import PetManager
from src.service import PetService

FAKE_FACT = "🐱 เกร็ดความรู้แมว: test fact"


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    monkeypatch.setattr(Interaction, "fetch_cat_fact", staticmethod(lambda: FAKE_FACT))


@pytest.fixture
def paths(tmp_path):
    return {
        "data": str(tmp_path / "pets.json"),
        "backup": str(tmp_path / "pets_backup.json"),
        "history": str(tmp_path / "history.json"),
        "history_backup": str(tmp_path / "history_backup.json"),
    }


@pytest.fixture
def make_manager(paths):
    return lambda: PetManager(paths["data"], paths["backup"])


@pytest.fixture
def make_service(paths, make_manager):
    def factory():
        return PetService(
            manager=make_manager(),
            history=InteractionHistory(paths["history"], paths["history_backup"]),
        )
    return factory


@pytest.fixture
def service(make_service):
    return make_service()
