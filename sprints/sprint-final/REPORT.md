# Final Sprint: DevOps, CI/CD & AI Integration

**สถานะ:** พัฒนาเสร็จ (v0.4.3) · นำเสนอ 6-7 ต.ค. 2569 · ส่งงาน 16 ต.ค. 2569 (v1.0.0)
**จุดเน้น:** AI Companion, Automated Testing, CI/CD บน GitHub Actions และ Deploy ออนไลน์
**เว็บออนไลน์:** https://virtual-pet-companion.onrender.com/

## บทบาทในทีม (Sprint นี้)
| สมาชิก | บทบาท | หน้าที่รับผิดชอบ |
|---|---|---|
| เชอร์ | Planner / Architect | กำหนดขอบเขต AI Companion และ DoD, ออกแบบสถาปัตยกรรม AI (fallback, เรียกนอก lock), วางแผน CI/CD และ deploy |
| พรีม | Coder | พัฒนา `src/companion.py` (Gemini / ChatGPT / Claude), `PetService.talk()`, คำสั่ง `talk`, API และกล่องสนทนา, `.env`, `render.yaml`, โหมดหลายผู้เล่น |
| เอม | Debugger / QA | ทดสอบ edge case ของ AI (ไม่มี key, 404, 503, ข้อความว่าง/ยาวเกิน), เขียนเทสต์ที่ mock AI, ตรวจ CI, รีวิว PR, จัดทำ QA Test Log |

## เป้าหมายและขอบเขต (Scope)
- [x] คำสั่ง `talk` ใช้ได้ทั้ง CLI และเว็บ AI ตอบในบทบาทแมวตามสถานะจริง (หิว / ง่วง / มีความสุข)
- [x] การคุยเพิ่มความสุข +5 — AI เป็นส่วนหนึ่งของ Business Logic ไม่ใช่ chatbot แยก
- [x] รองรับ AI 3 เจ้า: Gemini, ChatGPT, Claude เลือกด้วย `AI_PROVIDER` หรือ key ที่ตั้งไว้
- [x] ไม่มี key / timeout / server ไม่ว่าง / ตอบผิดรูปแบบ → ลองใหม่ 1 ครั้ง แล้วตอบแบบออฟไลน์ตามอารมณ์ ไม่ crash
- [x] บันทึกทั้งข้อความผู้ใช้และคำตอบลงประวัติ (`kind = talk`) ค้นหา/กรองได้
- [x] เก็บ API key ใน `.env` หรือ environment variable ไม่อยู่ใน repo
- [x] CI: flake8 แบบเต็ม + pytest บน Python 3.10 และ 3.12 ทุก push และ PR
- [x] CD: merge เข้า main แล้ว Render deploy ใหม่อัตโนมัติ (`render.yaml`)
- [x] บนเว็บออนไลน์ แต่ละเบราว์เซอร์มีสัตว์เลี้ยงของตัวเอง (`MULTI_PLAYER=1`)

## ขอบเขตงานส่วนโค้ด
| ไฟล์ | Layer | สิ่งที่ทำ |
|---|---|---|
| `src/companion.py` | Business Logic | `PetCompanion`: prompt จากสถานะ, เรียก Gemini/ChatGPT/Claude, ลองใหม่, คำตอบออฟไลน์ |
| `src/service.py` | Service | `PetService.talk()`: ตรวจข้อความ, ความสุข +5, เรียก AI นอก lock, บันทึกประวัติ |
| `src/main.py`, `src/cli.py` | Presentation | คำสั่ง `talk` (คุยต่อเนื่องจนกด Enter ว่าง), โหลด `.env` |
| `web/app.py` | Presentation (Web) | `POST /api/pet/talk`, โหมดหลายผู้เล่นแยก `PetService` ตามรหัสผู้เล่น |
| `web/static/index.html` | Presentation (Web) | กล่องสนทนา + ป้าย "ตอบโดย AI" / "โหมดออฟไลน์", สุ่มรหัสผู้เล่น |
| `.github/workflows/ci.yml` | DevOps | matrix Python 3.10/3.12, flake8, pytest |
| `render.yaml` | DevOps | gunicorn 1 worker หลาย thread, `MULTI_PLAYER=1`, key ใส่ในหน้า Render |
| `tests/test_companion.py` ฯลฯ | Test | mock AI ทุกเจ้า, ลองใหม่, หลายผู้เล่น (รวม 91 เทสต์) |

## สถาปัตยกรรมของ AI
```text
ผู้ใช้ (CLI talk / กล่องสนทนาบนเว็บ)
        ↓
PetService.talk()  → ตรวจข้อความ, pet.chat() (ความสุข +5), บันทึกข้อความผู้ใช้   [ใน lock]
        ↓
PetCompanion.reply(pet, message)                                            [นอก lock]
   ├─ มี key → Gemini / ChatGPT / Claude (system prompt = บทบาทแมว + สถานะปัจจุบัน)
   │           timeout หรือ 429/5xx → รอ 1 วินาที ลองใหม่ 1 ครั้ง
   └─ ไม่มี key / ยังล้มเหลว → คำตอบสำรองตามอารมณ์
        ↓
บันทึกคำตอบลงประวัติ (source = AI Companion หรือ Companion (offline))
```

## Definition of Done
- [x] `talk` ใช้ได้ทั้ง CLI และเว็บ และคำตอบเปลี่ยนตามสถานะของสัตว์เลี้ยง
- [x] ไม่มี API key หรือ API ล่ม → ตอบแบบออฟไลน์ ไม่ crash
- [x] ประวัติกรอง `talk` แล้วเห็นทั้งข้อความผู้ใช้และคำตอบ
- [x] GitHub Actions ผ่านทั้ง flake8 และ pytest บน 2 เวอร์ชัน Python
- [x] ไม่มี API key อยู่ใน repo
- [x] เว็บเปิดใช้ออนไลน์ได้ และผู้ใช้แต่ละคนเห็นข้อมูลของตัวเอง

## เวอร์ชันใน Sprint นี้
| เวอร์ชัน | สิ่งที่ได้ |
|---|---|
| 0.4.0 | AI Companion (`talk`), โหมดออฟไลน์, CI matrix + flake8 เต็ม |
| 0.4.1 | รองรับ Gemini / ChatGPT / Claude, แก้ตัวอักษรช่องพิมพ์จาง |
| 0.4.2 | `.env`, ลองใหม่เมื่อ AI error ชั่วคราว, เตรียม deploy (`render.yaml`, gunicorn) |
| 0.4.3 | โหมดหลายผู้เล่นบนเว็บออนไลน์ |
| 1.0.0 | (16 ต.ค.) เอกสารครบ + แก้ตามที่พบระหว่างนำเสนอ |

## ข้อจำกัดที่ทราบ
- Render แผนฟรี: server หลับเมื่อไม่มีคนใช้ 15 นาที และข้อมูลหายเมื่อหลับ restart หรือ deploy ใหม่
- โหมดหลายผู้เล่นผูกกับเบราว์เซอร์: เปลี่ยนเบราว์เซอร์หรือล้างข้อมูลเบราว์เซอร์ = เริ่มใหม่
- Gemini รุ่น lite (ฟรี) บางครั้งตอบปนอักษรลาว — เปลี่ยนรุ่นได้ด้วย `GEMINI_MODEL` โดยไม่แก้โค้ด
- ทุกคนบนเว็บออนไลน์ใช้โควตา AI ของเจ้าของ key

## ผลการทดสอบ
- `QA_TEST_LOG.md` · CI: แท็บ Actions ของ repository
