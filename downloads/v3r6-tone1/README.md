# Thai-Menu v3r6-tone1 — ทดลองโทน JPEG

- [UPDATE สำหรับกล้อง/การ์ดที่ใช้ Magic Lantern อยู่แล้ว](camera/600D-102-Thai-Menu-v3r6-tone1-UPDATE.zip)
- [ซอร์สโค้ด](../../deliveries/photo-ui-v3r6-tone1-full/600D-PHOTO-UI-v3r6-tone1-source.zip)
- [วิธีใช้ / ขอบเขตผลตรวจ / การคืนค่า](../../PHOTO_UI_V3R6-TONE1.md)
- [ภาพเมนูและตัวบอกขั้นตอน](../../README.md)
- [SHA256SUMS](SHA256SUMS)

ใช้เฉพาะ Canon EOS 600D / Canon firmware 1.0.2 รุ่นทดสอบนี้ยังไม่ยืนยันการบูต การถ่าย JPEG จริง และความเร็วบนกล้อง ต้องตั้ง JPEG หรือ RAW+JPEG ใน Canon ก่อนใช้โทน ไม่เรียก Firmware Update ซ้ำเพื่ออัปเดตเมนูบนกล้อง/การ์ดที่ใช้ Magic Lantern ได้แล้ว

## ข้อจำกัดที่พบเพิ่มจากการตรวจโมดูล

ตรวจ imports ของทั้ง 10 โมดูลกับ symbol file ในแพ็ก พบ `pic_view.mo` ต้องการ `lossless_decompress_raw` ที่ core ไม่ส่งออก มีข้อจำกัดเดียวกันใน v3r5 ไม่ใช่ regression จากฟีเจอร์โทน JPEG จึงยังไม่ยืนยันว่าโมดูล pic_view โหลดได้ อย่าเปิดโมดูลนี้เพื่อทดสอบโทน ฟีเจอร์โทนอยู่ใน core ไม่ต้องโหลดโมดูลเพิ่ม ใช้การดูภาพของ Canon ตามปกติ หลักฐานอยู่ MODULE_IMPORT_AUDIT.json

ไฟล์ FIRST-INSTALL ในโฟลเดอร์ข้างเคียงเป็นผลจาก packager ที่ใช้ตัวติดตั้งเดิม ไม่ใช่ผลยืนยัน first install บนกล้องจริง ผู้ที่ใช้ v3r5 อยู่เลือก UPDATE เท่านั้น และสำรอง autoexec.bin/ML เดิมก่อนทดลอง
