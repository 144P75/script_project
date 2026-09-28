import pytest

from src.exceptions import InvalidActionError, NoActivePetError


def test_no_pet_yet(service):
    assert not service.has_pet()
    with pytest.raises(NoActivePetError):
        service.perform("feed")


def test_action_updates_file_and_history(service, make_service):
    service.create_pet("Milo")
    result = service.perform("FEED ")
    assert "ให้อาหาร" in result["message"]
    # อีก instance (เช่น เว็บ) ต้องเห็นค่าเดียวกัน
    assert make_service().status()["hunger"] == result["pet"]["hunger"]
    kinds = [h["kind"] for h in service.query_history(order="asc")]
    assert kinds == ["create", "feed"]


def test_invalid_action(service):
    service.create_pet("Milo")
    with pytest.raises(InvalidActionError):
        service.perform("dance")


def test_cli_and_web_stay_in_sync(make_service):
    cli, web = make_service(), make_service()
    cli.create_pet("Milo")
    web.perform("play")
    web.create_pet("Mimi")
    assert {p["name"] for p in cli.list_pets()} == {"Milo", "Mimi"}
    assert cli.status()["name"] == "Mimi"


def test_crud_is_logged(service):
    service.create_pet("Milo")
    service.rename_pet("milo", "Momo")
    service.delete_pet("Momo")
    assert [h["kind"] for h in service.query_history(source="System", order="asc")] == ["create", "rename", "delete"]
    assert service.history_filters()["kinds"] == ["create", "delete", "rename"]


def test_concurrent_requests_do_not_lose_writes(service):
    import threading
    names = [f"Pet{i}" for i in range(10)]
    for name in names:
        service.create_pet(name)
    threads = [threading.Thread(target=service.delete_pet, args=(n,)) for n in names]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not service.has_pet()
