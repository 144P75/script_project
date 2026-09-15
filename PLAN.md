# 🚀 Project Sprint Lifecycle & Reports (ALL_SPRINTS.md)

เอกสารรวบรวมแผนการดำเนินงาน ผลการพัฒนา รายงานการทดสอบระบบ (QA & Debugging Reports) และตารางการแบ่งหน้าที่ของสมาชิกในทีม สำหรับโปรเจกต์ **Virtual Pet Companion (CLI)** ครอบคลุมตั้งแต่ Sprint 1 ถึง Final Sprint

---

## 👥 ตารางบทบาทและความรับผิดชอบของสมาชิกในทีม (Team Roles & Responsibilities)

| Sprint | สมาชิกในทีม | บทบาท (Role) | หน้าที่รับผิดชอบ (Responsibilities) |
| :--- | :--- | :--- | :--- |
| **Sprint 1** | **พรีม** | **Planner** | • วางแผนและออกแบบสถาปัตยกรรมระบบแบบ Modular (`src/pet.py`, `src/cli.py`, `src/main.py`)<br>• ออกแบบโครงสร้างคลาส OOP (`Pet`, `MoodTracker`, `Interaction`)<br>• ร่างลำดับการทำงาน (Control Flow) และสเปกของไฟล์บันทึกข้อมูล `pet_state.json` |
| | **เอม** | **Coder** | • พัฒนา Business Logic Layer ใน `src/pet.py` (ระบบสถานะ, คำนวณ Time-based Decay, Cat Facts API)<br>• พัฒนา Presentation Layer ใน `src/cli.py` (หน้าจอ CLI, Status Display)<br>• เขียนฟังก์ชันเชื่อมต่อระบบ Data Access Layer และ Loop ใน `src/main.py` |
| | **เชอร์** | **Debugger / QA** | • ทำ Input Validation และ Sanitization (`.strip().lower()`) เพื่อจัดการอินพุตขยะ<br>• ดักจับ Exception (`KeyboardInterrupt`, `EOFError`, `FileNotFoundError`) ป้องกันโปรแกรม Crash<br>• พัฒนาชุดทดสอบ Unit Tests ใน `tests/test_cli.py` และตั้งค่า CI/CD Pipeline (`ci.yml`) |
| **Sprint 2** | **ชื่อผู้รับผิดชอบ** | *(ว่างไว้ระบุบทบาท)* | • *(รอระบุรายละเอียดเมื่อเริ่ม Sprint 2)* |
| | **ชื่อผู้รับผิดชอบ** | *(ว่างไว้ระบุบทบาท)* | • *(รอระบุรายละเอียดเมื่อเริ่ม Sprint 2)* |
| | **ชื่อผู้รับผิดชอบ** | *(ว่างไว้ระบุบทบาท)* | • *(รอระบุรายละเอียดเมื่อเริ่ม Sprint 2)* |
| **Sprint 3** | **ชื่อผู้รับผิดชอบ** | *(ว่างไว้ระบุบทบาท)* | • *(รอระบุรายละเอียดเมื่อเริ่ม Sprint 3)* |
| | **ชื่อผู้รับผิดชอบ** | *(ว่างไว้ระบุบทบาท)* | • *(รอระบุรายละเอียดเมื่อเริ่ม Sprint 3)* |
| | **ชื่อผู้รับผิดชอบ** | *(ว่างไว้ระบุบทบาท)* | • *(รอระบุรายละเอียดเมื่อเริ่ม Sprint 3)* |
| **Final Sprint**| **ชื่อผู้รับผิดชอบ** | *(ว่างไว้ระบุบทบาท)* | • *(รอระบุรายละเอียดเมื่อเริ่ม Final Sprint)* |
| | **ชื่อผู้รับผิดชอบ** | *(ว่างไว้ระบุบทบาท)* | • *(รอระบุรายละเอียดเมื่อเริ่ม Final Sprint)* |
| | **ชื่อผู้รับผิดชอบ** | *(ว่างไว้ระบุบทบาท)* | • *(รอระบุรายละเอียดเมื่อเริ่ม Final Sprint)* |

---

## Sprint 1: Front-End App Dev & Foundation
* **ช่วงเวลา:** สัปดาห์ที่ 12 (นำเสนอ: 15-16 ก.ย. 2569 | ส่งงาน: 18 ก.ย. 2569)
* **จุดเน้น:** การออกแบบ UI/CLI, โครงสร้าง OOP (Pet, MoodTracker, Interaction), Data Persistence (JSON) และการทำ Input Validation

