# Photo UI TH1 — Thai prototype for Canon 600D / Canon 1.0.2

ต้นแบบภาษาไทยพร้อมตัวเลือก English ใช้ Noto Sans Thai ภายใต้ SIL OFL มีคำแปล 318 ข้อความ จัดรูปสระ/วรรณยุกต์ล่วงหน้า ไม่ดึงฟอนต์จาก Canon และไม่เปลี่ยนชื่อ/คำสั่งภายใน ML

## เลือกไฟล์

- **600D-102-PHOTO-UI-TH1-TEST.zip**: สำหรับกล้องและการ์ดที่ใช้ ML อยู่แล้ว เช่น กล้องของเจ้าของโครงการ เปลี่ยน autoexec.bin และ ML/ ทั้งชุดหลังสำรองข้อมูล ไม่ใช้ FIR
- **600D-102-PHOTO-UI-TH1-FULL-EXPERIMENTAL.zip**: เพิ่มตัวติดตั้ง FIR เดิมสำหรับผู้เริ่มติดตั้งครั้งแรก อ่าน [คู่มือติดตั้ง](../../INSTALL_PHOTO_THAI_TH.md) ก่อน ไม่รวม Canon firmware 1.0.2
- **600D-PHOTO-UI-TH1-source.zip**: ซอร์สที่ตรงกับบิลด์ ฟอนต์ต้นฉบับ ใบอนุญาต และเครื่องมือสร้างข้อความ ไม่ใช่ไฟล์สำหรับคัดลอกลงการ์ด

ดาวน์โหลดด้วย Download raw file ไม่ใช่ Code > Download ZIP

อ่าน [คู่มือภาษาไทยและวิธีสลับภาษา](../../PHOTO_UI_THAI.md) สลับได้ที่ + > ภาษา / Language ภาษาไทยแสดงตัวเลือกขวาครั้งละ 3 แถวเพื่อเว้นวรรณยุกต์ ภาษาอังกฤษยังเป็น 4 แถว

ดู [ตัวอย่างจัดรูปฟอนต์](../../previews/thai-font-proof.png) — เป็นภาพจากเครื่อง ไม่ใช่ภาพจากกล้องจริง

**ยังไม่ได้ทดสอบ TH1 บนกล้องจริง** เมนูเดิม/โมดูลบางส่วนและข้อความนอกคำแปลยังเป็นอังกฤษ ไม่ได้อ้างว่าทุกส่วนของ ML แปลไทยแล้ว เมื่อข้อมูลภาษาไทยขาดหรือผิดรุ่นจะกลับเป็นอังกฤษ ยังไม่มีหน้าจอขณะถ่ายภาพ/วิดีโอใหม่หรือการวัด recorded fps

Build ผ่าน (รวม full clean build ก่อนการปรับ deferred loading ขั้นสุดท้าย และ incremental build หลังปรับ); host tests 16 กลุ่มผ่าน; ตรวจ 33 bindings กับ ARM ELF/โมดูลผ่าน; ZIP/XOR checksum และความตรงกันของข้อมูลฟอนต์ผ่าน BUILD_INFO.json บันทึก source commit และที่มาฟอนต์ ตรวจไฟล์ด้วย SHA256SUMS

Noto font/license bytes are retained unchanged from the pinned official source. The original OFL text contains upstream trailing whitespace which is preserved. The rendering implementation and translations are Codex/LLM-assisted fork changes, not an upstream-endorsed release. Preserve GPL and SIL OFL notices when redistributing.
