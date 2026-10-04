"""AI Companion: สัตว์เลี้ยงตอบข้อความตามสถานะจริง (Gemini / ChatGPT / Claude) พร้อมโหมดออฟไลน์"""
import os
import random

import requests

MAX_MESSAGE_LENGTH = 200
TIMEOUT = 10

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GEMINI_MODEL = "gemini-flash-latest"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"
CLAUDE_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# provider -> ชื่อ environment variable ของ key (เรียงตามลำดับที่เลือกใช้ก่อน)
PROVIDERS = {"gemini": "GEMINI_API_KEY", "openai": "OPENAI_API_KEY", "claude": "ANTHROPIC_API_KEY"}

OFFLINE_REPLIES = {
    "hungry": ["เมี้ยว... {name} หิวจนท้องร้องแล้ว ขอข้าวก่อนได้ไหม 🍖",
               "{name} ฟังอยู่นะ แต่หิวมากเลย ให้อาหารหน่อยน้า"],
    "sleepy": ["หาววว... {name} ง่วงมาก ขอนอนก่อนนะ 💤",
               "{name} ตาจะปิดแล้ว คุยต่อพรุ่งนี้ได้ไหม"],
    "happy": ["เมี้ยว! {name} ดีใจที่ได้คุยด้วย ไปเล่นกันเถอะ 🎾",
              "{name} คลอเคลียขาคุณอย่างมีความสุข 😸"],
    "ok": ["เมี้ยว~ {name} ฟังอยู่นะ", "{name} เอียงหัวมองคุณอย่างสงสัย 😺"],
}


def build_system_prompt(pet):
    m = pet.mood_tracker
    return (
        f"คุณคือแมวชื่อ {pet.name} ในเกมเลี้ยงสัตว์เสมือน ตอบในบทบาทของแมวตัวนี้เท่านั้น\n"
        f"สถานะตอนนี้ (0-100): ความหิว {m.hunger} (ยิ่งมากยิ่งหิว), พลังงาน {m.energy}, "
        f"ความสุข {m.happiness}, อารมณ์: {m.get_mood_key()}\n"
        "ให้คำตอบสะท้อนสถานะนี้ เช่น หิวมากก็ขออาหาร ง่วงก็ขอนอน มีความสุขก็ชวนเล่น\n"
        "ตอบสั้น 1-2 ประโยค เป็นภาษาเดียวกับผู้ใช้ น่ารักแบบแมว ไม่ต้องอธิบายว่าเป็น AI"
    )


class PetCompanion:
    """ใช้ AI_PROVIDER ถ้าตั้งไว้ ไม่งั้นใช้เจ้าแรกที่มี key — ไม่มี key หรือ API ใช้ไม่ได้ → ออฟไลน์"""

    def __init__(self, provider=None, api_key=None, timeout=TIMEOUT):
        provider = provider or os.environ.get("AI_PROVIDER", "").strip().lower() or next(
            (name for name, env in PROVIDERS.items() if os.environ.get(env)), None)
        self.provider = provider if provider in PROVIDERS else None
        self.api_key = api_key if api_key is not None else os.environ.get(PROVIDERS.get(self.provider, ""), "")
        self.timeout = timeout

    def reply(self, pet, message):
        """คืน (ข้อความตอบ, True ถ้าตอบโดย AI จริง)"""
        if self.provider and self.api_key:
            try:
                ask = getattr(self, f"_ask_{self.provider}")
                text = ask(build_system_prompt(pet), message)
                if text:
                    return text, True
            except (requests.RequestException, ValueError, KeyError, TypeError, IndexError):
                pass
        return self.offline_reply(pet), False

    @staticmethod
    def offline_reply(pet):
        return random.choice(OFFLINE_REPLIES[pet.mood_tracker.get_mood_key()]).format(name=pet.name)

    def _ask_gemini(self, system, message):
        model = os.environ.get("GEMINI_MODEL", GEMINI_MODEL)
        response = requests.post(
            GEMINI_URL.format(model=model),
            headers={"x-goog-api-key": self.api_key},
            json={
                "system_instruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": message}]}],
                "generationConfig": {"maxOutputTokens": 1024},
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        parts = response.json()["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts).strip()

    def _ask_openai(self, system, message):
        response = requests.post(
            OPENAI_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": os.environ.get("OPENAI_MODEL", OPENAI_MODEL),
                "max_completion_tokens": 1024,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return (response.json()["choices"][0]["message"]["content"] or "").strip()

    def _ask_claude(self, system, message):
        response = requests.post(
            CLAUDE_URL,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": os.environ.get("ANTHROPIC_MODEL", CLAUDE_MODEL),
                "max_tokens": 150,
                "system": system,
                "messages": [{"role": "user", "content": message}],
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        blocks = response.json()["content"]
        return "".join(b.get("text", "") for b in blocks if b.get("type") == "text").strip()
