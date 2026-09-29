"""Presentation Layer: แสดงผลและรับอินพุตผ่าน Command Line"""
from src.exceptions import InvalidInputError

COMMANDS = {
    "feed": "ให้อาหาร",
    "play": "เล่นด้วย",
    "sleep": "ให้นอนพัก",
    "fact": "ใช้เวลาด้วยกัน + เกร็ดความรู้แมว",
    "pets": "ดูสัตว์เลี้ยงทั้งหมด",
    "addpet": "เพิ่มสัตว์เลี้ยง",
    "switchpet": "สลับสัตว์เลี้ยง",
    "renamepet": "เปลี่ยนชื่อสัตว์เลี้ยง",
    "removepet": "ลบสัตว์เลี้ยง",
    "history": "ดู/ค้นหา/กรอง/เรียงประวัติ",
    "help": "แสดงคำสั่งทั้งหมด",
    "quit": "บันทึกและออก",
}


def bar(value, width=10):
    filled = round(value / 100 * width)
    return "█" * filled + "░" * (width - filled)


def shorten(text, width):
    text = str(text).replace("\n", " ")
    return text if len(text) <= width else text[:width - 1] + "…"


class CLIHandler:
    """รวมฟังก์ชันแสดงผลทั้งหมดของ CLI"""

    @staticmethod
    def display_welcome():
        print("=" * 50)
        print("     VIRTUAL PET SIMULATOR (AI Companion)     ")
        print("=" * 50)
        print("พิมพ์ help เพื่อดูคำสั่งทั้งหมด")

    @staticmethod
    def display_status(pet):
        print(f"\n--- สถานะของ {pet['name']} [{pet['mood']}] ---")
        print(f"  ความหิว (Hunger)   : {bar(pet['hunger'])} {pet['hunger']:>3}/100")
        print(f"  พลังงาน (Energy)   : {bar(pet['energy'])} {pet['energy']:>3}/100")
        print(f"  ความสุข (Happiness): {bar(pet['happiness'])} {pet['happiness']:>3}/100")
        print("-" * 44)

    @staticmethod
    def display_help():
        print("\nคำสั่งที่ใช้ได้:")
        for cmd, desc in COMMANDS.items():
            print(f"  {cmd:<10} {desc}")

    @staticmethod
    def display_table(rows, columns):
        """rows = list[dict], columns = list[(key, หัวตาราง, ความกว้าง)]"""
        if not rows:
            print("\n--- ไม่พบข้อมูล ---")
            return
        header = " | ".join(f"{title:<{width}}" for _, title, width in columns)
        print("\n" + header)
        print("-" * len(header))
        for row in rows:
            print(" | ".join(f"{shorten(row.get(key, ''), width):<{width}}" for key, _, width in columns))
        print(f"({len(rows)} รายการ)")

    @staticmethod
    def display_message(text):
        print(f"\n> {text}")

    @staticmethod
    def display_error(text):
        print(f"\n[ข้อผิดพลาด] {text}")

    @staticmethod
    def ask(prompt):
        return input(prompt).strip()

    @staticmethod
    def get_command_input():
        return input("\nเลือกคำสั่ง (help = ดูทั้งหมด): ").strip().lower()

    @staticmethod
    def choose(prompt, options, allow_blank=False):
        """ให้เลือกจากรายการด้วยหมายเลข คืนค่าที่เลือก หรือ None ถ้าเว้นว่าง"""
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        hint = " (Enter = ข้าม)" if allow_blank else ""
        raw = input(f"{prompt}{hint}: ").strip()
        if not raw and allow_blank:
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        raise InvalidInputError(f"กรุณาเลือกหมายเลข 1-{len(options)}")
