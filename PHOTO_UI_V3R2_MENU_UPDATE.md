# v3r2-menu-update — 600D.102 Experimental

- เปลี่ยนคำเป็น ค่าแสง (TV, AV), ล็อคกระจกสะท้อน และ วิธีล็อคกระจก
- เปลี่ยน หน่วงหลังยกกระจก เป็น หน่วงเมื่อถ่าย Time-lapse/ถ่ายคร่อม
- ชื่อยาวใช้ฟอนต์ 20px เฉพาะรายการนี้ เพื่อให้อ่านครบในช่อง 318px
- ตัดโหมดถือกล้อง และตัวเลือกชัตเตอร์/หน่วงเมื่อถือกล้องออกจาก 600D
- ค่าตั้งเก่าที่เคยเลือกโหมดถือกล้องจะกลับมาเป็นโหมดตั้งเวลาถ่าย
- คงการล็อคกระจกแบบเปิดตลอดและเชื่อมกับตั้งเวลาถ่าย ตลอดจนค่าหน่วงสำหรับ ML ถ่ายอัตโนมัติ

ผู้ใช้ยืนยันว่าการถ่ายหลายภาพในโหมดตั้งเวลาเกิดจากจำนวนภาพที่ตั้งไว้ ไม่ใช่ข้อผิดพลาดของเฟิร์มแวร์ จึงไม่ได้เปลี่ยนโค้ดเพื่อแก้อาการนี้

ข้อความ TV/AV เป็นการเปลี่ยนป้ายภาษาไทยตามคำขอ ไม่ได้เปลี่ยนอัลกอริทึมถ่ายคร่อมเดิม (M ปรับ Tv; โหมดอื่นปรับ AE compensation)

Build from the current working source (base commit plus uncommitted changes):

```sh
PATH=/workspace/ml-env/venv/bin:$PATH make -C firmware/platform/600D.102 -j4 ARM_BINPATH=/workspace/ml-env/toolchain/usr/bin CONFIG_QEMU=n VERSION=PHOTO-UI-v3r2-menu-update.600D.102
python3 tests/check_mlu_modes.py
/workspace/ml-env/venv/bin/python tests/check_photo_ui_v3.py
bash tests/run-photo-menu-tests.sh
python3 tests/check_game_registration.py
python3 tests/check_photo_menu_bindings.py
python3 tests/check_packaged_games.py
```

Codex/LLM-assisted changes cover translations, font generation, 600D feature selection, legacy MLU mode migration and regression tests. Host checks do not establish camera hardware behavior. This update has not been tested on a camera. The existing v3r2 delivery archives remain unchanged.
