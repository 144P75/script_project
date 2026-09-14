# 🐾 Virtual Pet Companion (CLI Application)

ระบบจำลองสัตว์เลี้ยงเสมือนจริงบน Terminal/CLI พัฒนาด้วยภาษา Python ตามหลัก **Object-Oriented Programming (OOP)** และ **Modular Architecture** เพื่อรองรับการประมวลผลสถานะตามเวลาจริง (Time-based Decay), การเชื่อมต่อ External API และการทำงานร่วมกับ CI/CD Pipeline

---
## 🎯 วัตถุประสงค์ของโครงการ (Project Objectives)

1. **สร้างเกมเลี้ยงสัตว์เสมือนจริงบน CLI:** พัฒนาโปรแกรมดูแลสัตว์เลี้ยงที่โต้ตอบผ่าน Command Line มีระบบให้อาหาร เล่นด้วย และดูสถานะ
2. **ฝึกเขียนโปรแกรมด้วยแนวคิด OOP:** ฝึกแบ่งโครงสร้างโค้ดอย่างเป็นระบบด้วยภาษา Python ผ่าน Class หลัก เช่น `Pet`, `MoodTracker` และ `Interaction`
3. **ทำระบบเซฟข้อมูล (Data Persistence):** บันทึกและดึงสถานะสัตว์เลี้ยง (ค่าความหิว, พลังงาน, อารมณ์) จากไฟล์ `pet_state.json` ทำให้เล่นต่อจากเดิมได้
4. **ทำระบบสถิติลดลงตามเวลา (Decay Over Time):** คำนวณส่วนต่างของเวลาจริง เพื่อลดค่าพลังงานและความหิวของสัตว์เลี้ยงโดยอัตโนมัติเมื่อไม่ได้เปิดโปรแกรม
5. **ดึงข้อมูลสุ่มจาก API:** เชื่อมต่อ Dog API หรือ Cat Facts API เพื่อนำรูปภาพหรือข้อความน่ารู้มาแสดงเวลามีปฏิสัมพันธ์กับสัตว์เลี้ยง
6. **ทำระบบป้องกันโปรแกรมพัง (Input Validation):** ดักจับ Error และตรวจสอบอินพุตของผู้ใช้ เพื่อให้โปรแกรมทำงานได้ต่อเนื่องแม้ผู้ใช้จะกรอกข้อมูลผิด

---

## 🌟 คุณสมบัติเด่นของระบบ (Key Features)

* **Modular Architecture:** แยก Presentation Layer (`src/cli.py`) และ Business Logic (`src/pet.py`) ชัดเจน
* **OOP Design:** พัฒนาด้วย 3 คลาสหลัก ได้แก่ `Pet`, `MoodTracker` และ `Interaction`
* **Data Persistence:** บันทึกและดึงสถานะผ่านไฟล์ `pet_state.json`
* **Time-based Decay:** คำนวณความหิว พลังงาน และอารมณ์ลดลงตามเวลาจริง
* **API Integration:** ดึงข้อมูลสุ่มเกร็ดความรู้แมวจาก Cat Facts API
* **DevOps Ready:** มี CI/CD Pipeline ด้วย GitHub Actions (`pytest` & `flake8`)

---

## 🏗️ สถาปัตยกรรมระบบ (Architectural Scope)

โปรเจกต์นี้ถูกออกแบบโดยแบ่งหน้าที่การทำงานอย่างชัดเจน (Separation of Concerns) ออกเป็น 3 ชั้นหลัก:

1. **Presentation Layer (`src/cli.py`):** ส่วนจัดการ CLI, การแสดงผลหน้าจอ/เมนูหลัก และรับอินพุตพร้อมตรวจสอบความถูกต้อง (Input Validation & Sanitization)
2. **Business Logic Layer (`src/pet.py`):** ส่วนประมวลผลคำนวณสถานะสัตว์เลี้ยง (Hunger, Energy, Happiness), การคำนวณ Decay Over Time และการประเมินอารมณ์ (`MoodTracker`)
3. **Data Access Layer (`src/main.py` / `pet_state.json`):** ส่วนการอ่านและบันทึกข้อมูลสถานะลงในไฟล์ `pet_state.json` (Data Persistence)

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
virtual-pet-cli/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD Pipeline
├── src/
│   ├── __init__.py
│   ├── cli.py             # Presentation Layer (CLI & UI)
│   ├── pet.py             # Business Logic Layer (OOP Classes & API)
│   └── main.py            # Entry Point & Data Access Layer
├── tests/
│   ├── __init__.py
│   └── test_cli.py        # Automated Unit Tests
├── .gitignore             # Git Ignore File
├── ALL_SPRINTS.md         # สรุปผลการดำเนินงานและ QA Reports แต่ละ Sprint
├── pet_state.json         # ไฟล์บันทึกสถานะสัตว์เลี้ยง (Auto-generated)
├── README.md              # เอกสารอธิบายโปรเจกต์
└── requirements.txt       # Dependencies (requests, pytest, flake8)
```
---

## 🚀 การรันโปรแกรม (Execution)

1. **เปิด Terminal / Command Prompt** และเข้าสู่โฟลเดอร์ Root ของโปรเจกต์
2. **รันไฟล์ Main Script:**
   ```bash
   python -m src.main

---
## 👥 สมาชิกในทีม (Team Members)

| รหัสนักศึกษา | ชื่อ-นามสกุล |ชื่อเล่น |
| :---: | :--- |:--- |
| **673380594-9** | นางสาวพรีมภัทร ภาวัฒนวคุณ | พรีม |
| **673380596-5** | นางสาวพิชยา สิทธิพันธ์ | เชอร์ |
| **673380598-1** | นางสาวมุกดา บุญประจันทร์ | เอม |


