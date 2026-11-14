# Thai-Menu v3r6-tone3 — Menu names and artwork samples (Experimental)

สำหรับ Canon EOS 600D / Canon firmware 1.0.2 เท่านั้น รุ่นหลักบนเว็บและคู่มือยังเป็น **v3r5**

## เปลี่ยนชื่อเมนูตามที่ขอ

- โทนสี JPEG → **FLIM TONE**
- ฟิล์มสี → **Color Film**
- ฟิล์มสไลด์ → **Silde Film**
- ซีนีมา → **Cinema**
- ขาวดำ → **Black and White**

ใช้การสะกด FLIM และ Silde ตามข้อความที่ผู้ใช้ระบุ ทั้งภาษาไทยและภาษาอังกฤษแสดงชื่อเหล่านี้เหมือนกัน ขยายช่อง Black and White ให้แสดงชื่อเต็ม โดยยังใช้ขนาดฟอนต์เดียวกับกลุ่มอื่น

สูตรทั้ง 72 รายการ การเลือก/ตั้งค่า/คืนค่า ISO/WB/Picture Style และภาพกลักที่ใช้จริงยังเหมือน tone2 การเปลี่ยนครั้งนี้ไม่ปรับสูตร ผู้ใช้ยืนยันว่าเมนู tone2 ใช้งานได้แล้ว แต่ยังไม่ได้ยืนยันความแตกต่าง/คุณภาพสีจากการถ่ายจริง

## ตัวอย่างภาพที่แยกไว้ให้เลือก

[กล่องมุมเฉียง](design/film-concepts/v3r6-tone3/angled-box.png) · [ด้านหน้ากล่อง](design/film-concepts/v3r6-tone3/front-box.png) · [กลักฟิล์มเดี่ยว](design/film-concepts/v3r6-tone3/canister.png)

ภาพตัวอย่างสร้างด้วย OpenAI image generation เป็นงานออกแบบ THAI-MENU / Color Film ของโครงการ ไม่ใช่ภาพหน้าจอกล้อง และ **ยังไม่ใส่แทนภาพใน firmware** ใช้ภาพเพื่อเลือกแนวทางก่อนนำไปย่อและปรับสี/ตัวอักษรสำหรับจอ 600D ไฟล์ใน design เป็นตัวอย่างออกแบบ ไม่ใช่ runtime asset จึงไม่รวมใน source ZIP ของ firmware

## ใช้งานและผลตรวจ

วิธีใช้/ข้อจำกัดเหมือน [tone2](PHOTO_UI_V3R6-TONE2.md) แต่ชื่อทางเข้าเป็น **S → FLIM TONE** สำรอง autoexec.bin และ ML/ เดิมทั้งชุดก่อนลง UPDATE ไม่เรียก Firmware Update ซ้ำเพื่ออัปเดตเมนู คืนค่าด้วย Q แล้ว SET ก่อนปิดกล้องหากต้องการค่า ISO/WB/Picture Style เดิม

Host tests ใช้ engine/UI และ Canon adapter จากโค้ดจริง ตรวจสูตรเดิมครบ72, การคืนค่า, metadata, failure/rollback, กรอบภาพไทย/อังกฤษ; ARM build และชุดไฟล์ตรวจเลขรุ่น/CRC/XOR/atlas/source ตรงกัน ชื่อเวอร์ชันในเมนูเป็น v3r6-tone3

**ยังไม่ได้ทดสอบบูตหรือถ่าย JPEG ของ tone3 บนกล้องจริงหรือ QEMU** และยังไม่สรุปผลสี/ความเร็ว เป็นรุ่นทดลองแยกจาก v3r5 ตัวติดตั้งเดิมไม่แก้ไข ข้อค้าง inherited dietlibc corresponding source และ pic_view import ยังคงเดิม ดู THIRD_PARTY_NOTICES.md
