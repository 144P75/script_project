# Changelog

บันทึกการเปลี่ยนแปลงที่สำคัญของโปรเจกต์ Virtual Pet Companion เรียงจากใหม่ล่าสุดไปเก่าสุด
รูปแบบเลขเวอร์ชัน `MAJOR.MINOR.PATCH` — MINOR เพิ่มเมื่อมีฟีเจอร์ใหม่ (1 Sprint = 1 MINOR),
PATCH เพิ่มเมื่อเป็นการแก้บั๊กหรือเก็บงานโดยไม่มีฟีเจอร์ใหม่ และจะขึ้น 1.0.0 เมื่อส่งงาน Final ครบและผ่านการตรวจแล้ว

## [Unreleased] — Final Sprint (วางแผนไว้ ยังไม่เริ่ม)

รายละเอียดใน `sprints/sprint-final/REPORT.md`
- **0.4.0** (เป้าหมาย: ก่อนนำเสนอ 6-7/10/69) — AI Companion คำสั่ง `talk` ที่รู้สถานะของสัตว์เลี้ยง, CI รันหลายเวอร์ชัน Python และ flake8 แบบเต็ม, เทสต์ที่ mock AI
- **0.4.x** — แก้ไขตามที่พบระหว่างนำเสนอ
- **1.0.0** (เป้าหมาย: ส่งงาน 16/10/69) — เวอร์ชันส่งงานสุดท้าย เอกสารครบ ไม่มีฟีเจอร์ใหม่เพิ่มจาก 0.4.x

## [0.3.1] — Sprint 3 (patch) 

### Fixed
- กดลบหลายตัวพร้อมกันบนเว็บแล้วข้อมูลหาย เพราะแต่ละ request โหลดไฟล์เดิมแล้วเขียนทับกัน → ใส่ lock ใน `PetService`
- เว็บตอบ error บางกรณีเป็นหน้า HTML (เช่น path ที่ไม่มี) หน้าเว็บอ่านไม่ได้ → error handler ตอบ JSON ทุกกรณี
- ปุ่มเปลี่ยนชื่อและลบบนเว็บกดแล้วไม่ทำงานในเบราว์เซอร์ที่บล็อกกล่อง `prompt()`/`confirm()` (เช่น preview ใน VS Code) → เปลี่ยนเป็นแก้ชื่อในแถว และกด "ลบ" แล้วยืนยันอีกครั้ง

## [0.3.0] — Sprint 3 — 

### Added
- `src/service.py` — `PetService` จุดเดียวที่ CLI และเว็บเรียกใช้ (reload ก่อนทุกคำสั่ง, save ทันทีหลังเปลี่ยน)
- คำสั่ง CLI: `pets` (เรียงได้), `renamepet`, `removepet` (มียืนยัน), `help`
- `web/app.py` — REST API: `/api/pet`, `/api/pet/actions/<action>`, `/api/pets` (GET/POST), `/api/pets/<name>` (PUT/DELETE), `/api/pets/<name>/select`, `/api/history`, `/api/warning`
- `web/static/index.html` — หน้าเว็บเล่นเกม: ดูแลสัตว์เลี้ยง, CRUD, ค้นหา/กรอง/เรียงประวัติ, สถานะอัปเดตทุก 10 วินาที
- บันทึกการเพิ่ม/เปลี่ยนชื่อ/ลบ ลงประวัติ (`source = System`)
- `tests/test_service.py`, `tests/test_app.py` (รวม 58 เทสต์)

### Changed
- `src/main.py` เรียกผ่าน `PetService` และแยกแต่ละคำสั่งเป็นฟังก์ชัน
- `src/cli.py` แสดงแถบสถานะ ตาราง และเมนูเลือกด้วยหมายเลข
- `web/app.py` เปลี่ยนเป็น `create_app()`
- `/api/interact` (Dog/Cat แบบสุ่ม) รวมเข้ากับ `POST /api/pet/actions/fact`

## [0.2.1] — Sprint 2 (patch) 

