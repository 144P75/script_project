"""AI Companion: สัตว์เลี้ยงตอบข้อความตามสถานะจริง (Claude API) พร้อมโหมดออฟไลน์"""
import os
import random

import requests

API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MAX_MESSAGE_LENGTH = 200
MAX_TOKENS = 150
TIMEOUT = 10

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
    """มี API key → ถาม Claude API, ไม่มี key หรือ API ใช้ไม่ได้ → ตอบแบบออฟไลน์ตามอารมณ์"""

    def __init__(self, api_key=None, model=None, timeout=TIMEOUT):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY", "") if api_key is None else api_key
        self.model = model or os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
        self.timeout = timeout

    def reply(self, pet, message):
        """คืน (ข้อความตอบ, True ถ้าตอบโดย AI จริง)"""
        if self.api_key:
            try:
                text = self._ask_api(pet, message)
                if text:
                    return text, True
            except (requests.RequestException, ValueError, KeyError, TypeError):
                pass
        return self.offline_reply(pet), False

    @staticmethod
    def offline_reply(pet):
        return random.choice(OFFLINE_REPLIES[pet.mood_tracker.get_mood_key()]).format(name=pet.name)

    def _ask_api(self, pet, message):
        response = requests.post(
            API_URL,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": self.model,
                "max_tokens": MAX_TOKENS,
                "system": build_system_prompt(pet),
                "messages": [{"role": "user", "content": message}],
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        blocks = response.json()["content"]
        return "".join(b.get("text", "") for b in blocks if b.get("type") == "text").strip()
