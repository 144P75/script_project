"""Entry point ของ CLI: python -m src.main"""
import sys

from src.cli import COMMANDS, CLIHandler
from src.exceptions import InvalidInputError, PetError
from src.pet_manager import PET_SORT_KEYS
from src.service import ACTIONS, PetService

if hasattr(sys.stdout, "reconfigure"):  # ให้ภาษาไทยแสดงผลได้บน Windows
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

HISTORY_COLUMNS = [
    ("timestamp", "เวลา", 19),
    ("pet", "สัตว์เลี้ยง", 10),
    ("source", "แหล่งที่มา", 14),
    ("kind", "ประเภท", 7),
    ("content", "รายละเอียด", 40),
]
PET_COLUMNS = [
    ("marker", " ", 1),
    ("name", "ชื่อ", 20),
    ("hunger", "หิว", 4),
    ("energy", "พลังงาน", 7),
    ("happiness", "สุข", 4),
    ("mood", "อารมณ์", 18),
]


def ask_new_pet(service):
    name = CLIHandler.ask("ตั้งชื่อสัตว์เลี้ยงของคุณ: ")
    pet = service.create_pet(name)
    CLIHandler.display_message(f"ยินดีต้อนรับ {pet['name']}!")


def cmd_pets(service):
    sort_by = CLIHandler.choose("เรียงตาม", list(PET_SORT_KEYS), allow_blank=True) or "name"
    order = "desc" if sort_by in ("hunger", "energy", "happiness") else "asc"
    pets = service.list_pets(sort_by, order)
    for pet in pets:
        pet["marker"] = "*" if pet["active"] else ""
    CLIHandler.display_table(pets, PET_COLUMNS)
    print("(* = ตัวที่กำลังใช้งาน)")


def cmd_addpet(service):
    ask_new_pet(service)


def cmd_switchpet(service):
    pet = service.select_pet(CLIHandler.ask("สลับไปยังสัตว์เลี้ยงชื่อ: "))
    CLIHandler.display_message(f"สลับไปยัง {pet['name']} เรียบร้อย")


def cmd_renamepet(service):
    old = CLIHandler.ask("ชื่อเดิม: ")
    new = CLIHandler.ask("ชื่อใหม่: ")
    pet = service.rename_pet(old, new)
    CLIHandler.display_message(f"เปลี่ยนชื่อเป็น {pet['name']} เรียบร้อย")


def cmd_removepet(service):
    name = CLIHandler.ask("ชื่อสัตว์เลี้ยงที่จะลบ: ")
    if CLIHandler.ask(f"ยืนยันการลบ '{name}'? (y/n): ").lower() != "y":
        CLIHandler.display_message("ยกเลิกการลบ")
        return
    result = service.delete_pet(name)
    CLIHandler.display_message(f"ลบ {result['deleted']} เรียบร้อย")


def cmd_history(service):
    menu = ["ดู 10 รายการล่าสุด", "ค้นหาด้วยคำค้น", "กรองตามแหล่งที่มา/ประเภท/สัตว์เลี้ยง",
            "เรียงลำดับ", "กลับเมนูหลัก"]
    while True:
        print("\n--- History Menu ---")
        try:
            choice = CLIHandler.choose("เลือกเมนูย่อย", menu)
            if choice == menu[0]:
                rows = service.query_history(limit=10)
            elif choice == menu[1]:
                rows = service.query_history(keyword=CLIHandler.ask("คำค้นหา: "))
            elif choice == menu[2]:
                filters = service.history_filters()
                picked = {}
                for field, title in (("sources", "แหล่งที่มา"), ("kinds", "ประเภทกิจกรรม"), ("pets", "สัตว์เลี้ยง")):
                    print(f"{title}:")
                    options = filters[field]
                    picked[field] = CLIHandler.choose("เลือก", options, allow_blank=True) if options else None
                rows = service.query_history(source=picked["sources"], kind=picked["kinds"], pet=picked["pets"])
            elif choice == menu[3]:
                raw = CLIHandler.ask("เรียงตาม (timestamp/source/kind/pet คั่นด้วย , เช่น kind,timestamp): ")
                order = "asc" if CLIHandler.ask("1 = เก่า→ใหม่ / A→Z, 2 = ใหม่→เก่า / Z→A: ") == "1" else "desc"
                rows = service.query_history(sort_by=raw or "timestamp", order=order)
            else:
                return
            rows = [dict(r, timestamp=r["timestamp"].replace("T", " ")) for r in rows]
            CLIHandler.display_table(rows, HISTORY_COLUMNS)
        except PetError as e:
            CLIHandler.display_error(e.message)


HANDLERS = {
    "pets": cmd_pets,
    "addpet": cmd_addpet,
    "switchpet": cmd_switchpet,
    "renamepet": cmd_renamepet,
    "removepet": cmd_removepet,
    "history": cmd_history,
    "help": lambda service: CLIHandler.display_help(),
}


def run_command(service, cmd):
    if cmd in ACTIONS:
        CLIHandler.display_message(service.perform(cmd)["message"])
    elif cmd in HANDLERS:
        HANDLERS[cmd](service)
    else:
        raise InvalidInputError(f"ไม่รู้จักคำสั่ง '{cmd}' พิมพ์ help เพื่อดูคำสั่ง ({', '.join(COMMANDS)})")


def main(service=None):
    service = service or PetService()
    CLIHandler.display_welcome()
    warning = service.pop_warning()
    if warning:
        CLIHandler.display_error(warning)
    try:
        while True:
            try:
                if not service.has_pet():
                    ask_new_pet(service)
                    continue
                CLIHandler.display_status(service.status())
                cmd = CLIHandler.get_command_input()
                if cmd in ("quit", "exit"):
                    break
                run_command(service, cmd)
            except PetError as e:
                CLIHandler.display_error(e.message)
    except (KeyboardInterrupt, EOFError):
        print()
    print("\nบันทึกข้อมูลเรียบร้อย ลาก่อน! 👋")


if __name__ == "__main__":
    main()
