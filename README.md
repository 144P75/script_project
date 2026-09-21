# 🐾 Virtual Pet Companion (CLI Application)

ระบบจำลองสัตว์เลี้ยงเสมือนจริงบน Terminal/CLI พัฒนาด้วยภาษา Python ตามหลัก **Object-Oriented Programming (OOP)** และ **Modular Architecture** เพื่อรองรับการประมวลผลสถานะตามเวลาจริง (Time-based Decay), การเชื่อมต่อ External API และการทำงานร่วมกับ CI/CD Pipeline

---

## 🎯 วัตถุประสงค์ของโครงการ (Project Objectives)

1. **สร้างเกมเลี้ยงสัตว์เสมือนจริงบน CLI:** พัฒนาโปรแกรมดูแลสัตว์เลี้ยงที่โต้ตอบผ่าน Command Line มีระบบให้อาหาร เล่นด้วย และดูสถานะ
2. **ฝึกเขียนโปรแกรมด้วยแนวคิด OOP:** ฝึกแบ่งโครงสร้างโค้ดอย่างเป็นระบบด้วยภาษา Python ผ่าน Class หลัก เช่น `Pet`, `MoodTracker` และ `Interaction`
3. **ทำระบบเซฟข้อมูล (Data Persistence):** บันทึกและดึงสถานะสัตว์เลี้ยง (ค่าความหิว, พลังงาน, ความสุข) จากไฟล์ `.json` ทำให้เล่นต่อจากเดิมได้
4. **ทำระบบสถิติลดลงตามเวลา (Decay Over Time):** คำนวณส่วนต่างของเวลาจริง เพื่อลดค่าพลังงานและความหิวของสัตว์เลี้ยงโดยอัตโนมัติเมื่อไม่ได้เปิดโปรแกรม
5. **ดึงข้อมูลสุ่มจาก API:** เชื่อมต่อ Cat Facts API เพื่อนำเกร็ดความรู้มาแสดงเวลามีปฏิสัมพันธ์กับสัตว์เลี้ยง
6. **ทำระบบป้องกันโปรแกรมพัง (Input Validation):** ดักจับ Error และตรวจสอบอินพุตของผู้ใช้ เพื่อให้โปรแกรมทำงานได้ต่อเนื่องแม้ผู้ใช้จะกรอกข้อมูลผิด

---

## 🌟 คุณสมบัติเด่นของระบบ (Key Features)

* **Modular Architecture:** แยก Presentation Layer (`src/cli.py`), Business Logic (`src/pet.py`, `src/pet_manager.py`) และ Data Access (`web/history.py`) ชัดเจน
* **OOP Design:** พัฒนาด้วยคลาสหลัก ได้แก่ `Pet`, `MoodTracker`, `Interaction` และ `PetManager`
* **Multi-Pet Management:** จัดการสัตว์เลี้ยงได้หลายตัว สลับใช้งานได้ผ่านคำสั่ง `addpet` / `switchpet`
* **Data Persistence:** บันทึกและดึงสถานะผ่านไฟล์ `pets.json` พร้อมไฟล์สำรอง `pets_backup.json`
* **Time-based Decay:** คำนวณความหิว พลังงาน และความสุขลดลงตามเวลาจริง
* **Interaction History:** บันทึกประวัติการโต้ตอบทุกครั้ง พร้อมค้นหา กรอง และเรียงลำดับได้ (คำสั่ง `history`)
* **API Integration:** ดึงข้อมูลสุ่มเกร็ดความรู้แมวจาก Cat Facts API
* **DevOps Ready:** มี CI/CD Pipeline ด้วย GitHub Actions (`pytest` และ `flake8`)

---

## 🏗️ สถาปัตยกรรมระบบ (Architectural Scope)

โปรเจกต์นี้ถูกออกแบบโดยแบ่งหน้าที่การทำงานอย่างชัดเจน (Separation of Concerns) ออกเป็น 3 ชั้นหลัก — รายละเอียดสถาปัตยกรรมและ Class Diagram แบบเต็มอยู่ใน [`PLAN.md`](./PLAN.md):

