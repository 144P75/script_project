"""ประวัติการโต้ตอบ: บันทึกลงไฟล์ (Data Access) และค้นหา/กรอง/เรียงลำดับ (Data Processing)"""
from datetime import datetime

from src.exceptions import InvalidInputError
from src.storage import JsonStore

HISTORY_SORT_KEYS = ("timestamp", "source", "kind", "pet")
MAX_ENTRIES = 5000


def _text(entry, field):
    return str(entry.get(field) or "")


def search_history(entries, keyword):
    """ค้นหาแบบไม่สนตัวพิมพ์ใน content, pet, kind และ source — คำว่างคืนทั้งหมด"""
    keyword = (keyword or "").strip().casefold()
    if not keyword:
        return list(entries)
    fields = ("content", "pet", "kind", "source")
    return [e for e in entries if any(keyword in _text(e, f).casefold() for f in fields)]


def filter_history(entries, source=None, kind=None, pet=None, since=None, until=None):
    """กรองตามค่าที่ระบุ (ค่า None หรือว่าง = ไม่กรอง) since/until เป็น ISO date/time"""
    result = list(entries)
    for field, value in (("source", source), ("kind", kind), ("pet", pet)):
        if value:
            result = [e for e in result if _text(e, field).casefold() == str(value).casefold()]
    if since:
        result = [e for e in result if _text(e, "timestamp") >= since]
    if until:
        result = [e for e in result if _text(e, "timestamp")[:len(until)] <= until]
    return result


def parse_sort_keys(sort_by):
    """รับ 'kind,timestamp' หรือ list แล้วคืน list ของคีย์ที่ตรวจสอบแล้ว"""
    keys = sort_by.split(",") if isinstance(sort_by, str) else list(sort_by or [])
    keys = [k.strip() for k in keys if k and k.strip()] or ["timestamp"]
    invalid = [k for k in keys if k not in HISTORY_SORT_KEYS]
    if invalid:
        raise InvalidInputError(f"เรียงได้ตาม: {', '.join(HISTORY_SORT_KEYS)}")
    return keys


def sort_history(entries, sort_by="timestamp", order="desc"):
    """เรียงตามหลายคีย์ เช่น sort_by='kind,timestamp'"""
    if order not in ("asc", "desc"):
        raise InvalidInputError("order ต้องเป็น asc หรือ desc")
    keys = parse_sort_keys(sort_by)
    return sorted(
        entries,
        key=lambda e: tuple(_text(e, k).casefold() for k in keys),
        reverse=(order == "desc"),
    )


class InteractionHistory:
    """เก็บประวัติการโต้ตอบลงไฟล์ JSON"""

    def __init__(self, path="interaction_history.json", backup_path="interaction_history_backup.json"):
        self.store = JsonStore(path, backup_path, default_factory=list)

    def load(self):
        entries, _ = self.store.load()
        return [e for e in entries if isinstance(e, dict)]

    def add(self, source, kind, content, pet=None):
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "source": source,
            "kind": kind,
            "pet": pet or "",
            "content": content,
        }
        entries = self.load()
        entries.append(entry)
        self.store.save(entries[-MAX_ENTRIES:])
        return entry

    def query(self, keyword="", source=None, kind=None, pet=None, sort_by="timestamp", order="desc"):
        entries = search_history(self.load(), keyword)
        entries = filter_history(entries, source=source, kind=kind, pet=pet)
        return sort_history(entries, sort_by=sort_by, order=order)

    def distinct(self, field):
        return sorted({_text(e, field) for e in self.load() if _text(e, field)})
