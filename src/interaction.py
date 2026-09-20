# [Sprint 2] ขยาย API Integration (Dog API + Weather API)
import requests

class Interaction:
    @staticmethod
    def fetch_cat_fact():
        try:
            res = requests.get("https://catfact.ninja/fact", timeout=5)
            return res.json().get("fact", "ไม่พบข้อมูลแมว")
        except Exception:
            return "ไม่สามารถเชื่อมต่อ Cat API ได้"

    @staticmethod
    def fetch_dog_image():
        try:
            res = requests.get("https://dog.ceo/api/breeds/image/random", timeout=5)
            return res.json().get("message", "ไม่พบรูปสุนัข")
        except Exception:
            return "ไม่สามารถเชื่อมต่อ Dog API ได้"

    @staticmethod
    def fetch_weather(city="Bangkok"):
        try:
            res = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
            data = res.json()
            condition = data["current_condition"][0]["weatherDesc"][0]["value"]
            return condition
        except Exception:
            return "ไม่สามารถเชื่อมต่อ Weather API ได้"
