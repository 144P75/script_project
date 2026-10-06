# 🐾 Virtual Pet Companion (CLI + Web Application)

ระบบจำลองสัตว์เลี้ยงเสมือนจริงที่เล่นได้ทั้งบน Terminal/CLI และหน้าเว็บ พัฒนาด้วยภาษา Python ตามหลัก **Object-Oriented Programming (OOP)** และ **Modular Architecture** รองรับการประมวลผลสถานะตามเวลาจริง (Time-based Decay), การจัดการสัตว์เลี้ยงหลายตัว, การเชื่อมต่อ External API และการทำงานร่วมกับ CI/CD Pipeline

> **สถานะปัจจุบัน:** v1.0.0 (ส่งงาน Final) · เว็บออนไลน์: https://virtual-pet-companion.onrender.com/ · รายละเอียดใน [`sprints/sprint-final/REPORT.md`](./sprints/sprint-final/REPORT.md)

---

## 🎯 วัตถุประสงค์ของโครงการ (Project Objectives)

1. **สร้างเกมเลี้ยงสัตว์เสมือนจริง:** พัฒนาโปรแกรมดูแลสัตว์เลี้ยงที่ให้อาหาร เล่นด้วย ให้นอน และดูสถานะได้ ทั้งผ่าน CLI และหน้าเว็บ
2. **ฝึกเขียนโปรแกรมด้วยแนวคิด OOP:** แบ่งโครงสร้างโค้ดอย่างเป็นระบบผ่าน Class หลัก เช่น `Pet`, `MoodTracker`, `PetManager` และ `PetService`
3. **ทำระบบเซฟข้อมูล (Data Persistence):** บันทึกและดึงสถานะสัตว์เลี้ยงจากไฟล์ `.json` พร้อมไฟล์สำรองและกู้คืนอัตโนมัติเมื่อไฟล์เสียหาย
4. **ทำระบบสถิติลดลงตามเวลา (Decay Over Time):** คำนวณจากเวลาจริง เพื่อปรับความหิว พลังงาน และความสุขโดยอัตโนมัติ แม้ไม่ได้เปิดโปรแกรม
5. **ประมวลผลข้อมูล:** ค้นหา กรอง และเรียงลำดับประวัติการโต้ตอบได้หลายคุณลักษณะ
6. **เชื่อม Front-End กับ Back-End (Full-Stack):** ให้ CLI และหน้าเว็บใช้ Business Logic และข้อมูลชุดเดียวกัน
7. **ดึงข้อมูลสุ่มจาก API:** เชื่อมต่อ Cat Facts API เพื่อนำเกร็ดความรู้มาแสดงเวลามีปฏิสัมพันธ์กับสัตว์เลี้ยง
8. **ทำระบบป้องกันโปรแกรมพัง:** ตรวจสอบอินพุตและจัดการข้อผิดพลาดด้วย Custom Exceptions เพื่อให้โปรแกรมทำงานต่อเนื่อง

---

## 🌟 คุณสมบัติเด่นของระบบ (Key Features)

* **Layered Architecture:** แยก Presentation, Service, Business Logic และ Data Access ชัดเจน
* **OOP Design:** คลาสหลัก ได้แก่ `Pet`, `MoodTracker`, `Interaction`, `PetManager`, `InteractionHistory`, `JsonStore` และ `PetService`
* **Multi-Pet Management (CRUD):** เพิ่ม ดู เปลี่ยนชื่อ ลบ และสลับสัตว์เลี้ยงได้ ทั้งใน CLI และหน้าเว็บ
* **Web UI:** หน้าเว็บเล่นเกมได้ครบทุกฟังก์ชัน ผ่าน Flask REST API
* **State Consistency:** CLI และเว็บเรียกผ่าน `PetService` จุดเดียว ข้อมูลตรงกันเสมอแม้เปิดพร้อมกัน
* **Data Persistence:** บันทึกอัตโนมัติลง `pets.json` แบบ atomic พร้อม `pets_backup.json` และกู้คืนเองเมื่อไฟล์หายหรือเสีย
* **Time-based Decay:** ความหิว พลังงาน และความสุขเปลี่ยนตามเวลาจริง
* **Interaction History:** บันทึกทุกการโต้ตอบ ค้นหา กรองตามแหล่งที่มา/ประเภท/สัตว์เลี้ยง และเรียงลำดับได้หลายคีย์
* **Custom Exceptions:** แจ้งข้อผิดพลาดเป็นระบบ เช่น `PetNotFoundError`, `DuplicatePetError` และแปลงเป็น HTTP status บนเว็บ
* **API Integration:** ดึงเกร็ดความรู้แมวจาก Cat Facts API พร้อมข้อมูลสำรองเมื่อออฟไลน์
* **DevOps Ready:** CI/CD Pipeline ด้วย GitHub Actions (`pytest` และ `flake8`)

