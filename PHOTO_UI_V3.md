# Canon 600D 1.0.2 — Photo UI v3 Full (ทดลอง)

ฐาน: package/600d-photo-ui-v2-full (ca97d4ea27d08fee3698c5c8ac2ee0753b75a2f2)
Branch: feature/600d-full-thai-menu-revision

ยังไม่ทดสอบบนกล้องจริงและยังไม่ยืนยันการติดตั้งครั้งแรก อ่าน PHOTO_UI_V3_INSTALL_TH.md ก่อนติดตั้ง ใช้เฉพาะ Canon 600D firmware 1.0.2 ไม่รวม Canon firmware updater

## เมนูและภาษา

- คงรายการหน้า Photo UI เดิมทุกตัว ยกเว้น Silent Picture ที่นำออก พร้อมนำ silent.mo และ placeholder ของ 600D ออกจากแพ็กเกจใหม่
- ชื่อหน้าใหม่: Histogram, Waveform, Time-lapse, ถ่ายคร่อม, zebra settings
- Movie → Bitrate (CBR) เชื่อมกับ Bit Rate ของ ML เดิม ใช้ Mode = CBR และ CBR factor ในตัวเลือกเดิม ยังมี OFF/QScale ตามโค้ดเดิม ไม่บังคับเริ่มบันทึกหรือเปลี่ยน bitrate อัตโนมัติ
- คืน Arkanoid (Setup → เกม หลังโหลด arkanoid) และ pong.lua / sokoban.lua (Setup → สคริปต์ หลังโหลด lua) โมดูลไม่ถูกเปิดอัตโนมัติ ให้เปิดใน Setup → โมดูล แล้วรีสตาร์ตตาม ML
- Setup เพิ่มข้อมูลกล้อง จำนวนชัตเตอร์ เกม สคริปต์ เสียง และทางเข้า Shoot/Focus/Expo/Overlay/Movie แบบเดิมทั้งหมด INFO สลับกลับ Classic ได้
- ภาษาไทย 48 ข้อความในหน้า Photo UI: หมวด รายการหลัก สถานะ และคำแนะนำปุ่ม ใช้บิตแมป Noto Sans Thai ที่จัดสระด้วย RAQM ไม่ส่ง UTF-8 ให้ฟอนต์ ML เดิม คงคำเทคนิคบางชื่อเป็นอังกฤษ เมนูย่อยดั้งเดิม ค่าและคำเตือนจาก ML ยังใช้ภาษาดั้งเดิม ไม่ใช่การแปลทุกข้อความของ ML
- ไม่แก้ Picture Style และไม่เพิ่มสไตล์ใหม่ ทางเข้าของเดิมยังอยู่
- ข้อมูลกล้องใช้ camera_model / firmware_version จาก property ของ Canon ไม่มีการสร้าง serial หรือเดารุ่นจากชื่อแพ็กเกจ
- จำนวนชัตเตอร์แสดง Unavailable (ยังอ่านค่าไม่ได้) จนรับ PROP_SHUTTER_COUNTER ขนาดอย่างน้อย 8 ไบต์และค่าถูกช่วง แสดงค่า mechanical + Live View แบบเดิมของ ML ไม่ใช่จำนวนไฟล์ภาพหรือค่าประเมินจากชื่อไฟล์ ค่า 0 จะแสดงได้เมื่อได้รับ property จริงเท่านั้น

## ใช้งาน

ขึ้น/ลงเลือกหมวด → ขวา/SET เลือกรายการ → ขวา/SET เข้าแผงขวา → SET เข้าแก้ค่า → ซ้าย/ขวาปรับ → SET จบ ซ้ายกลับ Q เปิดตัวเลือกเดิม คำสั่ง Action ต้องยืนยัน SET อีกครั้ง MENU ยกเลิก INFO สลับ Classic

## Build และตรวจสอบ

```
bash baseline-600d-102/bootstrap-toolchain.sh
python3 -m venv /workspace/ml-env/venv
/workspace/ml-env/venv/bin/pip install docutils pycparser Pillow
bash tests/run-photo-menu-tests.sh
python3 tests/check_photo_ui_v3.py
bash scripts/build-photo-ui.sh --clean
python3 tests/check_photo_menu_bindings.py
python3 tools/package_photo_ui_v3.py
```

ARM GCC 14.2.1; -j4; CONFIG_QEMU=n. บิตแมปภาษาไทยถูกเก็บในซอร์สแล้ว ไม่ต้องสร้างใหม่เพื่อ build หากแก้คำแปลใช้ tools/generate_photo_thai.py ซึ่งต้องมี Pillow/RAQM และ NotoSansThai-Regular.ttf ตามพาธในสคริปต์ ใบอนุญาตฟอนต์อยู่ firmware/data/fonts/thai/NOTO-LICENSE.txt

Host tests ใช้ ASan/UBSan, ตรวจ binding กับ ARM ELF/โมดูลจริง และตรวจ ZIP/XOR/SHA256 ไม่ยืนยันการบูต การเรนเดอร์บนจอกล้อง การเล่นเกม การบันทึกภาพ/เสียง หรือความถูกต้องของ counter บนฮาร์ดแวร์ ต้องตรวจบนกล้องต่อไป ไม่ได้รัน QEMU

ML-SETUP.FIR ใช้ต้นฉบับจากฐาน ไม่แก้และไม่ได้ rebuild ตรวจ SHA256 เทียบค่าฐานก่อนแพ็ก คู่มือติดตั้งรองรับกล้องที่ไม่เคยลง ML แต่ยังไม่ผ่าน hardware test

งาน fork นี้ใช้ Codex/LLM ช่วย ไม่ใช่ upstream-endorsed release เก็บ COPYING และประกาศลิขสิทธิ์เดิม
