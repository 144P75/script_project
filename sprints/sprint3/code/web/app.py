"""Presentation Layer (Web): Flask API + หน้าเว็บเกม

รัน: python -m web.app แล้วเปิด http://127.0.0.1:5000
ทุก route เรียก PetService ตัวเดียวกับ CLI จึงใช้ข้อมูลชุดเดียวกัน
"""
import os

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException

from src.exceptions import InvalidInputError, PetError
from src.service import PetService

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


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


def create_app(service=None):
    app = Flask(__name__, static_folder=None)
    app.json.ensure_ascii = False
    svc = service or PetService()

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
        return jsonify(svc.status())

    @app.post("/api/pet/actions/<action>")
    def pet_action(action):
        return jsonify(svc.perform(action))

    # ----- CRUD สัตว์เลี้ยง -----
    @app.get("/api/pets")
    def list_pets():
        pets = svc.list_pets(request.args.get("sort_by", "name"), request.args.get("order", "asc"))
        active = next((p["name"] for p in pets if p["active"]), None)
        return jsonify({"pets": pets, "active": active})

    @app.post("/api/pets")
    def create_pet():
        return jsonify(svc.create_pet(_json_body().get("name"))), 201

    @app.put("/api/pets/<name>")
    def rename_pet(name):
        return jsonify(svc.rename_pet(name, _json_body().get("new_name")))

    @app.delete("/api/pets/<name>")
    def delete_pet(name):
        return jsonify(svc.delete_pet(name))

    @app.post("/api/pets/<name>/select")
    def select_pet(name):
        return jsonify(svc.select_pet(name))

    # ----- ประวัติ -----
    @app.get("/api/history")
    def history():
        args = request.args
        results = svc.query_history(
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
            "filters": svc.history_filters(),
        })

    @app.get("/api/warning")
    def warning():
        return jsonify({"warning": svc.pop_warning()})

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)))