---

## 🏗️ สถาปัตยกรรมระบบ (Architectural Scope)

โปรเจกต์นี้แบ่งหน้าที่การทำงานอย่างชัดเจน (Separation of Concerns) รายละเอียดสถาปัตยกรรม, Class Diagram, Data Schema และ API แบบเต็มอยู่ใน [`PLAN.md`](./PLAN.md)

1. **Presentation Layer** (`src/cli.py`, `src/main.py`, `web/app.py`, `web/static/index.html`): แสดงผลและรับอินพุตผ่าน CLI และหน้าเว็บ
2. **Service Layer** (`src/service.py`): `PetService` จุดเดียวที่ทั้ง CLI และเว็บเรียกใช้ โหลดข้อมูลล่าสุดก่อนทุกคำสั่ง บันทึกทันทีหลังเปลี่ยน และป้องกันการเขียนทับกัน
3. **Business Logic Layer** (`src/pet.py`, `src/pet_manager.py`, `src/history.py`, `src/exceptions.py`): คำนวณสถานะ, Decay, อารมณ์, จัดการสัตว์เลี้ยงหลายตัว และค้นหา/กรอง/เรียงประวัติ
4. **Data Access Layer** (`src/storage.py`, ไฟล์ `.json`): อ่าน/เขียนไฟล์อย่างปลอดภัย สำรองและกู้คืนข้อมูล

```text
      CLI (main.py, cli.py)            Web (app.py, index.html)
                     \                     /
                   PetService (service.py)
                  /           |            \
           pet.py      pet_manager.py     history.py
                              |               |
                     storage.py (JsonStore) → ไฟล์ JSON
```

---

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)

**ภาษา:** Python 3.10 ขึ้นไป

**ไลบรารีมาตรฐาน**
* `json`, `os`, `shutil` — อ่าน เขียน และสำรองไฟล์
* `threading` — ล็อกไม่ให้คำสั่งทำงานทับกัน
* `datetime`, `re` — จัดการเวลาและตรวจรูปแบบชื่อ

**ไลบรารีภายนอก** (ติดตั้งจาก `requirements.txt`)
* `Flask` — หน้าเว็บและ REST API
* `requests` — เรียก Cat Facts API
* `pytest` — ทดสอบอัตโนมัติ
* `flake8` — ตรวจรูปแบบโค้ดตาม PEP8

**Design Patterns**
* **Service Layer** — `PetService` เป็นทางเข้าเดียวของ CLI และเว็บ
* **Repository** — `JsonStore` แยกการอ่านเขียนไฟล์ออกจาก Business Logic
* **Decorator** — `@synchronized` ใส่ล็อกให้ทุกเมธอดของ `PetService`
* **Exception Hierarchy** — ข้อผิดพลาดทุกแบบสืบทอดจาก `PetError`
## 🧩 โครงสร้างโค้ด (Source Code)

