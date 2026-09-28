"""Custom exceptions ของระบบ

ทุกตัวสืบทอดจาก PetError ทำให้ Presentation Layer (CLI และ Web API)
ดักข้อผิดพลาดของระบบได้ในที่เดียว และ status_code ใช้แปลงเป็น HTTP status
"""


class PetError(Exception):
    """Base exception ของโปรเจกต์"""

    status_code = 400

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InvalidInputError(PetError):
    """อินพุตไม่ถูกต้อง เช่น ข้อความว่าง หรือค่าที่ไม่อยู่ในตัวเลือก"""


class InvalidPetNameError(InvalidInputError):
    """ชื่อสัตว์เลี้ยงไม่ผ่านการตรวจสอบ"""


class InvalidActionError(InvalidInputError):
    """คำสั่งกับสัตว์เลี้ยงที่ระบบไม่รู้จัก"""

    def __init__(self, action):
        super().__init__(f"ไม่รู้จักคำสั่ง '{action}'")
        self.action = action


class PetNotFoundError(PetError):
    """ไม่พบสัตว์เลี้ยงตามชื่อที่ระบุ"""

    status_code = 404

    def __init__(self, name):
        super().__init__(f"ไม่พบสัตว์เลี้ยงชื่อ '{name}'")
        self.name = name


class DuplicatePetError(PetError):
    """มีสัตว์เลี้ยงชื่อนี้อยู่แล้ว"""

    status_code = 409

    def __init__(self, name):
        super().__init__(f"มีสัตว์เลี้ยงชื่อ '{name}' อยู่แล้ว")
        self.name = name


class NoActivePetError(PetError):
    """ยังไม่มีสัตว์เลี้ยงให้ใช้งาน"""

    status_code = 409

    def __init__(self):
        super().__init__("ยังไม่มีสัตว์เลี้ยง กรุณาเพิ่มสัตว์เลี้ยงก่อน")