### เป้าหมายและขอบเขต (Scope & DoD)
- [x] ออกแบบโครงสร้างระบบแบบ Modular (`src/cli.py`, `src/pet.py`, `src/main.py`)
- [x] พัฒนา Class ตามหลัก OOP: `Pet`, `MoodTracker` และ `Interaction`
- [x] แสดงแบนเนอร์ต้อนรับ เมนู และสถานะสัตว์เลี้ยงในระบบ CLI
- [x] รองรับการรับคำสั่งแบบไม่ไวต่อตัวพิมพ์เล็ก-ใหญ่ด้วย `.strip().lower()`
- [x] บันทึกและโหลดสถานะสัตว์เลี้ยงผ่านไฟล์ `pet_state.json`
- [x] จัดการ Exception (Invalid Input, KeyboardInterrupt, FileNotFoundError) เพื่อป้องกันไม่ให้โปรแกรม Crash
- [x] ตั้งค่า CI/CD Pipeline อัตโนมัติด้วย GitHub Actions, Pytest และ Flake8

### ผลการทดสอบประจำ Sprint 1 (Quality Assurance)
| รายการทดสอบ | อินพุต/สถานการณ์ | ผลลัพธ์ที่คาดหวัง | ผลการทดสอบจริง | สถานะ |
| :--- | :--- | :--- | :--- | :---: |
| **การออกจากโปรแกรม** | `QUIT`, ` exit ` | บันทึกข้อมูลลงไฟล์ `pet_state.json` และออกจากโปรแกรม | บันทึกไฟล์สำเร็จและหลุดออกจาก Loop | **PASSED** |
| **การจัดการคำสั่ง (Input Validation)** | `  FEED  `, `pLaY` | ตัดช่องว่าง แปลงเป็นตัวพิมพ์เล็ก และประมวลผลคำสั่งถูกต้อง | ทำงานถูกต้องตามคำสั่ง | **PASSED** |
| **การกรอกข้อมูลผิดพลาด** | `abc`, `99` | แสดงคำเตือน และวนลูปรับค่าใหม่โดยไม่พัง | แสดงแจ้งเตือน ไม่ทำให้โปรแกรม Crash | **PASSED** |
| **ไฟล์เซฟสูญหาย** | ลบไฟล์ `pet_state.json` | ระบบไม่พัง และแจ้งเตือนให้สร้างสัตว์เลี้ยงตัวใหม่ | ดักจับ Exception และให้ตั้งชื่อสัตว์เลี้ยงใหม่ได้ | **PASSED** |
| **การเชื่อมต่อ API** | คำสั่ง `fact` | ดึงเกร็ดความรู้แมวจาก Cat Facts API มาแสดงผล | แสดงผลข้อความจาก API ผ่าน `requests` สำเร็จ | **PASSED** |

### Retrospective (Wow! & Whoops!)
* **Wow! (ส่วนที่ทำได้ดี):** การวางสถาปัตยกรรมแยก 3 Layers (Presentation, Business Logic, Data Access) ทำให้เขียน Unit Test ได้ง่าย โค้ดอ่านเป็นระเบียบ และมีระบบ Input Sanitization ที่รัดกุม
* **Whoops! (ปัญหาและแก้ไข):** ช่วงแรกการกด `Ctrl+C` ขณะรับ Input ทำให้เกิด `KeyboardInterrupt` โค้ดหลุดกระจาย แก้ไขโดยการครอบ `try-except (KeyboardInterrupt, EOFError)` ใน `src/cli.py` ให้ปิดโปรแกรมได้อย่างนุ่มนวล (Graceful Exit)

---

## Sprint 2: Back-End App Dev
* **ช่วงเวลา:** สัปดาห์ที่ 13 (นำเสนอ: 22-23 ก.ย. 2569 | ส่งงาน: 25 ก.ย. 2569)
* **จุดเน้น:** การขยายขีดความสามารถ Business Logic Layer, ระบบจัดเก็บข้อมูลขั้นสูง และการประมวลผลข้อมูล

### เป้าหมายและขอบเขต (Scope & DoD)
- [ ] เพิ่มความสามารถในการจัดการสัตว์เลี้ยงหลายตัว (Multi-Pet Management)
- [ ] พัฒนาระบบค้นหา กรองข้อมูล และเรียงลำดับประวัติการโต้ตอบของสัตว์เลี้ยง
- [ ] ปรับปรุง Data Access Layer ให้รองรับการสำรองข้อมูล (Backup & Auto-Save)
- [ ] ขยายการเชื่อมต่อ API เพิ่มเติม (เช่น Dog API หรือ Weather API เพื่อปรับอารมณ์สัตว์เลี้ยงตามสภาพอากาศ)

### ผลการทดสอบประจำ Sprint 2 (QA Plan)
| รายการทดสอบ | อินพุต/สถานการณ์ | ผลลัพธ์ที่คาดหวัง | ผลการทดสอบจริง | สถานะ |
| :--- | :--- | :--- | :--- | :---: |
| การจัดการสัตว์เลี้ยงหลายตัว | สลับใช้งานโปรไฟล์ Pet A / Pet B | โหลดข้อมูลและแยกไฟล์ JSON ของแต่ละตัวได้ถูกต้อง | *Pending* | **PENDING** |
| การค้นหาประวัติกิจกรรม | ค้นหาด้วยคำสั่ง `history` | แสดงรายการกิจกรรมที่ผ่านมาเรียงตามลำดับเวลา | *Pending* | **PENDING** |
| ระบบ Auto-Save & Backup | โปรแกรมปิดตัวกะทันหัน | มีไฟล์สำรองข้อมูลล่าสุดเพื่อป้องกันข้อมูลสูญหาย | *Pending* | **PENDING** |

