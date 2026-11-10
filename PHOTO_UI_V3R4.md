# FIRMWARE ADD-ON Thai-Menu v3r4 — Public Experimental

โครงการ: **FIRMWARE ADD-ON Thai-Menu**
เว็บไซต์: https://itsamachom.github.io/eos_rom_mlv_modifly/
เป้าหมาย: **Canon EOS 600D / Canon firmware 1.0.2 เท่านั้น**

## การเปลี่ยนแปลง

- แก้หน้าเวอร์ชั่นที่แสดง Build .*s โดยเลิกใช้ precision รูปแบบ %.*s ตัดข้อความลงบัฟเฟอร์ที่จำกัดขนาดก่อนใช้ %s
- หน้าเวอร์ชั่นแสดงชื่อ FIRMWARE ADD-ON, Thai-Menu และ v3r4 ซึ่งอ่านจาก build จริง พร้อม domain/path และ URL เต็มของโครงการ
- ใช้ชื่อรุ่นแบบเดิม v3r4 ไม่มีหมายเลข Build อีกชุด เลขใน scripts/photo-ui-version.txt ถูกใช้โดย build, version menu และ packager
- คงการเลื่อนรายการกลางข้ามหมวดทั้งสองทิศ และหน้า + เจ็ดรายการจาก v3r3
- ข้อมูลกล้องอยู่หน้าแรกของ +; จำนวนชัตเตอร์อยู่หน้า 2/2 ค่า Live View เป็นตัวนับการทำงานกลไก ไม่ใช่จำนวนไฟล์ภาพ Live View โดยตรง

## ดาวน์โหลดและอัปเดต

ไฟล์กล้องคือ **600D-102-PHOTO-UI-v3r4-FULL-EXPERIMENTAL.zip** ไม่ใช่ source ZIP หรือ Source code ที่ GitHub สร้างให้อัตโนมัติ ตรวจ SHA256SUMS ก่อนใช้

สำหรับกล้องที่ติดตั้ง ML แล้ว สำรองการ์ดและแทนที่ autoexec.bin กับ ML/ ทั้งชุด **ไม่เรียก Firmware Update ซ้ำเพื่ออัปเดต UI** อ่าน INSTALL_TH.md กับ UPDATE_TH.md ใน Full ZIP ตัวติดตั้ง FIR ยังคงเดิม ไม่ได้ rebuild หรือทดสอบการติดตั้งครั้งแรกใหม่

## การทดสอบและข้อจำกัด

การทดสอบ host สำหรับหน้าเวอร์ชั่นจำกัด format ที่อนุญาตเป็น literal, %s และ %d โค้ด %.*s เดิมทำให้ regression guard นี้ล้มเหลว โค้ดแก้ผ่าน พร้อมทดสอบเลขรุ่นที่เปลี่ยนไป, ข้อความยาว/ว่าง, read-only และรูปแบบไทย/อังกฤษ ภาพ previews/photo-ui-v3r4-version-proof.png เป็นภาพจาก host fixtures และ font renderer ของโครงการ **ไม่ใช่ภาพจากกล้องหรือการรัน Canon ROM formatter**

ARM build, ASan/UBSan Photo UI tests, atlas regeneration, production shutter-property/MLU/Game checks, 39 linked bindings, packaged module imports, ZIP CRC, XOR และ checksums ผ่านแล้ว เว็บสองภาษาตรวจใน browser ภายในเครื่อง

**เผยแพร่ให้ดาวน์โหลดสาธารณะในสถานะ Experimental ไม่ใช่ Stable** v3r4 ยังไม่ได้ทดสอบบนกล้องจริงหรือ QEMU ผล host tests ไม่รับรองฮาร์ดแวร์

ยังไม่ยืนยัน corresponding implementation source/patches ของ inherited dietlibc 0.33 ตาม release/v3r2/PROVENANCE.md และ READINESS.json การรวมซอร์ส fork และใช้คำว่า Experimental ไม่ได้ปิดประเด็นนี้ ไม่อ้างว่าผ่าน source audit หรือได้รับการรับรองจาก Canon/Magic Lantern เก็บเครดิตและใบอนุญาตต้นทางตาม THIRD_PARTY_NOTICES.md

การแก้ version display, project identity, regression tests, เอกสารและหน้าเว็บมี Codex/LLM ช่วยพัฒนา ดู AI_ASSISTANCE.md

## ออกรุ่นถัดไป

เปลี่ยน scripts/photo-ui-version.txt, เพิ่ม PHOTO_UI_<VERSION>.md, รัน bash scripts/build-photo-ui.sh และ host checks, เพิ่มไฟล์ซอร์สใหม่เข้า Git index แล้วรัน python3 tools/package_photo_ui_current.py ห้ามใส่เลขรุ่นคงที่ในเมนูและห้ามใช้ printf precision แบบ dynamic กับ Canon formatter
