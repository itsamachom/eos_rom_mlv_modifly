# Canon 600D 1.0.2 — Photo UI v3r2 Full EXPERIMENTAL

ใช้ **600D-102-PHOTO-UI-v3r2-FULL-EXPERIMENTAL.zip** แทน v3r1 คงฟอนต์เดิม เปลี่ยนไฮไลต์จุดชัดเป็น Focus Peaking

แก้สาเหตุ Arkanoid ไม่สร้างแท็บเกม: โค้ด menu_add_internal บน 600D ยังทิ้งการลงทะเบียน Games อยู่ v3r2 เอาการบล็อกนี้ออกแล้ว ไฟล์ arkanoid.mo มีอยู่แล้วใน v3r1

Pong และ Sokoban เป็นสคริปต์ Lua ไม่ใช่โมดูลแยก ตรวจพบไฟล์และ helper ครบใน Full ZIP นี้:

- ML/modules/arkanoid.mo
- ML/modules/lua.mo
- ML/scripts/pong.lua
- ML/scripts/sokoban.lua
- ML/scripts/lib/keys.lua
- ML/scripts/lib/config.lua

อ่าน [คู่มือเปิดเกมและแก้ปัญหา](../../GAMES_V3R2_TH.md) และ [คู่มือติดตั้ง](../../PHOTO_UI_V3R2_INSTALL_TH.md) Full ZIP มี GAMES_TH.md, INSTALL_TH.md และซอร์สใน SOURCE/ อยู่แล้ว ผู้ที่ติดตั้ง ML แล้วอัปเดต autoexec.bin และ ML/ ทั้งชุดหลังสำรองข้อมูล ไม่เรียก Firmware Update ซ้ำ

Source commit: 5f543089565c1574606ea2436315e6ea5419ce70. ผ่าน clean ARM build, 28 ASan/UBSan groups, 38 ELF/module/script bindings, production Games registry/Arkanoid init+start test, imports 32 ตัวของ Arkanoid และ 242 ตัวของ Lua กับ core symbols ที่อยู่ใน ZIP เดียวกัน รวม source/atlas equality, ZIP CRC, XOR และ SHA256

ตรวจไฟล์ด้วย `sha256sum -c SHA256SUMS` จากโฟลเดอร์นี้

**ยังไม่ได้ทดสอบ v3r2 บนกล้องจริง รวมถึงการติดตั้งครั้งแรกและการเล่นเกม** ไม่ได้รัน QEMU ตัวติดตั้ง FIR เดิมไม่แก้และไม่ได้ rebuild เป็น Codex/LLM-assisted fork ที่ upstream ไม่ได้รับรอง เก็บ GPL/OFL และประกาศลิขสิทธิ์เดิม
