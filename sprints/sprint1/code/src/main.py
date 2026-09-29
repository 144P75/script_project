import sys
import json
import os
from src.pet import Pet
from src.cli import CLIHandler

DATA_FILE = "pet_state.json"


def load_pet_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Warning] ไม่สามารถอ่านไฟล์ข้อมูลได้: {e}")
        return None


def save_pet_data(pet: Pet):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(pet.to_dict(), f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[Error] ไม่สามารถบันทึกข้อมูลได้: {e}")
        return False


def main():
    CLIHandler.display_welcome()
    pet_data = load_pet_data()

    if pet_data:
        pet = Pet.from_dict(pet_data)
        print(f"\nต้อนรับการกลับมา! โหลดข้อมูลของ {pet.name} เรียบร้อย")
    else:
        name = input("กรุณาตั้งชื่อสัตว์เลี้ยงของคุณ: ").strip() or "Buddy"
        pet = Pet(name=name)
        save_pet_data(pet)
        print(f"\nสร้างสัตว์เลี้ยงใหม่ชื่อ {pet.name} เรียบร้อย!")

    while True:
        CLIHandler.display_status(pet)
        cmd = CLIHandler.get_command_input()

        if cmd in ["quit", "exit"]:
            save_pet_data(pet)
            print(f"\nบันทึกข้อมูลเรียบร้อย ลาก่อนจาก {pet.name}! 👋")
            sys.exit(0)
        elif cmd == "feed":
            print(f"\n> {pet.feed()}")
        elif cmd == "play":
            print(f"\n> {pet.play()}")
        elif cmd == "sleep":
            print(f"\n> {pet.sleep()}")
        elif cmd == "fact":
            print(f"\n> {pet.interact_api()}")
        elif cmd == "save":
            if save_pet_data(pet):
                print("\n> บันทึกสถานะสัตว์เลี้ยงสำเร็จ!")
        else:
            print("\n[คำสั่งไม่ถูกต้อง] กรุณาพิมพ์: feed, play, sleep, fact, save หรือ quit")


if __name__ == "__main__":
    main()