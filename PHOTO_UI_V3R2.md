# Photo UI v3r2 — Canon 600D firmware 1.0.2

แก้จาก v3r1 โดยคงฟอนต์ขนาดเดิมและคำแปลอื่นไว้

- เปลี่ยนชื่อ ไฮไลต์จุดชัด เป็น **Focus Peaking** ทั้งชื่อรายการและคำแปลของ Focus Peak เดิม การเชื่อมฟังก์ชันยังเป็น Overlay → Focus Peak ของ ML
- เอาเงื่อนไขใน menu_add_internal ที่บล็อก Games บน 600D ออก ทำให้โมดูล Arkanoid สร้างเมนูเดิมได้ ไฟล์ arkanoid.mo มีอยู่แล้วใน v3r1 ข้อบกพร่องคือการลงทะเบียนเมนู ไม่ใช่ขาดไฟล์
- Pong/Sokoban เป็นสคริปต์ Lua ใช้โมดูล lua ไม่ใช่โมดูลแยก เพิ่มข้อความแนะนำโมดูลเฉพาะเกมและแปล Run Script/Autorun โดยไม่เปิดเกมหรือ Autorun อัตโนมัติ
- ทางเข้าของเกม Lua ข้ามแถว container ที่ไม่ได้เริ่มเกม ไปที่ Run Script และตัวเลือกจริง
- ไม่เปลี่ยน Picture Style หรือฟอนต์

อ่าน **GAMES_V3R2_TH.md** สำหรับไฟล์ที่ต้องมี การเปิดโมดูล การรีสตาร์ต ปุ่มเล่น และการตรวจสถานะผิดปกติ อ่าน PHOTO_UI_V3R2_INSTALL_TH.md สำหรับติดตั้งครั้งแรก

ตรวจ clean ARM build, 28 ASan/UBSan test groups, 38 actual ELF/module/script bindings, production Games registration/Arkanoid init+start host test, ไฟล์เกมและ helper ใน ZIP, imports ของ arkanoid/lua กับ symbol file ที่แพ็ก, คำแปลเดิมยกเว้นชื่อที่สั่งเปลี่ยน และ checksum/source/atlas integrity

```
bash tests/run-photo-menu-tests.sh
/workspace/ml-env/venv/bin/python tests/check_photo_ui_v3.py
python3 tests/check_game_registration.py
bash scripts/build-photo-ui.sh --clean
python3 tests/check_photo_menu_bindings.py
python3 tests/check_packaged_games.py
python3 tools/package_photo_ui_v3r2.py
```

ใช้ toolchain เดิม ARM GCC 14.2.1, CONFIG_QEMU=n และ tools/requirements-thai.txt ใน Python venv ไม่ได้รัน QEMU

**ยังไม่ทดสอบ v3r2 บนกล้องจริง รวมถึงการติดตั้งครั้งแรกและการเล่นเกม** ตัวติดตั้ง FIR เดิมไม่แก้และไม่ได้ rebuild ตรวจ SHA256 เดิมก่อนแพ็ก งาน fork ใช้ Codex/LLM ช่วย ไม่ใช่ upstream-endorsed release เก็บ GPL/OFL และประกาศเดิม