### Fixed
- ระบบเซฟข้อมูลซ้อนกัน 2 ระบบ (`pet_state.json` จาก Sprint 1 กับ `pets.json`) → รวมให้เหลือ `PetManager`
- เทสต์เรียกฟังก์ชันที่ชื่อไม่ตรงกับโค้ด ทำให้ CI ไม่ผ่าน
- decay ไม่เกิดเมื่อกดคำสั่งถี่กว่า 10 วินาที เพราะปัดเศษวินาทีทิ้ง
- ไฟล์ backup ถูกเขียนพร้อมไฟล์หลักจึงเหมือนกันทุกครั้ง กู้คืนไม่ได้จริง → backup เก็บเวอร์ชันก่อนหน้า
- ข้อความ "ความหิวยานลง" → "ความหิวลดลง"
- `flask` ไม่อยู่ใน `requirements.txt`

### Removed
- `src/interaction.py` (Dog API) ที่ไม่ได้ถูกเรียกใช้ และ `tests/test_interaction.py`

## [0.2.0] — Sprint 2 — 

### Added
- `src/pet_manager.py` — `PetManager` จัดการสัตว์เลี้ยงหลายตัว: เพิ่ม, สลับ, เปลี่ยนชื่อ, ลบ, แสดงรายการพร้อมเรียงตามชื่อ/หิว/พลังงาน/ความสุข
- ตรวจสอบชื่อสัตว์เลี้ยง (ห้ามว่าง, ยาวไม่เกิน 20, ห้ามอักขระพิเศษ, ห้ามซ้ำแบบไม่สนตัวพิมพ์)
- `src/exceptions.py` — Custom Exceptions (`PetNotFoundError`, `DuplicatePetError`, `InvalidPetNameError`, `InvalidActionError`, `NoActivePetError`)
- `src/storage.py` — `JsonStore` เขียนไฟล์แบบ atomic, กู้คืนจาก backup เมื่อไฟล์หาย/เสีย, เก็บไฟล์ที่เสียเป็น `.corrupt`
- `src/history.py` — `InteractionHistory` บันทึกประวัติพร้อมชื่อสัตว์เลี้ยง, ค้นหาหลายฟิลด์, กรองตาม source/kind/pet/ช่วงเวลา, เรียงลำดับหลายคีย์ (เช่น `kind,timestamp`)
- `web/app.py` — Flask API เบื้องต้น (`/api/interact`, `/api/history`)
- เมนูย่อย `history` ใน CLI: ดูล่าสุด / ค้นหา / กรอง / เรียงหลายคีย์
- `scripts/benchmark.py` วัดความเร็ว search/filter/sort กับข้อมูล 1,000 รายการ
- เทสต์: `tests/test_pet.py`, `tests/test_pet_manager.py`, `tests/test_history.py` (39 เทสต์ ไม่เรียกอินเทอร์เน็ตจริง)

### Changed
- `pets.json` เป็น schema v2 (`version`, `active`, `pets`) จำตัวที่เลี้ยงล่าสุดได้ และยังอ่านไฟล์รูปแบบเดิมได้
- ย้าย `web/history.py` → `src/history.py` ให้ตรงกับ Layer
- `tests/test_cli.py` → `tests/test_pet.py` ให้ชื่อตรงกับสิ่งที่ทดสอบ
- Cat Facts API ใช้ข้อมูลสำรองเมื่อเชื่อมต่อไม่ได้

## [0.1.0] — Sprint 1 — 

### Added
- โครงสร้าง Modular เริ่มต้น: `src/cli.py`, `src/pet.py`, `src/main.py`
- Class หลักตามหลัก OOP: `Pet`, `MoodTracker`, `Interaction`
- CLI: welcome banner, เมนูหลัก, การแสดงสถานะสัตว์เลี้ยง
- Data persistence ผ่านไฟล์ `pet_state.json`
- Input validation (`.strip().lower()`) และ exception handling (`KeyboardInterrupt`, `EOFError`, `FileNotFoundError`)
- เชื่อมต่อ Cat Facts API สำหรับคำสั่ง `fact`
- `tests/test_cli.py` และ CI/CD เบื้องต้นด้วย GitHub Actions (`.github/workflows/ci.yml`)
