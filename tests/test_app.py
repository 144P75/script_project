import pytest

from web.app import create_app


@pytest.fixture
def client(service):
    app = create_app(service)
    app.testing = True
    return app.test_client()


def test_index_page(client):
    res = client.get("/")
    assert res.status_code == 200 and b"Virtual Pet Companion" in res.data


def test_full_crud_flow(client):
    assert client.get("/api/pet").status_code == 409
    assert client.post("/api/pets", json={"name": "Milo"}).status_code == 201
    assert client.post("/api/pets", json={"name": "Mimi"}).status_code == 201
    assert client.get("/api/pets").get_json()["active"] == "Mimi"
    assert client.post("/api/pets/Milo/select").get_json()["name"] == "Milo"
    assert client.put("/api/pets/Milo", json={"new_name": "Momo"}).get_json()["name"] == "Momo"
    assert client.delete("/api/pets/Mimi").get_json()["deleted"] == "Mimi"
    names = [p["name"] for p in client.get("/api/pets").get_json()["pets"]]
    assert names == ["Momo"]


def test_actions_and_history(client):
    client.post("/api/pets", json={"name": "Milo"})
    res = client.post("/api/pet/actions/feed")
    assert res.status_code == 200 and res.get_json()["pet"]["hunger"] == 20
    client.post("/api/pet/actions/fact")
    data = client.get("/api/history?kind=fact").get_json()
    assert data["count"] == 1 and "test fact" in data["results"][0]["content"]
    assert "fact" in data["filters"]["kinds"]


def test_talk_endpoint(client):
    client.post("/api/pets", json={"name": "Milo"})
    data = client.post("/api/pet/talk", json={"message": "hi"}).get_json()
    assert data["online"] is False and data["reply"] and data["pet"]["name"] == "Milo"
    assert client.get("/api/history?kind=talk").get_json()["count"] == 2


@pytest.mark.parametrize("method, url, body, status", [
    ("post", "/api/pets", {"name": ""}, 400),
    ("post", "/api/pets", None, 400),
    ("put", "/api/pets/Ghost", {"new_name": "X"}, 404),
    ("delete", "/api/pets/Ghost", None, 404),
    ("post", "/api/pets/Ghost/select", None, 404),
    ("post", "/api/pet/actions/dance", None, 400),
    ("get", "/api/history?sort_by=weight", None, 400),
    ("get", "/api/history?limit=abc", None, 400),
    ("get", "/api/nothing", None, 404),
    ("post", "/api/pet/talk", {"message": ""}, 400),
    ("post", "/api/pet/talk", None, 400),
])
def test_errors_return_json(client, method, url, body, status):
    client.post("/api/pets", json={"name": "Milo"})
    res = getattr(client, method)(url, json=body) if body is not None else getattr(client, method)(url)
    assert res.status_code == status
    assert "error" in res.get_json()


def test_duplicate_returns_409(client):
    client.post("/api/pets", json={"name": "Milo"})
    assert client.post("/api/pets", json={"name": "milo"}).status_code == 409
