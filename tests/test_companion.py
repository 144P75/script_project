from unittest.mock import MagicMock

import pytest
import requests

from src import companion
from src.companion import PetCompanion, build_system_prompt
from src.pet import Pet


def fake_response(json_data):
    res = MagicMock()
    res.json.return_value = json_data
    return res


def test_prompt_contains_pet_state():
    prompt = build_system_prompt(Pet("Milo", hunger=85, energy=40, happiness=30))
    assert "Milo" in prompt and "85" in prompt and "hungry" in prompt


def test_no_key_uses_offline_reply_by_mood(monkeypatch):
    post = MagicMock()
    monkeypatch.setattr(companion.requests, "post", post)
    text, online = PetCompanion(api_key="").reply(Pet("Milo", hunger=90), "สวัสดี")
    assert not online and "Milo" in text and "หิว" in text
    post.assert_not_called()


def test_api_success(monkeypatch):
    post = MagicMock(return_value=fake_response({"content": [{"type": "text", "text": "เมี้ยว!"}]}))
    monkeypatch.setattr(companion.requests, "post", post)
    text, online = PetCompanion(api_key="k").reply(Pet("Milo"), "hi")
    assert (text, online) == ("เมี้ยว!", True)
    body = post.call_args.kwargs["json"]
    assert "Milo" in body["system"] and body["messages"][0]["content"] == "hi"


@pytest.mark.parametrize("behavior", [
    requests.Timeout(),
    requests.ConnectionError(),
    fake_response({"error": "bad"}),       # ไม่มี content
    fake_response({"content": []}),        # ตอบว่าง
])
def test_api_failure_falls_back(monkeypatch, behavior):
    kwargs = {"side_effect": behavior} if isinstance(behavior, Exception) else {"return_value": behavior}
    monkeypatch.setattr(companion.requests, "post", MagicMock(**kwargs))
    text, online = PetCompanion(api_key="k").reply(Pet("Milo"), "hi")
    assert not online and "Milo" in text
