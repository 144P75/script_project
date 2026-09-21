# PLAN.md — Virtual Pet Companion (CLI)

เอกสารสถาปัตยกรรมรวมของโปรเจกต์ **Virtual Pet Companion (CLI)** — รายละเอียดการดำเนินงาน
ผลการทดสอบ และ retrospective ของแต่ละ Sprint อยู่ใน `sprints/sprintX/` แทน ไฟล์นี้เก็บเฉพาะ
ภาพรวมสถาปัตยกรรมที่ใช้ร่วมกันทุก Sprint

## สมาชิกในทีม (Team Members)
| รหัสนักศึกษา | ชื่อ-นามสกุล | ชื่อเล่น |
| :---: | :--- | :--- |
| 673380594-9 | นางสาวพรีมภัทร ภาวัฒนวคุณ | พรีม |
| 673380596-5 | นางสาวพิชยา สิทธิพันธ์ | เชอร์ |
| 673380598-1 | นางสาวมุกดา บุญประจันทร์ | เอม |

## ตารางบทบาทตาม Sprint
| Sprint | รายละเอียด |
|---|---|
| Sprint 1 | ดู `sprints/sprint1/REPORT.md` |
| Sprint 2 | ดู `sprints/sprint2/REPORT.md` |
| Sprint 3 | ดู `sprints/sprint3/REPORT.md` |
| Sprint Final | ดู `sprints/sprint-final/REPORT.md` |

## สถาปัตยกรรมระบบ (Architectural Scope)
แบ่งหน้าที่การทำงานอย่างชัดเจน (Separation of Concerns) เป็น 3 ชั้นหลัก:

1. **Presentation Layer** (`src/cli.py`) — จัดการ CLI, แสดงผลหน้าจอ/เมนูหลัก, รับอินพุตพร้อมตรวจสอบความถูกต้อง
2. **Business Logic Layer** (`src/pet.py`, `src/pet_manager.py`) — คำนวณสถานะสัตว์เลี้ยง (Hunger, Energy, Happiness), Time-based Decay, ประเมินอารมณ์ (`MoodTracker`), จัดการหลายสัตว์เลี้ยง (`PetManager`)
3. **Data Access Layer** (`web/history.py`, ไฟล์ `.json`) — อ่าน/บันทึกสถานะสัตว์เลี้ยงและประวัติการโต้ตอบ

## Class Diagram (สรุป)
```
Pet
 ├─ MoodTracker (hunger, energy, happiness, get_mood())
 └─ Interaction (fetch_cat_fact())

PetManager
 ├─ pets: dict[str, Pet]
 ├─ active_pet: Pet
 ├─ add_pet(name), switch_pet(name)
 └─ save_pets() / load_pets()  → pets.json (+ pets_backup.json)

history (web/history.py)
 ├─ add_entry(source, kind, content)
 ├─ search_history(data, query)
 ├─ filter_history(data, source, kind)
 └─ sort_history(data, order)
```

## โครงสร้างโปรเจกต์ (Project Structure)
```text
script_project/
├── .github/workflows/ci.yml
├── src/
│   ├── cli.py             # Presentation Layer
│   ├── pet.py              # Business Logic Layer (Pet, MoodTracker, Interaction)
│   ├── pet_manager.py       # Business Logic Layer (multi-pet)
│   └── main.py              # Entry point
├── web/
│   ├── app.py               # Flask API (Sprint 3 integration target)
│   └── history.py           # Data Access Layer (interaction log)
├── tests/
├── sprints/
│   ├── sprint1/
│   ├── sprint2/
│   ├── sprint3/
│   └── sprint-final/
├── PLAN.md                  # ภาพรวมสถาปัตยกรรม
├── README.md
└── requirements.txt
```

## การรันโปรแกรม (Execution)
```bash
python -m src.main
```
