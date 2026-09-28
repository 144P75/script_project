# Sprint 2: Back-End App Dev

**ช่วงเวลา:** สัปดาห์ที่ 13 (นำเสนอ: 29-30 ก.ย. 2569 | ส่งงาน: 2 ต.ค. 2569 — เลื่อนจากเดิม 25 ก.ย. ส่งรวมกับ Sprint 3)
**จุดเน้น:** การขยายขีดความสามารถ Business Logic Layer, ระบบจัดเก็บข้อมูลขั้นสูง และการประมวลผลข้อมูล

## บทบาทในทีม (Sprint นี้)
| สมาชิก | บทบาท | หน้าที่รับผิดชอบ |
|---|---|---|
| พรีม | Debugger / QA | *ทดสอบ Multi-Pet, JSON Persistence, switchpet, Interaction History และ Auto-Save & Backup ตรวจสอบ Edge Cases และ Exception Handling พร้อมจัดทำ QA Test Log และตรวจสอบความเสถียรของระบบใน CLI Loop* |
| เอม | Planner | *วางแผนและออกแบบสถาปัตยกรรมระบบ Multi-Pet และ Data Persistence กำหนดโครงสร้าง PetManager และรูปแบบข้อมูล JSON (to_dict() / from_dict()), ออกแบบระบบ Interaction History และกำหนด Definition of Done (DoD)* |
| เชอร์ | Coder | *พัฒนา Business Logic และ Data Access ใน src/pet_manager.py สำหรับจัดการสัตว์เลี้ยงหลายตัว (active_pet), โหลด/บันทึกข้อมูล JSON, ระบบ Auto-Save & Backup และพัฒนาการค้นหา กรอง และเรียงลำดับข้อมูล Interaction History ใน web/history.py* |

## เป้าหมายและขอบเขต (Scope)
- [x] จัดการสัตว์เลี้ยงหลายตัว (Multi-Pet Management) พร้อม CRUD ใน Business Logic: เพิ่ม, สลับ, เปลี่ยนชื่อ, ลบ, แสดงรายการ
- [x] Custom Exceptions สำหรับทุกกรณีผิดพลาดของ Business Logic
- [x] Data Access Layer ที่ทนทาน: atomic write, backup เวอร์ชันก่อนหน้า, กู้คืนอัตโนมัติ
- [x] Data Persistence ด้วย JSON (schema v2 จำตัวที่เลี้ยงล่าสุด และอ่านรูปแบบเดิมได้)
- [x] Interaction History: ค้นหาหลายฟิลด์, กรองตามหลายคุณลักษณะ, เรียงลำดับหลายคีย์
- [x] Flask API เบื้องต้น (`/api/interact`, `/api/history`) เตรียมไว้สำหรับ Sprint 3

### ขอบเขตงานส่วนโค้ด
| ไฟล์ | Layer | สิ่งที่ทำ |
|---|---|---|
| `src/pet_manager.py` | Business Logic | CRUD สัตว์เลี้ยง, ตรวจชื่อ, เรียงลำดับ, schema v2 |
| `src/exceptions.py` | Business Logic | Custom Exceptions |
| `src/pet.py` | Business Logic | แก้บั๊ก decay, ปรับค่าสถานะผ่าน `change()`, Cat Facts สำรอง |
| `src/history.py` | Business Logic + Data | บันทึก/ค้นหา/กรอง/เรียงประวัติ (ย้ายจาก `web/history.py`) |
| `src/storage.py` | Data Access | `JsonStore` อ่าน/เขียน JSON อย่างปลอดภัย |
| `src/main.py` | Presentation | ใช้ `PetManager`/`InteractionHistory` ใหม่ และแสดง error จาก exception |
| `web/app.py` | Presentation (Web) | Flask API เบื้องต้น |
| `scripts/benchmark.py` | เครื่องมือ | วัดความเร็วอัลกอริทึม |
| `tests/` | Test | `test_pet.py`, `test_pet_manager.py`, `test_history.py` |

## Definition of Done (DoD)
- โหลดข้อมูลสัตว์เลี้ยงจาก JSON ได้ และแสดงสถานะ (Hunger, Energy, Happiness) พร้อมอารมณ์
- `switchpet` / ลบ / เปลี่ยนชื่อ ชื่อที่ไม่มีอยู่ → `PetNotFoundError` แจ้งผู้ใช้โดยโปรแกรมไม่พัง
- ชื่อว่าง, ยาวเกิน, มีอักขระพิเศษ → `InvalidPetNameError` · ชื่อซ้ำ (ไม่สนตัวพิมพ์) → `DuplicatePetError`
- ไฟล์หาย → เริ่มใหม่ · ไฟล์เสีย → กู้จาก backup แจ้งผู้ใช้ และซ่อมไฟล์หลัก · ข้อมูลบางตัวเสีย → ข้ามตัวนั้นและแจ้งเตือน
- ทุก Interaction (`feed`, `play`, `sleep`, `fact`) ถูกบันทึกพร้อมชื่อสัตว์เลี้ยง และค้นหา/กรอง/เรียงได้
- ค้นหาคำว่างคืนทั้งหมด · เรียงด้วยคีย์ที่ไม่รองรับ → แจ้งตัวเลือกที่ใช้ได้
- ค้นหา + กรอง + เรียง ข้อมูล 1,000 รายการเสร็จภายใน 50 ms
- ระบบทำงานต่อเนื่องใน loop โดยไม่ crash

---
ผลการทดสอบอัตโนมัติ: pytest ผ่าน 39/39 เทสต์, flake8 ไม่มี warning

รายละเอียดผลการทดสอบ: ดู `QA_TEST_LOG.md`
สรุปบทเรียน: ดู `RETROSPECTIVE.md`
