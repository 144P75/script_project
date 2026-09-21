# Sprint 1: Front-End App Dev & Foundation

**ช่วงเวลา:** สัปดาห์ที่ 12 (นำเสนอ: 15-16 ก.ย. 2569 | ส่งงาน: 18 ก.ย. 2569)
**จุดเน้น:** การออกแบบ UI/CLI, โครงสร้าง OOP (Pet, MoodTracker, Interaction), Data Persistence (JSON) และการทำ Input Validation

## บทบาทในทีม (Sprint นี้)
| สมาชิก | บทบาท | หน้าที่รับผิดชอบ |
|---|---|---|
| พรีม | Planner | วางแผนและออกแบบสถาปัตยกรรมระบบแบบ Modular (`src/pet.py`, `src/cli.py`, `src/main.py`), ออกแบบโครงสร้างคลาส OOP (`Pet`, `MoodTracker`, `Interaction`), ร่างลำดับการทำงาน (Control Flow) และสเปกของไฟล์บันทึกข้อมูล `pet_state.json` |
| เอม | Coder | พัฒนา Business Logic Layer ใน `src/pet.py` (ระบบสถานะ, คำนวณ Time-based Decay, Cat Facts API), พัฒนา Presentation Layer ใน `src/cli.py` (หน้าจอ CLI, Status Display), เขียนฟังก์ชันเชื่อมต่อระบบ Data Access Layer และ Loop ใน `src/main.py` |
| เชอร์ | Debugger / QA | ทำ Input Validation และ Sanitization (`.strip().lower()`) เพื่อจัดการอินพุตขยะ, ดักจับ Exception (`KeyboardInterrupt`, `EOFError`, `FileNotFoundError`) ป้องกันโปรแกรม Crash, พัฒนาชุดทดสอบ Unit Tests ใน `tests/test_cli.py` และตั้งค่า CI/CD Pipeline (`ci.yml`) |

## เป้าหมายและขอบเขต (Scope & DoD)
- [x] ออกแบบโครงสร้างระบบแบบ Modular (`src/cli.py`, `src/pet.py`, `src/main.py`)
- [x] พัฒนา Class ตามหลัก OOP: `Pet`, `MoodTracker` และ `Interaction`
- [x] แสดงแบนเนอร์ต้อนรับ เมนู และสถานะสัตว์เลี้ยงในระบบ CLI
- [x] รองรับการรับคำสั่งแบบไม่ไวต่อตัวพิมพ์เล็ก-ใหญ่ด้วย `.strip().lower()`
- [x] บันทึกและโหลดสถานะสัตว์เลี้ยงผ่านไฟล์ `pet_state.json`
- [x] จัดการ Exception (Invalid Input, KeyboardInterrupt, FileNotFoundError) เพื่อป้องกันไม่ให้โปรแกรม Crash
- [x] ตั้งค่า CI/CD Pipeline อัตโนมัติด้วย GitHub Actions, Pytest และ Flake8

รายละเอียดผลการทดสอบ: ดู `QA_TEST_LOG.md`
สรุปบทเรียน: ดู `RETROSPECTIVE.md`
