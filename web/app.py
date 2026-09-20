# [Sprint 2] เพิ่ม Web API Layer
from flask import Flask, jsonify, request
import random
import requests
from web import history

app = Flask(__name__)

@app.route("/api/interact")
def api_interact():
    try:
        if random.choice([True, False]):
            res = requests.get("https://dog.ceo/api/breeds/image/random", timeout=5)
            res.raise_for_status()
            data = res.json()
            entry = history.add_entry("Dog API", "image", data["message"])
            return jsonify({"source": "Dog API", "interaction": entry})
        else:
            res = requests.get("https://catfact.ninja/fact", timeout=5)
            res.raise_for_status()
            data = res.json()
            entry = history.add_entry("Cat Facts API", "fact", data["fact"])
            return jsonify({"source": "Cat Facts API", "interaction": entry})
    except requests.exceptions.Timeout:
        return jsonify({"error": "API timeout"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "API connection error"}), 502
    except Exception:
        return jsonify({"error": "Unexpected error"}), 502

@app.route("/api/history")
def api_history():
    q = request.args.get("q", "")
    source = request.args.get("source")
    kind = request.args.get("kind")
    order = request.args.get("order", "desc")

    data = history.load_history()
    data = history.search_history(data, q)
    data = history.filter_history(data, source=source, kind=kind)
    data = history.sort_history(data, order=order)

    return jsonify({"count": len(data), "results": data})
