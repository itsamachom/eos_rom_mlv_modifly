# Photo UI v2 — 600D / Canon 1.0.2

ไฟล์ทดสอบสำหรับกล้อง: **600D-102-PHOTO-UI-v2-TEST.zip** กด Download raw file แล้วอ่าน [คู่มือ v2 ภาษาไทย](../../PHOTO_UI_V2.md) ก่อนเปลี่ยนไฟล์ในการ์ด เก็บบิลด์ v1 ที่ใช้งานได้ไว้ย้อนกลับ

รุ่นนี้เพิ่มตัวอักษรใหญ่ แยกชื่อ/ค่าเป็นสองบรรทัด แก้ค่าทั่วไปในแผงขวา และใช้ขึ้น/ลงเลื่อนหมวดแนวตั้ง ซ้าย/ขวาย้ายคอลัมน์ ต้องกด SET เข้าโหมดแก้ก่อนจึงปรับค่าด้วยซ้าย/ขวาได้ ตัวแก้ค่าเฉพาะทางบางตัวยังใช้หน้าเดิมผ่าน Q

Build ใหม่จากสถานะสะอาดผ่าน; host behavioral tests 12 กลุ่มผ่าน; ตรวจ 32 bindings กับ ARM ELF/โมดูลผ่าน; ZIP และ XOR checksum ผ่าน ยังไม่ได้ทดสอบ v2 บนกล้องจริง และยังไม่มีหน้าถ่ายภาพ/วิดีโอใหม่หรือการวัด recorded fps

ดู BUILD_INFO.json สำหรับ commit ของซอร์สและขนาด autoexec.bin; ตรวจไฟล์ดาวน์โหลดด้วย SHA256SUMS ซอร์สที่ตรงกับบิลด์อยู่ใน **600D-PHOTO-UI-v2-source.zip** ห้ามนำ ZIP ซอร์สไปใช้แทนแพ็กเกจกล้อง

This is a Codex/LLM-assisted fork experiment, not an upstream-endorsed release. Corresponding source and original GPL license notices are included. Inherited optional-document-copy, tcc_status broken-pipe and existing module build warnings remain; no compiler warning or artifact verification was disabled. Host ASan/UBSan remain active; only LeakSanitizer is unavailable under the cloud runner's ptrace, and the tests allocate no heap memory.
