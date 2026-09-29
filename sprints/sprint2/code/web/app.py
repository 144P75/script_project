# [Sprint 2] Web API Layer — เตรียมไว้เชื่อมกับหน้าเว็บใน Sprint 3
import random

import requests
from flask import Flask, jsonify, request

from src.exceptions import PetError
from src.history import InteractionHistory

app = Flask(__name__)
app.json.ensure_ascii = False
history = InteractionHistory()


@app.errorhandler(PetError)
def handle_pet_error(error):
    return jsonify({"error": error.message}), error.status_code


@app.route("/api/interact")
def api_interact():
    try:
        if random.choice([True, False]):
            res = requests.get("https://dog.ceo/api/breeds/image/random", timeout=5)
            res.raise_for_status()
            entry = history.add("Dog API", "image", res.json()["message"])
            return jsonify({"source": "Dog API", "interaction": entry})
        res = requests.get("https://catfact.ninja/fact", timeout=5)
        res.raise_for_status()
        entry = history.add("Cat Facts API", "fact", res.json()["fact"])
        return jsonify({"source": "Cat Facts API", "interaction": entry})
    except requests.exceptions.Timeout:
        return jsonify({"error": "API timeout"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "API connection error"}), 502
    except (requests.RequestException, ValueError, KeyError):
        return jsonify({"error": "Unexpected error"}), 502


@app.route("/api/history")
def api_history():
    args = request.args
    data = history.query(
        keyword=args.get("q", ""),
        source=args.get("source") or None,
        kind=args.get("kind") or None,
        pet=args.get("pet") or None,
        sort_by=args.get("sort_by", "timestamp"),
        order=args.get("order", "desc"),
    )
    return jsonify({"count": len(data), "results": data})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
