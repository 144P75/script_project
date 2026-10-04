from unittest.mock import MagicMock

import pytest
import requests

from src import companion
from src.companion import PetCompanion, build_system_prompt
from src.pet import Pet

GEMINI_OK = {"candidates": [{"content": {"parts": [{"text": "เมี้ยว!"}]}}]}
OPENAI_OK = {"choices": [{"message": {"content": "เมี้ยว!"}}]}
CLAUDE_OK = {"content": [{"type": "text", "text": "เมี้ยว!"}]}


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(companion.time, "sleep", lambda s: None)


def fake_response(json_data, status=200):
    res = MagicMock(status_code=status)
    res.json.return_value = json_data
    if status >= 400:
        res.raise_for_status.side_effect = requests.HTTPError(str(status))
    return res


def test_prompt_contains_pet_state():
    prompt = build_system_prompt(Pet("Milo", hunger=85, energy=40, happiness=30))
    assert "Milo" in prompt and "85" in prompt and "hungry" in prompt


def test_no_key_uses_offline_reply_by_mood(monkeypatch):
    post = MagicMock()
    monkeypatch.setattr(companion.requests, "post", post)
    text, online = PetCompanion().reply(Pet("Milo", hunger=90), "สวัสดี")
    assert not online and "Milo" in text and "หิว" in text
    post.assert_not_called()


def test_provider_picked_from_env(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "a")
    assert PetCompanion().provider == "claude"
    monkeypatch.setenv("OPENAI_API_KEY", "o")
    assert PetCompanion().provider == "openai"
    monkeypatch.setenv("GEMINI_API_KEY", "g")
    assert (PetCompanion().provider, PetCompanion().api_key) == ("gemini", "g")
    monkeypatch.setenv("AI_PROVIDER", "Claude")  # บังคับเลือกเองได้
    assert (PetCompanion().provider, PetCompanion().api_key) == ("claude", "a")


@pytest.mark.parametrize("provider, body", [("gemini", GEMINI_OK), ("openai", OPENAI_OK), ("claude", CLAUDE_OK)])
def test_api_success(monkeypatch, provider, body):
    post = MagicMock(return_value=fake_response(body))
    monkeypatch.setattr(companion.requests, "post", post)
    text, online = PetCompanion(provider, api_key="k").reply(Pet("Milo"), "hi")
    assert (text, online) == ("เมี้ยว!", True)
    assert "Milo" in str(post.call_args.kwargs["json"])


@pytest.mark.parametrize("provider", ["gemini", "openai", "claude"])
@pytest.mark.parametrize("behavior", [
    requests.Timeout(),
    requests.ConnectionError(),
    fake_response({"error": "bad"}),                       # ผิดรูปแบบ
    fake_response({"candidates": [], "choices": [], "content": []}),  # ตอบว่าง
])
def test_api_failure_falls_back(monkeypatch, provider, behavior):
    kwargs = {"side_effect": behavior} if isinstance(behavior, Exception) else {"return_value": behavior}
    monkeypatch.setattr(companion.requests, "post", MagicMock(**kwargs))
    text, online = PetCompanion(provider, api_key="k").reply(Pet("Milo"), "hi")
    assert not online and "Milo" in text


@pytest.mark.parametrize("first", [fake_response({}, status=503), requests.Timeout()])
def test_retry_once_on_temporary_error(monkeypatch, first):
    post = MagicMock(side_effect=[first, fake_response(GEMINI_OK)])
    monkeypatch.setattr(companion.requests, "post", post)
    assert PetCompanion("gemini", api_key="k").reply(Pet("Milo"), "hi") == ("เมี้ยว!", True)
    assert post.call_count == 2


def test_gives_up_after_second_failure(monkeypatch):
    post = MagicMock(return_value=fake_response({}, status=503))
    monkeypatch.setattr(companion.requests, "post", post)
    assert PetCompanion("gemini", api_key="k").reply(Pet("Milo"), "hi")[1] is False
    assert post.call_count == 2


def test_model_name_with_prefix(monkeypatch):
    monkeypatch.setenv("GEMINI_MODEL", "models/gemini-x")
    post = MagicMock(return_value=fake_response(GEMINI_OK))
    monkeypatch.setattr(companion.requests, "post", post)
    PetCompanion("gemini", api_key="k").reply(Pet("Milo"), "hi")
    assert "/models/gemini-x:" in post.call_args.args[0]
