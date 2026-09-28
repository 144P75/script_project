# Sprint 3: Full-Stack App Dev

**ช่วงเวลา:** สัปดาห์ที่ 14 (นำเสนอ: 29-30 ก.ย. 2569 รวมกับ Sprint 2)
**จุดเน้น:** เชื่อม Front-End (CLI + Web) เข้ากับ Back-End จาก Sprint 2, State Management, Data Consistency และ Edge Cases

## บทบาทในทีม (Sprint นี้)
| สมาชิก | บทบาท | หน้าที่รับผิดชอบ |
|---|---|---|
| เชอร์ | Planner / Architect | กำหนดข้อกำหนด Integration และ End-to-End DoD ใน `PLAN.md`, ออกแบบ Service Layer และ REST API, ประสานงาน Live Demo |
| พรีม | Coder | พัฒนา `src/service.py`, คำสั่ง CLI ใหม่ (`pets`, `renamepet`, `removepet`, `help`), Flask API และหน้าเว็บ |
| เอม | Debugger / QA | ทดสอบ Edge Cases แบบ End-to-End (CLI ↔ เว็บ, request พร้อมกัน, input ผิด), เขียน `test_service.py`, `test_app.py`, รีวิว PR, จัดทำ QA Test Log |

## เป้าหมายและขอบเขต (Scope)
- [x] Service Layer (`PetService`) เป็นจุดเดียวที่ CLI และเว็บเรียกใช้ Business Logic
- [x] CLI เรียก CRUD ได้ครบ: `addpet`, `pets`, `renamepet`, `removepet`, `switchpet`
- [x] หน้าเว็บเล่นเกมได้ครบทุกฟังก์ชันเหมือน CLI (ดูแลสัตว์เลี้ยง, CRUD, ค้นหา/กรอง/เรียงประวัติ)
- [x] REST API ที่แปลง Custom Exceptions เป็น HTTP status (400/404/409) และตอบ error เป็น JSON เสมอ
- [x] State Management: reload ก่อนทุกคำสั่ง, save ทันทีหลังเปลี่ยน, lock กันหลาย request เขียนทับกัน
- [x] บันทึกการเพิ่ม/เปลี่ยนชื่อ/ลบ ลงประวัติ (`source = System`)
- [x] CLI แสดงสถานะเป็นแถบ และแสดงประวัติ/รายชื่อเป็นตาราง

## ขอบเขตงานส่วนโค้ด
| ไฟล์ | Layer | สิ่งที่ทำ |
|---|---|---|
| `src/service.py` | Service | `PetService`: สถานะ, action, CRUD, ประวัติ + lock |
| `src/main.py` | Presentation | เรียกผ่าน `PetService`, แยกคำสั่งเป็นฟังก์ชัน, จัดการ exception ที่เดียว |
| `src/cli.py` | Presentation | แถบสถานะ, ตาราง, เมนูเลือกด้วยหมายเลข, คำสั่ง `help` |
| `web/app.py` | Presentation (Web) | REST API (`create_app`) + error handler |
| `web/static/index.html` | Presentation (Web) | หน้าเว็บเกม |
| `tests/test_service.py`, `tests/test_app.py` | Test | Integration + API tests |

## Definition of Done
- [x] CLI และเว็บเรียก CRUD ได้ครบ และข้อมูลตรงกันทันที (`test_cli_and_web_stay_in_sync`)
- [x] ทุก error จากเว็บตอบเป็น JSON พร้อม status ที่ถูกต้อง รวมทั้ง path ที่ไม่มี (404) และ body ที่ไม่ใช่ JSON (400)
- [x] ลบตัวสุดท้ายแล้ว CLI ถามชื่อตัวใหม่ และเว็บปิดปุ่มพร้อมบอกให้เพิ่มสัตว์เลี้ยง
- [x] หลาย request พร้อมกันไม่ทำให้ข้อมูลหาย
- [x] Ctrl+C / Ctrl+D ใน CLI ออกได้โดยข้อมูลไม่หาย

## ผลการทดสอบ
- Automated: pytest ผ่าน 58/58 เทสต์, flake8 ไม่มี warning
- Manual / End-to-End: ดู `QA_TEST_LOG.md`
- สรุปบทเรียน: ดู `RETROSPECTIVE.md`