```text
script_project/
├── .github/
│   └── workflows/
│       └── ci.yml                     GitHub Actions: flake8 + pytest อัตโนมัติทุก push/PR
│
├── src/                                Presentation (CLI) + Service + Business Logic + Data Access
│   ├── main.py                         Entry point ของ CLI — game loop และคำสั่งทั้งหมด
│   ├── cli.py                          Presentation Layer — แสดงสถานะ ตาราง เมนู และรับ input
│   ├── service.py                      Service Layer — PetService จุดเดียวที่ CLI และเว็บเรียกใช้
│   ├── pet.py                          Business Logic — Pet, MoodTracker, Interaction (Cat Facts API)
│   ├── pet_manager.py                  Business Logic — CRUD สัตว์เลี้ยงหลายตัว, ตรวจชื่อ, เรียงลำดับ
│   ├── history.py                      บันทึก/ค้นหา/กรอง/เรียงลำดับ ประวัติการโต้ตอบ
│   ├── exceptions.py                   Custom Exceptions
│   └── storage.py                      Data Access — JsonStore (atomic write, backup, recovery)
│
├── web/                                Presentation (Web)
│   ├── app.py                          Flask REST API
│   └── static/
│       └── index.html                  หน้าเว็บเกม
│
├── scripts/
│   └── benchmark.py                    วัดความเร็ว search/filter/sort กับข้อมูล 1,000 รายการ
│
├── tests/                              Automated Tests (58 เทสต์)
│   ├── test_pet.py                     ทดสอบ MoodTracker, Pet (decay, feed, play, sleep)
│   ├── test_pet_manager.py             ทดสอบ CRUD, ชื่อผิด/ซ้ำ, ไฟล์หาย/เสีย, backup
│   ├── test_history.py                 ทดสอบ search/filter/sort, ไฟล์ประวัติเสีย, ความเร็ว
│   ├── test_service.py                 ทดสอบ PetService, ข้อมูล CLI ↔ เว็บตรงกัน, request พร้อมกัน
│   └── test_app.py                     ทดสอบ Web API และ HTTP status ของ error
│
├── conftest.py                         Fixtures กลางของเทสต์ (ไฟล์ชั่วคราว, mock API)
├── setup.cfg                           ตั้งค่า flake8 และ pytest
├── requirements.txt                    Dependencies: pytest, flake8, requests, flask
└── .gitignore                          ไฟล์ที่ไม่ track: pets.json, interaction_history.json, __pycache__ ฯลฯ
```

---

## 📄 เอกสารประกอบโปรเจกต์ (Documentation)

```text
script_project/
├── README.md                          ไฟล์นี้ — ภาพรวมโปรเจกต์ วิธีติดตั้ง/รัน สมาชิกทีม
├── PLAN.md                            สถาปัตยกรรม, Class Diagram, Data Schema, API, DoD, ประวัติการ Refactor
├── CHANGELOG.md                       การเปลี่ยนแปลงแต่ละเวอร์ชัน
│
└── sprints/                           หลักฐานการทำงานแยกตามรอบ (ไม่มีโค้ด)
    ├── sprint1/
    │   ├── code/                      Source Code ของ Sprint 1
    │   ├── REPORT.md                  Scope, DoD, บทบาททีมของ Sprint
    │   ├── QA_TEST_LOG.md             ตารางผลทดสอบ (Observation/Expected/Actual)
    │   ├── RETROSPECTIVE.md           Wow! / Whoops!
    │   └── PEER_EVALUATION.md         คะแนนประเมิน self/peer ตามบทบาท
    │
    ├── sprint2/
    │   ├── code/                      Source Code ของ Sprint 2
    │   ├── REPORT.md
    │   ├── QA_TEST_LOG.md
    │   ├── RETROSPECTIVE.md
    │   └── PEER_EVALUATION.md
    │
    ├── sprint3/
    │   ├── code/                      Source Code ของ Sprint 3
    │   ├── REPORT.md
    │   ├── QA_TEST_LOG.md
    │   ├── RETROSPECTIVE.md
    │   └── PEER_EVALUATION.md
    │
    └── sprint-final/
        └── REPORT.md                  แผนงาน Final Sprint (ยังไม่เริ่ม)
```

> รายละเอียดผลงานแต่ละ Sprint อยู่ในโฟลเดอร์ [`sprints/`](./sprints)

---

## 🚀 การรันโปรแกรม (Execution)
   ต้องใช้ Python 3.10 ขึ้นไป