### Retrospective
* *(รอสรุปหลังเสร็จสิ้น Sprint 2)*

---

## Sprint 3: Full-Stack App Dev
* **ช่วงเวลา:** สัปดาห์ที่ 14 (นำเสนอ: 29-30 ก.ย. 2569 | ส่งงาน: 2 ต.ค. 2569)
* **จุดเน้น:** การเชื่อมต่อระบบสมบูรณ์, ระบบ Time-based Decay Over Time ขั้นสูง และการรับมือ Edge Cases

### เป้าหมายและขอบเขต (Scope & DoD)
- [ ] เชื่อมต่อ UI/CLI เข้ากับคลาส Business Logic และ Data Access Layer อย่างสมบูรณ์แบบไร้รอยต่อ
- [ ] พัฒนากลไกคำนวณส่วนต่างของเวลา (`timestamp`) เพื่อหักลบค่า Stats (Decay Over Time) อัตโนมัติเมื่อไม่ได้เปิดโปรแกรมเป็นเวลานาน
- [ ] ประเมินและจัดการกรณีขอบเขต (Edge Cases) เช่น ค่า Hunger/Energy ติดลบ หรือเกิน 100
- [ ] ปรับปรุง UX/UI การแสดงผลหน้าจอ CLI ให้มีแถบพลังงาน (Status Bar) สวยงาม

### ผลการทดสอบประจำ Sprint 3 (QA Plan)
| รายการทดสอบ | อินพุต/สถานการณ์ | ผลลัพธ์ที่คาดหวัง | ผลการทดสอบจริง | สถานะ |
| :--- | :--- | :--- | :--- | :---: |
| คำนวณ Decay ตามเวลาข้ามคืน | ปิดโปรแกรมไว้ 12 ชั่วโมง | เมื่อเปิดใหม่ ค่า Hunger เพิ่มขึ้น และ Energy ลดลงอย่างสมเหตุสมผล | *Pending* | **PENDING** |
| Edge Case (Stats Boundary) | สั่ง Feed / Play รัวๆ | ค่า Energy ไม่ต่ำกว่า 0 และ Hunger ไม่เกิน 100 | *Pending* | **PENDING** |
| การแสดงผล Status Bar | สั่งดูสถานะ | แถบสถานะแบบ ASCII/Progress bar แสดงผลถูกต้อง | *Pending* | **PENDING** |

### Retrospective
* *(รอสรุปหลังเสร็จสิ้น Sprint 3)*

---

## Final Sprint: DevOps, CI/CD & AI Integration
* **ช่วงเวลา:** สัปดาห์ที่ 15 (นำเสนอ: 6-7 ต.ค. 2569 | ส่งงานส่งท้าย: 16 ต.ค. 2569)
* **จุดเน้น:** Automated Testing, GitHub Actions CI/CD Pipeline และ AI/Automation Agent Integration

### เป้าหมายและขอบเขต (Scope & DoD)
- [ ] พัฒนาชุดทดสอบอัตโนมัติ (Automated Unit Tests) ครอบคลุม Code Coverage มากกว่า 80%
- [ ] ปรับแต่ง CI/CD Pipeline บน GitHub Actions ให้ตรวจ Linting และรัน Unit Test อัตโนมัติทุกครั้งที่มี Push/PR
- [ ] เชื่อมต่อฟีเจอร์ AI หรือ Smart Automation Agent (เช่น AI ประเมินอารมณ์สัตว์เลี้ยง หรือสร้างบทสนทนาโต้ตอบแบบไดนามิก)
- [ ] รวบรวม Artifacts, สรุปผลโปรเจกต์ และจัดทำสไลด์นำเสนอฉบับสมบูรณ์ (5-Part Presentation)

### ผลการทดสอบประจำ Final Sprint (QA Plan)
| รายการทดสอบ | อินพุต/สถานการณ์ | ผลลัพธ์ที่คาดหวัง | ผลการทดสอบจริง | สถานะ |
| :--- | :--- | :--- | :--- | :---: |
| GitHub Actions CI/CD | Push Code ขึ้น Main | Workflow รันผ่าน (Passed) ทั้งหมด ไม่พบ Linting/Test Error | *Pending* | **PENDING** |
| AI Companion Interaction | เรียกฟีเจอร์ AI Chat/Fact | AI ตอบกลับวิเคราะห์สถานะสัตว์เลี้ยงได้เป็นธรรมชาติและถูกต้อง | *Pending* | **PENDING** |
| End-to-End System Test | รันโปรแกรมเต็มรูปแบบ | ทำงานได้ราบรื่น ไม่พบ Memory Leak หรือ Unhandled Crash | *Pending* | **PENDING** |

### Retrospective
* *(รอสรุปหลังเสร็จสิ้น Final Sprint)*
