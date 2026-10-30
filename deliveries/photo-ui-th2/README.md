# Photo UI TH2 — state/race fixes for Canon 600D / Canon 1.0.2

รุ่นแก้บั๊กจาก TH1 อ่าน [รายละเอียดการแก้และวิธีทดสอบ](../../PHOTO_UI_TH2.md) ก่อนอัปเดต

- **600D-102-PHOTO-UI-TH2-TEST.zip**: สำหรับกล้องและการ์ดที่ใช้ ML อยู่แล้ว สำรองของเดิมและเปลี่ยน autoexec.bin กับ ML/ ทั้งชุด ไม่ต้องใช้ FIR
- **600D-102-PHOTO-UI-TH2-FULL-EXPERIMENTAL.zip**: เพิ่มตัวติดตั้ง FIR เดิมสำหรับผู้ติดตั้ง ML ครั้งแรก ไม่รวม Canon firmware 1.0.2
- **600D-PHOTO-UI-TH2-source.zip**: ซอร์สตรงรุ่น ฟอนต์ ใบอนุญาต และเครื่องมือ build ไม่ใช่ ZIP สำหรับลงการ์ด

กด Download raw file จากหน้าไฟล์ ไม่ใช่ Code > Download ZIP

แก้การเปลี่ยนหมวดพร้อมวาดจอ และแยกตัวตนของรายการที่แสดงออกจากรายการที่เริ่มแก้ค่า/รอยืนยัน หากรายการเปลี่ยนจะยกเลิกสถานะเดิมและต้องกด SET ใหม่ Callback ของ ML ยังทำงานนอกล็อกเพื่อให้เรียกเมนูซ้ำได้ การวาดจอจะไม่เปลี่ยน selection ระหว่าง callback

Build ผ่าน, host tests 23 กลุ่มผ่าน (รวม 7 กลุ่มเพิ่มจาก TH1), ตรวจ 33 bindings กับ ARM ELF/โมดูลจริงผ่าน, ZIP/XOR checksum ผ่าน ฟอนต์และคำแปลเหมือน TH1 **ยังไม่ได้ทดสอบ TH2 บนกล้องจริงหรือทดสอบติดตั้งครั้งแรก** ไม่ใช่การรับรองว่าทั้งเฟิร์มแวร์ไม่มีบั๊ก

BUILD_INFO.json ระบุ source commit, เวอร์ชัน, ขนาด autoexec.bin และข้อมูลฟอนต์ SHA256SUMS ใช้ตรวจไฟล์ดาวน์โหลด รุ่น TH1 เดิมเก็บแยกไว้ใน deliveries/photo-ui-thai ไม่ได้ถูกทับ

This is a Codex/LLM-assisted fork experiment, not an upstream-endorsed release. Corresponding source and original GPL/OFL notices are included. The original installer FIR is unchanged and not independently rebuilt.