1. **เปิด Terminal / Command Prompt** และเข้าสู่โฟลเดอร์ Root ของโปรเจกต์
2. **ติดตั้ง Dependencies:**
```bash
   pip install -r requirements.txt
```
3. **เล่นผ่าน CLI:**
```bash
   python -m src.main
```
   พิมพ์ `help` เพื่อดูคำสั่งทั้งหมด: `feed` `play` `sleep` `fact` `pets` `addpet` `switchpet` `renamepet` `removepet` `talk` `history` `quit`
4. **เล่นผ่านหน้าเว็บ:**
```bash
   python -m web.app
```
   แล้วเปิด http://127.0.0.1:5000 (ต้องเปิดผ่านลิงก์นี้ ห้ามดับเบิลคลิกเปิดไฟล์ `index.html` ตรงๆ)

   เปิด CLI และเว็บพร้อมกันได้ ทั้งสองใช้ข้อมูลชุดเดียวกัน

5. **เปิด AI Companion (ไม่บังคับ):** copy `.env.example` แล้วเปลี่ยนชื่อเป็น `.env` จากนั้นใส่ key ของเจ้าใดเจ้าหนึ่ง เช่น `GEMINI_API_KEY=xxxx` เกมจะอ่านไฟล์นี้เองทุกครั้งที่เปิด ถ้าไม่ใส่ `talk` จะตอบแบบออฟไลน์ตามอารมณ์

   | AI | ตัวแปรใน `.env` | สร้าง key ที่ |
   |---|---|---|
   | Gemini (มีโควตาฟรี) | `GEMINI_API_KEY` | aistudio.google.com |
   | ChatGPT | `OPENAI_API_KEY` | platform.openai.com |
   | Claude | `ANTHROPIC_API_KEY` | platform.claude.com |

   ถ้าใส่หลาย key เลือกเองได้ด้วย `AI_PROVIDER=gemini` (หรือ `openai`, `claude`) — ไฟล์ `.env` ไม่ถูก commit ขึ้น GitHub

6. **ทดสอบระบบ:**
```bash
   python -m pytest -v            # รันเทสต์ทั้งหมด (ไม่ต้องใช้อินเทอร์เน็ตหรือ API key)
   flake8 .                       # ตรวจรูปแบบโค้ด
   python -m scripts.benchmark    # วัดความเร็ว search/filter/sort
```

### ☁️ Deploy ออนไลน์ (Render)
ตั้งค่าไว้ใน `render.yaml` — บน Render เลือก **New → Blueprint** แล้วเลือก repo นี้ จากนั้นใส่ `GEMINI_API_KEY` ในหน้า Render
- รันด้วย `gunicorn` **1 worker** หลาย thread เพราะ lock ใน `PetService` ทำงานภายใน process เดียว
- แผนฟรี: server หลับเมื่อไม่มีคนใช้ (เปิดครั้งแรกช้า) และไม่เก็บไฟล์ถาวร ข้อมูลสัตว์เลี้ยงหายเมื่อ deploy ใหม่หรือ restart
- เปิดโหมดหลายผู้เล่น (`MULTI_PLAYER=1`): แต่ละเบราว์เซอร์มีสัตว์เลี้ยงของตัวเอง เปลี่ยนเบราว์เซอร์หรือล้างข้อมูลเบราว์เซอร์ = เริ่มใหม่
- ทุกคนใช้โควตา AI ของเจ้าของ key — รันในเครื่องปกติ (ไม่ตั้ง `MULTI_PLAYER`) เว็บใช้ข้อมูลชุดเดียวกับ CLI เหมือนเดิม

---

## 👥 สมาชิกในทีม (Team Members)

| รหัสนักศึกษา | ชื่อ-นามสกุล | ชื่อเล่น |
| :---: | :--- | :--- |
| **673380594-9** | นางสาวพรีมภัทร ภาวัฒนวคุณ | พรีม |
| **673380596-5** | นางสาวพิชยา สิทธิพันธ์ | เชอร์ |
| **673380598-1** | นางสาวมุกดา บุญประจันทร์ | เอม |
