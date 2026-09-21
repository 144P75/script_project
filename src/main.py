import sys
from src.cli import CLIHandler
from src.pet_manager import PetManager
from web import history


def main():
    CLIHandler.display_welcome()
    manager = PetManager()

    if not manager.pets:
        name = input("กรุณาตั้งชื่อสัตว์เลี้ยงของคุณ: ").strip() or "Buddy"
        print(manager.add_pet(name))
    else:
        print(f"\nต้อนรับการกลับมา! โหลดข้อมูลของ {manager.active_pet.name} เรียบร้อย")

    while True:
        CLIHandler.display_status(manager.active_pet)
        cmd = CLIHandler.get_command_input()

        if cmd in ["quit", "exit"]:
            manager.save_pets()
            print(f"\nบันทึกข้อมูลเรียบร้อย ลาก่อนจาก {manager.active_pet.name}! 👋")
            sys.exit(0)

        elif cmd == "feed":
            msg = manager.active_pet.feed()
            print(f"\n> {msg}")
            history.add_entry("User", "feed", msg)
            manager.save_pets()

        elif cmd == "play":
            msg = manager.active_pet.play()
            print(f"\n> {msg}")
            history.add_entry("User", "play", msg)
            manager.save_pets()

        elif cmd == "sleep":
            msg = manager.active_pet.sleep()
            print(f"\n> {msg}")
            history.add_entry("User", "sleep", msg)
            manager.save_pets()

        elif cmd == "fact":
            msg = manager.active_pet.interact_api()
            print(f"\n> {msg}")
            history.add_entry("Cat Facts API", "fact", msg)
            manager.save_pets()

        elif cmd == "save":
            manager.save_pets()
            print("\n> บันทึกสถานะสัตว์เลี้ยงสำเร็จ!")

        elif cmd == "addpet":
            name = input("ตั้งชื่อสัตว์เลี้ยงใหม่: ").strip()
            print(manager.add_pet(name))

        elif cmd == "switchpet":
            name = input("สลับไปยังสัตว์เลี้ยงชื่อ: ").strip()
            print(manager.switch_pet(name))

        elif cmd == "history":
            while True:
                print("\n--- History Menu ---")
                print("1. ดู 5 รายการล่าสุด")
                print("2. ค้นหาตามคำค้นหา (keyword)")
                print("3. กรองตามแหล่งที่มา/ประเภทกิจกรรม")
                print("4. เรียงลำดับเวลา")
                print("5. กลับไปเมนูหลัก")
                choice = input("เลือกเมนูย่อย: ").strip()

                data = history.load_history()
                if not data:
                    print("\n--- ยังไม่มีประวัติการโต้ตอบ ---")
                else:
                    if choice == "1":
                        for entry in reversed(data[-5:]):
                            print(f"[{entry['timestamp']}] {entry['source']} ({entry['kind']}): {entry['content']}")

                    elif choice == "2":
                        keyword = input("🔎 กรอก Keyword: ").strip()
                        results = history.search_history(data, keyword)
                        if not results:
                            print("\n--- ไม่พบข้อมูลที่ตรงกับคำค้นหา ---")
                        else:
                            for entry in results:
                                print(f"[{entry['timestamp']}] {entry['source']} ({entry['kind']}): {entry['content']}")

                    elif choice == "3":
                        print("เลือกแหล่งที่มา:")
                        print("1. User")
                        print("2. Fact")
                        src_choice = input("พิมพ์หมายเลข: ").strip()

                        if src_choice == "1":
                            src = "User"
                            print("เลือกประเภทกิจกรรม: User")
                            print("1. feed")
                            print("2. play")
                            print("3. sleep")
                            kind_choice = input("พิมพ์หมายเลข: ").strip()
                            kind_map = {"1": "feed", "2": "play", "3": "sleep"}
                            kind = kind_map.get(kind_choice)
                        elif src_choice == "2":
                            src = "Cat Facts API"
                            kind = "fact"
                        else:
                            print("\n[คำสั่งไม่ถูกต้อง] กรุณาเลือก 1 หรือ 2")
                            continue

                        results = history.filter_history(data, source=src, kind=kind)
                        if not results:
                            print("\n--- ไม่พบข้อมูลที่ตรงกับการกรอง ---")
                        else:
                            for entry in results:
                                print(f"[{entry['timestamp']}] {entry['source']} ({entry['kind']}): {entry['content']}")

                    elif choice == "4":
                        print("เลือกการเรียงลำดับเวลา:")
                        print("1. เก่าสุดก่อน")
                        print("2. ใหม่สุดก่อน")
                        order_choice = input("พิมพ์หมายเลข: ").strip()
                        order = "asc" if order_choice == "1" else "desc" if order_choice == "2" else None
                        if not order:
                            print("\n[คำสั่งไม่ถูกต้อง] กรุณาเลือก 1 หรือ 2")
                            continue
                        results = history.sort_history(data, order)
                        for entry in results:
                            print(f"[{entry['timestamp']}] {entry['source']} ({entry['kind']}): {entry['content']}")

                    elif choice == "5":
                        break

                    else:
                        print("\n[คำสั่งไม่ถูกต้อง] กรุณาเลือก 1–5")

        else:
            print("\n[คำสั่งไม่ถูกต้อง] กรุณาพิมพ์: feed, play, sleep, fact, save, add pet, switch pet, history หรือ quit")


if __name__ == "__main__":
    main()
