"""Data Access Layer: อ่าน/เขียนไฟล์ JSON อย่างปลอดภัย

- เขียนแบบ atomic (เขียนไฟล์ชั่วคราวก่อนแล้วค่อยแทนที่) ไฟล์จึงไม่เสียถ้าโปรแกรมปิดกลางคัน
- ก่อนเขียนทับ จะคัดลอกไฟล์เดิมที่ยังอ่านได้ไปเป็นไฟล์สำรอง
- ถ้าไฟล์หลักหายหรือเสีย จะกู้จากไฟล์สำรอง และเก็บไฟล์ที่เสียไว้เป็น .corrupt
"""
import json
import os
import shutil


class JsonStore:
    """จัดเก็บข้อมูล 1 ชุดลงไฟล์ JSON พร้อมไฟล์สำรอง"""

    def __init__(self, path, backup_path=None, default_factory=dict):
        self.path = path
        self.backup_path = backup_path
        self.default_factory = default_factory

    def _read(self, path):
        """คืนข้อมูลจากไฟล์ หรือ raise ValueError ถ้าไฟล์เสีย/ผิดชนิด"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, type(self.default_factory())):
            raise ValueError("ชนิดข้อมูลในไฟล์ไม่ถูกต้อง")
        return data

    def _read_backup(self):
        if not self.backup_path:
            return None
        try:
            return self._read(self.backup_path)
        except (OSError, ValueError):
            return None

    def load(self):
        """คืน (data, warning) — warning เป็น None ถ้าโหลดได้ตามปกติ"""
        try:
            return self._read(self.path), None
        except FileNotFoundError:
            backup = self._read_backup()
            if backup is not None:
                return backup, "ไม่พบไฟล์ข้อมูลหลัก จึงกู้คืนจากไฟล์สำรอง"
            return self.default_factory(), None
        except (OSError, ValueError):
            self._quarantine()
            backup = self._read_backup()
            if backup is not None:
                return backup, "ไฟล์ข้อมูลหลักเสียหาย จึงกู้คืนจากไฟล์สำรอง"
            return self.default_factory(), "ไฟล์ข้อมูลเสียหายและไม่มีไฟล์สำรอง จึงเริ่มต้นใหม่"

    def _quarantine(self):
        """เก็บไฟล์ที่เสียไว้ตรวจสอบภายหลัง แทนการลบทิ้ง"""
        try:
            shutil.copyfile(self.path, self.path + ".corrupt")
        except OSError:
            pass

    def save(self, data):
        """บันทึกแบบ atomic และสำรองเวอร์ชันก่อนหน้า"""
        folder = os.path.dirname(os.path.abspath(self.path))
        os.makedirs(folder, exist_ok=True)
        if self.backup_path:
            try:
                self._read(self.path)
                shutil.copyfile(self.path, self.backup_path)
            except (OSError, ValueError):
                pass
        tmp_path = self.path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, self.path)
        if self.backup_path and not os.path.exists(self.backup_path):
            shutil.copyfile(self.path, self.backup_path)
