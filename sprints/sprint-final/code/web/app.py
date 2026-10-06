"""Presentation Layer (Web): Flask API + หน้าเว็บเกม

รัน: python -m web.app แล้วเปิด http://127.0.0.1:5000
บน server (Render): gunicorn "web.app:create_app()" ดู render.yaml
ทุก route เรียก PetService ตัวเดียวกับ CLI จึงใช้ข้อมูลชุดเดียวกัน
"""
import os
import re
import threading

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException

from src.exceptions import InvalidInputError, PetError
from src.history import InteractionHistory
from src.pet_manager import PetManager
from src.service import PetService

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
PLAYER_ID = re.compile(r"[A-Za-z0-9-]{16,64}")  # กันรหัสแปลกๆ เช่น ../ ที่อาจใช้อ่านไฟล์นอกโฟลเดอร์


def _json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise InvalidInputError("ต้องส่งข้อมูลเป็น JSON object")
    return data


def _int_arg(name, default):
    raw = request.args.get(name)
    if raw in (None, ""):
        return default
    if not raw.isdigit():
        raise InvalidInputError(f"{name} ต้องเป็นจำนวนเต็มบวก")
    return int(raw)


def create_app(service=None, multi_player=None, data_dir="data/players"):
    """multi_player=True (หรือ MULTI_PLAYER=1): แยกข้อมูลตามรหัสผู้เล่นใน header X-Player-Id
    ปิดไว้ (ค่าเริ่มต้นตอนรันในเครื่อง): ใช้ข้อมูลชุดเดียวกับ CLI"""
    app = Flask(__name__, static_folder=None)
    app.json.ensure_ascii = False
    if multi_player is None:
        multi_player = os.environ.get("MULTI_PLAYER") == "1"
    shared = None if multi_player else (service or PetService())
    players = {}
    players_lock = threading.Lock()

    def player_service(player_id):
        if not PLAYER_ID.fullmatch(player_id or ""):
            raise InvalidInputError("ไม่พบรหัสผู้เล่น กรุณารีเฟรชหน้าเว็บ")
        with players_lock:
            if player_id not in players:
                folder = os.path.join(data_dir, player_id)
                players[player_id] = PetService(
                    manager=PetManager(os.path.join(folder, "pets.json"), os.path.join(folder, "pets_backup.json")),
                    history=InteractionHistory(os.path.join(folder, "history.json"),
                                               os.path.join(folder, "history_backup.json")),
                )
            return players[player_id]

    def svc():
        return player_service(request.headers.get("X-Player-Id")) if multi_player else shared

    @app.errorhandler(PetError)
    def handle_pet_error(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(Exception)
    def handle_unexpected(error):
        if isinstance(error, HTTPException):
            return jsonify({"error": error.description}), error.code
        app.logger.exception(error)
        return jsonify({"error": "เกิดข้อผิดพลาดภายในระบบ"}), 500

    @app.get("/")
    def index():
        return send_from_directory(STATIC_DIR, "index.html")

    # ----- สัตว์เลี้ยงที่กำลังใช้งาน -----
    @app.get("/api/pet")
    def get_active_pet():
        return jsonify(svc().status())

    @app.post("/api/pet/actions/<action>")
    def pet_action(action):
        return jsonify(svc().perform(action))

    @app.post("/api/pet/talk")
    def pet_talk():
        return jsonify(svc().talk(_json_body().get("message")))

    # ----- CRUD สัตว์เลี้ยง -----
    @app.get("/api/pets")
    def list_pets():
        pets = svc().list_pets(request.args.get("sort_by", "name"), request.args.get("order", "asc"))
        active = next((p["name"] for p in pets if p["active"]), None)
        return jsonify({"pets": pets, "active": active})

    @app.post("/api/pets")
    def create_pet():
        return jsonify(svc().create_pet(_json_body().get("name"))), 201

    @app.put("/api/pets/<name>")
    def rename_pet(name):
        return jsonify(svc().rename_pet(name, _json_body().get("new_name")))

    @app.delete("/api/pets/<name>")
    def delete_pet(name):
        return jsonify(svc().delete_pet(name))

    @app.post("/api/pets/<name>/select")
    def select_pet(name):
        return jsonify(svc().select_pet(name))

    # ----- ประวัติ -----
    @app.get("/api/history")
    def history():
        args = request.args
        results = svc().query_history(
            keyword=args.get("q", ""),
            source=args.get("source") or None,
            kind=args.get("kind") or None,
            pet=args.get("pet") or None,
            sort_by=args.get("sort_by", "timestamp"),
            order=args.get("order", "desc"),
        )
        limit = _int_arg("limit", 100)
        return jsonify({
            "count": len(results),
            "results": results[:limit],
            "filters": svc().history_filters(),
        })

    @app.get("/api/warning")
    def warning():
        return jsonify({"warning": svc().pop_warning()})

    return app


if __name__ == "__main__":
    load_dotenv()  # อ่าน API key จากไฟล์ .env (ถ้ามี)
    create_app().run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)))
