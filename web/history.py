# [Sprint 2] เพิ่มระบบจัดการประวัติการโต้ตอบ (Search/Filter/Sort)
import json
import os
from datetime import datetime

HISTORY_FILE = "interaction_history.json"

def load_history():
    """โหลดประวัติจากไฟล์ JSON"""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_history(data):
    """บันทึกประวัติลงไฟล์ JSON"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_entry(source, kind, content):
    """เพิ่ม entry ใหม่ลงในประวัติ"""
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "source": source,
        "kind": kind,
        "content": content
    }
    history = load_history()
    history.append(entry)
    save_history(history)
    return entry

# [Sprint 2] ฟังก์ชันใหม่: ค้นหา กรอง และเรียงลำดับ
def search_history(history, query):
    """ค้นหาประวัติด้วย keyword"""
    if not query:
        return history
    return [h for h in history if query.lower() in h["content"].lower()]

def filter_history(history, source=None, kind=None):
    """กรองประวัติด้วย source หรือ kind"""
    result = history
    if source:
        result = [h for h in result if h["source"] == source]
    if kind:
        result = [h for h in result if h["kind"] == kind]
    return result

def sort_history(history, order="desc"):
    """เรียงลำดับประวัติตาม timestamp"""
    return sorted(history, key=lambda h: h["timestamp"], reverse=(order == "desc"))
