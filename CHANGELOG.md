# Changelog

บันทึกการเปลี่ยนแปลงที่สำคัญของโปรเจกต์ Virtual Pet Companion (CLI) เรียงจากใหม่ล่าสุดไปเก่าสุด

## [Unreleased] — Sprint 3 & Final Sprint

วางแผนไว้ใน `PLAN.md` ยังไม่เริ่มดำเนินการ:
- Sprint 3 (กำหนดส่ง 2/10/69, จะขึ้นเป็น v0.3.0): เชื่อมหน้าเว็บ pixel-pet เข้ากับ `web/app.py` จริง, เพิ่ม endpoint feed/play/sleep, state sync ระหว่าง CLI กับไฟล์ข้อมูล, ทดสอบ edge case เพิ่มเติม
- Final Sprint (กำหนดส่ง 16/10/69, จะขึ้นเป็น v1.0.0): CI/CD เขียวเต็มรูปแบบ, คำสั่ง `talk` (AI Companion Chat), รวมระบบ persistence ให้เหลือระบบเดียว, แก้ automated tests ที่ยังไม่ผ่าน

## [0.2.0] — Sprint 2 — 20/9/69 | กำหนดส่งจริง 25/9/69

### Added
- `src/pet_manager.py` — `PetManager` จัดการสัตว์เลี้ยงหลายตัว บันทึกลง `pets.json` พร้อมไฟล์สำรอง `pets_backup.json`
- `web/history.py` — บันทึกประวัติการโต้ตอบ พร้อม `search_history`, `filter_history`, `sort_history`
- `web/app.py` — Flask API เบื้องต้น (`/api/interact`, `/api/history`) เตรียมไว้สำหรับ Sprint 3
- เมนูย่อย `history` ใน `src/main.py` — ดูล่าสุด / ค้นหาด้วยคำค้นหา / กรองตามแหล่งที่มา-ประเภทกิจกรรม / เรียงลำดับเวลา
- `src/interaction.py` — เพิ่ม Dog API เป็นแหล่งข้อมูลเสริม (ยังไม่ได้เชื่อมเข้ากับ `main.py`)
- `tests/test_pet_manager.py`, `tests/test_history.py`, `tests/test_interaction.py`

### Verified
- ทดสอบดึง Cat Facts API จริงบนเครื่องที่มีอินเทอร์เน็ต (นอก sandbox พัฒนา) — ได้ข้อความเกร็ดความรู้จริงและบันทึกลง `interaction_history.json` ถูกต้อง

### Known issues (อยู่ระหว่างแก้ไข — จะปิดในรอบ cleanup ถัดไปก่อนเริ่ม Sprint 3)
- ระบบเซฟข้อมูลซ้อนกัน 2 ระบบ (`pet_state.json` จาก Sprint 1 กับ `pets.json` ของ `PetManager`) ยังไม่ได้รวมเป็นระบบเดียว
- `tests/test_history.py` และ `tests/test_pet_manager.py` เรียกฟังก์ชัน/เมธอดที่ชื่อไม่ตรงกับโค้ดจริง ทำให้ CI ยังไม่ผ่าน
- `src/interaction.py` เป็นโค้ดที่ไม่ได้ถูกเรียกใช้งานจริง — จะลบออกในรอบ cleanup

## [0.1.0] — Sprint 1 — 15/9/69 | ส่งจริง 18/9/69

### Added
- โครงสร้าง Modular เริ่มต้น: `src/cli.py`, `src/pet.py`, `src/main.py`
- Class หลักตามหลัก OOP: `Pet`, `MoodTracker`, `Interaction`
- CLI: welcome banner, เมนูหลัก, การแสดงสถานะสัตว์เลี้ยง
- Data persistence ผ่านไฟล์ `pet_state.json`
- Input validation (`.strip().lower()`) และ exception handling (`KeyboardInterrupt`, `EOFError`, `FileNotFoundError`)
- เชื่อมต่อ Cat Facts API สำหรับคำสั่ง `fact`
- `tests/test_cli.py` และ CI/CD เบื้องต้นด้วย GitHub Actions (`.github/workflows/ci.yml`)
