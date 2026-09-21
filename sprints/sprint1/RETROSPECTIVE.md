# Retrospective — Sprint 1

**Wow! (ส่วนที่ทำได้ดี):** การวางสถาปัตยกรรมแยก 3 Layers (Presentation, Business Logic, Data Access) ทำให้เขียน Unit Test ได้ง่าย โค้ดอ่านเป็นระเบียบ และมีระบบ Input Sanitization ที่รัดกุม

**Whoops! (ปัญหาและแก้ไข):** ช่วงแรกการกด `Ctrl+C` ขณะรับ Input ทำให้เกิด `KeyboardInterrupt` โค้ดหลุดกระจาย แก้ไขโดยการครอบ `try-except (KeyboardInterrupt, EOFError)` ใน `src/cli.py` ให้ปิดโปรแกรมได้อย่างนุ่มนวล (Graceful Exit)
