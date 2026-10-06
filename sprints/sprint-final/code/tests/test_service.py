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


def test_crud_updates_history(service):
    service.create_pet("Milo")
    service.create_pet("Mimi")
    service.perform("feed")
    service.rename_pet("mimi", "Momo")
    assert service.query_history(pet="Mimi") == []
    assert {h["kind"] for h in service.query_history(pet="Momo")} == {"create", "feed", "rename"}
    service.delete_pet("Momo")
    assert service.query_history(pet="Momo") == []
    assert service.history_filters()["pets"] == ["Milo"]


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


def test_talk_raises_happiness_and_logs_both_sides(service):
    from src.exceptions import InvalidInputError
    service.create_pet("Milo")
    before = service.status()["happiness"]
    result = service.talk("  สวัสดี  ")
    assert result["online"] is False and result["pet"]["happiness"] == before + 5
    talks = service.query_history(kind="talk", order="asc")
    assert [(h["source"], h["content"]) for h in talks] == [
        ("User", "สวัสดี"), ("Companion (offline)", result["reply"])]
    for bad in ("", "   ", "x" * 201):
        with pytest.raises(InvalidInputError):
            service.talk(bad)


def test_talk_without_pet(service):
    with pytest.raises(NoActivePetError):
        service.talk("hi")
