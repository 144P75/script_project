# Sprint 2: Back-End App Dev

**ช่วงเวลา:** สัปดาห์ที่ 13 (นำเสนอ: 22-23 ก.ย. 2569 | ส่งงาน: 25 ก.ย. 2569)
**จุดเน้น:** การขยายขีดความสามารถ Business Logic Layer, ระบบจัดเก็บข้อมูลขั้นสูง และการประมวลผลข้อมูล

## บทบาทในทีม (Sprint นี้)
| สมาชิก | บทบาท | หน้าที่รับผิดชอบ |
|---|---|---|
| พรีม | Debugger / QA | *ทดสอบ Multi-Pet, JSON Persistence, switchpet, Interaction History และ Auto-Save & Backup ตรวจสอบ Edge Cases และ Exception Handling พร้อมจัดทำ QA Test Log และตรวจสอบความเสถียรของระบบใน CLI Loop* |
| เอม | Planner | *วางแผนและออกแบบสถาปัตยกรรมระบบ Multi-Pet และ Data Persistence กำหนดโครงสร้าง PetManager และรูปแบบข้อมูล JSON (to_dict() / from_dict()), ออกแบบระบบ Interaction History และกำหนด Definition of Done (DoD)* |
| เชอร์ | Coder | *พัฒนา Business Logic และ Data Access ใน src/pet_manager.py สำหรับจัดการสัตว์เลี้ยงหลายตัว (active_pet), โหลด/บันทึกข้อมูล JSON, ระบบ Auto-Save & Backup และพัฒนาการค้นหา กรอง และเรียงลำดับข้อมูล Interaction History ใน web/history.py* |

## เป้าหมายและขอบเขต (Scope & DoD)
- [ ] เพิ่มความสามารถในการจัดการสัตว์เลี้ยงหลายตัว (Multi-Pet Management)
- [ ] พัฒนาระบบ Interaction History (ระบบค้นหา กรองข้อมูล และเรียงลำดับประวัติการโต้ตอบของสัตว์เลี้ยง)
- [ ] ปรับปรุง Data Access Layer ให้รองรับการสำรองข้อมูล (Backup & Auto-Save)
- [ ] ขยายการเชื่อมต่อ API เพิ่มเติม
- [ ] ทำระบบ Data Persistence ด้วย JSON (บันทึก/โหลดสถานะสัตว์เลี้ยง)

### ขอบเขตงานส่วนโค้ด
- `src/pet_manager.py`: จัดการสัตว์เลี้ยงหลายตัว, active_pet, บันทึก/โหลด JSON ด้วย `to_dict()` และ `from_dict()`  
- `src/cli.py`: แสดงผลสถานะสัตว์เลี้ยงใน CLI, รับคำสั่งจากผู้ใช้  
- `src/main.py`: จุดเริ่มต้นโปรแกรม, โหลด/บันทึกสัตว์เลี้ยง, loop หลักรับคำสั่ง, เรียกใช้ PetManager และ CLI  
- `web/history.py`: ระบบ Interaction History (บันทึก, ค้นหา, กรอง, เรียงลำดับ)  
- `tests/`: Unit Test ครอบคลุม pet_manager, cli, interaction, history 

## Definition of Done (DoD)

- โปรแกรมสามารถ โหลดข้อมูลสัตว์เลี้ยงจากไฟล์ JSON ได้จริง แสดงข้อความให้ผู้ใช้เห็นเมื่อเริ่มใช้งานโปรแกรม  
- ระบบแสดง สถานะสัตว์เลี้ยง (Hunger, Energy, Happiness) พร้อมอารมณ์ปัจจุบันที่มีการแสดงผลสถานะชัดเจน  
- ระบบสามารถ ตรวจสอบชื่อสัตว์เลี้ยง เมื่อใช้ `switchpet` → แจ้งว่าไม่พบชื่อสัตว์เลี้ยงที่ไม่มีอยู่จริง รองรับ Multi-Pet Management และตรวจสอบชื่อสัตว์เลี้ยงของผู้ใช้  
- ทุก Interaction (`feed`, `play`, `sleep`, `fact`) มีระบบบันทึกและสามารถค้นหา/กรอง/เรียงลำดับได้ โดยจะถูกบันทึกลง Interaction History ระบบทำงานต่อเนื่องใน loop โดยไม่ crash กำหนดให้โปรแกรมเสถียรและพร้อมใช้งานจริง  
---
> หมายเหตุ: โค้ดของฟีเจอร์เหล่านี้มีอยู่แล้วใน `src/pet_manager.py` และ `web/history.py`
> (multi-pet, search/filter/sort, backup) แต่ยังมีปัญหาเชิงสถาปัตยกรรมและเทสต์ที่ต้องแก้ไข
> ก่อนถือว่าปิดงานได้ — ติดตามรายละเอียดในรอบแก้ไขถัดไป

รายละเอียดผลการทดสอบ: ดู `QA_TEST_LOG.md`
สรุปบทเรียน: ดู `RETROSPECTIVE.md`