1. **Presentation Layer** (`src/cli.py`) — จัดการ CLI, การแสดงผลหน้าจอ/เมนูหลัก และรับอินพุตพร้อมตรวจสอบความถูกต้อง (Input Validation)
2. **Business Logic Layer** (`src/pet.py`, `src/pet_manager.py`) — คำนวณสถานะสัตว์เลี้ยง (Hunger, Energy, Happiness), การคำนวณ Decay Over Time, การประเมินอารมณ์ (`MoodTracker`) และการจัดการสัตว์เลี้ยงหลายตัว
3. **Data Access Layer** (`web/history.py`, ไฟล์ `.json`) — การอ่านและบันทึกข้อมูลสถานะสัตว์เลี้ยงและประวัติการโต้ตอบ

---

## 🧩 โครงสร้างโค้ด (Source Code)

```text
script_project/
├── .github/
│   └── workflows/
│       └── ci.yml                     GitHub Actions: flake8 + pytest อัตโนมัติทุก push/PR
│
├── src/                                Presentation + Business Logic Layer
│   ├── main.py                         Entry point — game loop, เมนูคำสั่งหลัก
│   ├── cli.py                          Presentation Layer — แสดงผล UI, รับ input
│   ├── pet.py                          Business Logic — Pet, MoodTracker, Interaction (Cat Facts API)
│   └── pet_manager.py                  Business Logic — จัดการสัตว์เลี้ยงหลายตัว, save/load + backup
│
├── web/                                Data Access + Web API Layer
│   ├── history.py                      บันทึก/ค้นหา/กรอง/เรียงลำดับ ประวัติการโต้ตอบ (JSON)
│   └── app.py                          Flask API (`/api/interact`, `/api/history`) — เตรียมไว้สำหรับ Sprint 3
│
├── tests/                              Automated Unit Tests
│   ├── test_cli.py                     ทดสอบ MoodTracker, Pet (decay, feed)
│   ├── test_history.py                 ทดสอบ search/filter/sort ของ web/history.py
│   └── test_pet_manager.py             ทดสอบ PetManager (save/load, backup)
│
├── requirements.txt                    Dependencies: pytest, flake8, requests, flask
└── .gitignore                          ไฟล์ที่ไม่ track: pets.json, pets_backup.json, __pycache__ ฯลฯ
```

---

## 📄 เอกสารประกอบโปรเจกต์ (Documentation)

```text
script_project/
├── README.md                          ไฟล์นี้ — ภาพรวมโปรเจกต์ วิธีติดตั้ง/รัน สมาชิกทีม
├── PLAN.md                            สถาปัตยกรรมรวม + Class Diagram (ใช้ร่วมทุก Sprint)
│
└── sprints/                           หลักฐานการทำงานแยกตามรอบ (ไม่มีโค้ด)
    ├── sprint1/
    │   ├── REPORT.md                  Scope, DoD, บทบาททีมของ Sprint 1
    │   ├── QA_TEST_LOG.md             ตารางผลทดสอบ (Observation/Expected/Actual)
    │   ├── RETROSPECTIVE.md           Wow! / Whoops!
    │   └── PEER_EVALUATION.md         คะแนนประเมิน self/peer ตามบทบาท
    │
    ├── sprint2/
    │   ├── REPORT.md
    │   ├── QA_TEST_LOG.md
    │   ├── RETROSPECTIVE.md
    │   └── PEER_EVALUATION.md
    └── sprint3/
        ├── REPORT.md
        ├── QA_TEST_LOG.md
        ├── RETROSPECTIVE.md
        └── PEER_EVALUATION.md
```

> รายละเอียดผลงานแต่ละ Sprint อยู่ในโฟลเดอร์ [`sprints/`](./sprints)

---

## 🚀 การรันโปรแกรม (Execution)

1. **เปิด Terminal / Command Prompt** และเข้าสู่โฟลเดอร์ Root ของโปรเจกต์
2. **ติดตั้ง Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **รันไฟล์ Main Script:**
   ```bash
   python -m src.main
   ```

---

## 👥 สมาชิกในทีม (Team Members)

| รหัสนักศึกษา | ชื่อ-นามสกุล | ชื่อเล่น |
| :---: | :--- | :--- |
| **673380594-9** | นางสาวพรีมภัทร ภาวัฒนวคุณ | พรีม |
| **673380596-5** | นางสาวพิชยา สิทธิพันธ์ | เชอร์ |
| **673380598-1** | นางสาวมุกดา บุญประจันทร์ | เอม |