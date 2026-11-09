# v3r2-menu-update2 — 600D.102 Experimental

เปลี่ยนชื่อ Normal MLU Delay เป็น **สำหรับ Timelapse/ถ่ายคร่อม** และเพิ่มฟอนต์เฉพาะรายการจาก 20px เป็น 25px (ขนาดวัดได้ประมาณ 310px ในช่อง 318px) ไม่เปลี่ยนค่าหน่วงหรือการถ่ายภาพ

## ข้อมูลกล้องไม่ได้หาย

ใน Photo UI เลือกหมวด **ตั้งค่า (+)** แล้วกดลงผ่าน **ตรวจสอบระบบ** ไปยัง **หน้า 2/3**:

- **ข้อมูลกล้อง**: รุ่นกล้อง และเฟิร์มแวร์ Canon ที่กล้องรายงาน
- **จำนวนชัตเตอร์**: ชัตเตอร์กลไก, กลไก Live View และรวมการทำงาน

Live View แสดงจำนวนการทำงานที่คำนวณจากตัวนับรวมลบตัวนับชัตเตอร์กลไก ไม่ใช่การนับไฟล์ภาพที่ถ่ายใน Live View โดยตรง หากกล้องไม่รายงานค่าที่ใช้ได้จะแสดง Unavailable ไม่เดาเป็นศูนย์

Host tests now navigate from the first Setup item to Camera Info on page 2/3 using Down/Right keys, in Thai and English. Existing read-only model/firmware and three counter tests remain. Camera-info code and menu ordering are unchanged.

Build version: PHOTO-UI-v3r2-menu-update2.600D.102. Target: Canon 600D with Canon firmware 1.0.2. Source ZIP contains the exact working source based on b574392 plus these changes; BUILD_INFO.json records its hash.

Build and checks:

```sh
PATH=/workspace/ml-env/venv/bin:$PATH make -C firmware/platform/600D.102 -j4 ARM_BINPATH=/workspace/ml-env/toolchain/usr/bin CONFIG_QEMU=n VERSION=PHOTO-UI-v3r2-menu-update2.600D.102
/workspace/ml-env/venv/bin/python tests/check_photo_ui_v3.py
bash tests/run-photo-menu-tests.sh
python3 tests/check_mlu_modes.py
python3 tests/check_photo_menu_bindings.py
python3 tests/check_packaged_games.py
```

Codex/LLM assistance covers the label, generated font atlas, navigation tests and package documentation. This is experimental, not camera/QEMU tested. Preserve inherited licenses and source-audit limitations in THIRD_PARTY_NOTICES.md and release/v3r2/PROVENANCE.md. The previous delivery remains unchanged.
