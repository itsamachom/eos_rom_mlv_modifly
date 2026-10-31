# Canon 600D / Canon 1.0.2 — Photo UI v3r1 Full EXPERIMENTAL

ใช้ **600D-102-PHOTO-UI-v3r1-FULL-EXPERIMENTAL.zip** แทน v3 อ่าน [คู่มือติดตั้ง](../../PHOTO_UI_V3R1_INSTALL_TH.md) และ [รายละเอียด](../../PHOTO_UI_V3R1.md)

- คืนฟอนต์และคำแปลเดิมจาก TH2 (d68c296) ทั้งด้านนอก/ด้านใน ยกเว้นชื่อที่สั่งแก้ ใช้ 23/28/32 แบบเดิม ไม่ย่อฟอนต์
- ตรวจ glyph ครบทุกตัวอักษรไทยและอังกฤษ แก้สี่เหลี่ยมแทน B/SET/MENU/Q
- เกมแยกหมวด G มี Arkanoid/Pong/Sokoban ต้องโหลดโมดูล arkanoid/lua ก่อน
- ข้อมูลกล้องแยกรุ่น/เฟิร์มแวร์คนละแถว จำนวนชัตเตอร์แยกกลไก/Live View/รวม เป็นค่าจำนวนเต็ม อ่านอย่างเดียวและรอ property จริง
- คงชื่อ Histogram, Waveform, Time-lapse, ถ่ายคร่อม, zebra settings และ Bitrate (CBR) นำ Silent Picture ออก ยังไม่เปลี่ยน Picture Style

Source commit: 12d71a6ddf73e192ed903687b8561cc45a11f0f9. Full ZIP รวมซอร์สไว้ใต้ SOURCE/ พร้อม GPL และคู่มือ ส่วน source.zip แยกให้ดาวน์โหลดอีกทาง

ผ่าน clean ARM build, 26 ASan/UBSan test groups, 38 ELF/module/script bindings, original-translation comparison, glyph coverage, production property/camera callback tests, ZIP CRC, source/atlas equality, autoexec XOR และ SHA256 ตัวติดตั้ง FIR ต้นฉบับไม่แก้และไม่ได้ rebuild

ตรวจด้วย `sha256sum -c SHA256SUMS` จากโฟลเดอร์นี้

[ภาพตรวจ layout บน host](../../previews/photo-ui-v3r1-layout-proof.png) ใช้ renderer จริงกับฟอนต์ที่แจก ตัวเลขชัตเตอร์ในภาพเป็นค่าจำลอง ไม่ใช่ข้อมูลจากกล้องของผู้ใช้

**ยังไม่ทดสอบ v3r1 บนกล้องจริง รวมถึงการติดตั้งครั้งแรก** ไม่ได้รัน QEMU ผล host ไม่ยืนยันฮาร์ดแวร์ เป็น Codex/LLM-assisted fork ที่ upstream ไม่ได้รับรอง

ผู้ที่ติดตั้ง ML แล้วให้อัปเดต autoexec.bin และ ML/ ทั้งชุดหลังสำรองข้อมูล ไม่เรียก Firmware Update ซ้ำสำหรับอัปเดต UI นี้
