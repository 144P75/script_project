from src.cli import CLIHandler
from src.exceptions import PetError
from src.history import InteractionHistory
from src.pet_manager import PetManager

HISTORY_SOURCES = {"1": ("User", {"1": "feed", "2": "play", "3": "sleep"}), "2": ("Cat Facts API", None)}


def print_entries(entries):
    if not entries:
        print("\n--- ไม่พบข้อมูล ---")
        return
    for e in entries:
        print(f"[{e['timestamp']}] {e.get('pet') or '-'} | {e['source']} ({e['kind']}): {e['content']}")


def history_menu(history):
    while True:
        print("\n--- History Menu ---")
        print("1. ดู 5 รายการล่าสุด")
        print("2. ค้นหาตามคำค้นหา (keyword)")
        print("3. กรองตามแหล่งที่มา/ประเภทกิจกรรม")
        print("4. เรียงลำดับ (เลือกได้หลายคีย์)")
        print("5. กลับไปเมนูหลัก")
        choice = input("เลือกเมนูย่อย: ").strip()
        try:
            if choice == "1":
                print_entries(history.query()[:5])
            elif choice == "2":
                print_entries(history.query(keyword=input("🔎 กรอก Keyword: ")))
            elif choice == "3":
                src_choice = input("แหล่งที่มา 1. User  2. Cat Facts API : ").strip()
                if src_choice not in HISTORY_SOURCES:
                    print("\n[คำสั่งไม่ถูกต้อง] กรุณาเลือก 1 หรือ 2")
                    continue
                source, kinds = HISTORY_SOURCES[src_choice]
                kind = kinds.get(input("ประเภท 1. feed  2. play  3. sleep : ").strip()) if kinds else None
                print_entries(history.query(source=source, kind=kind))
            elif choice == "4":
                keys = input("เรียงตาม (timestamp/source/kind/pet คั่นด้วย , ): ").strip() or "timestamp"
                order = "asc" if input("1. น้อย→มาก  2. มาก→น้อย : ").strip() == "1" else "desc"
                print_entries(history.query(sort_by=keys, order=order))
            elif choice == "5":
                return
            else:
                print("\n[คำสั่งไม่ถูกต้อง] กรุณาเลือก 1–5")
        except PetError as e:
            print(f"\n[ข้อผิดพลาด] {e.message}")


def main():
    CLIHandler.display_welcome()
    manager = PetManager()
    history = InteractionHistory()
    warning = manager.pop_warning()
    if warning:
        print(f"\n[คำเตือน] {warning}")

    try:
        while True:
            try:
                if manager.active_pet is None:
                    pet = manager.add_pet(input("กรุณาตั้งชื่อสัตว์เลี้ยงของคุณ: "))
                    print(f"\nยินดีต้อนรับ {pet.name}!")
                    continue

                pet = manager.active_pet
                CLIHandler.display_status(pet)
                cmd = CLIHandler.get_command_input()

                if cmd in ["quit", "exit"]:
                    break
                elif cmd in ["feed", "play", "sleep", "fact"]:
                    msg = pet.interact_api() if cmd == "fact" else getattr(pet, cmd)()
                    print(f"\n> {msg}")
                    manager.save()
                    history.add("Cat Facts API" if cmd == "fact" else "User", cmd, msg, pet=pet.name)
                elif cmd == "save":
                    manager.save()
                    print("\n> บันทึกสถานะสัตว์เลี้ยงสำเร็จ!")
                elif cmd == "addpet":
                    new_pet = manager.add_pet(input("ตั้งชื่อสัตว์เลี้ยงใหม่: "))
                    print(f"\n> เพิ่ม {new_pet.name} เรียบร้อย")
                elif cmd == "switchpet":
                    new_pet = manager.switch_pet(input("สลับไปยังสัตว์เลี้ยงชื่อ: "))
                    print(f"\n> สลับไปยัง {new_pet.name} เรียบร้อย")
                elif cmd == "history":
                    history_menu(history)
                else:
                    print("\n[คำสั่งไม่ถูกต้อง] กรุณาพิมพ์: feed, play, sleep, fact, save, "
                          "addpet, switchpet, history หรือ quit")
            except PetError as e:
                print(f"\n[ข้อผิดพลาด] {e.message}")
    except (KeyboardInterrupt, EOFError):
        print()
    manager.save()
    print("\nบันทึกข้อมูลเรียบร้อย ลาก่อน! 👋")


if __name__ == "__main__":
    main()
