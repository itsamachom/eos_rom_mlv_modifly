# Canon 600D 1.0.2 — Photo UI v3 Full EXPERIMENTAL

ไฟล์ติดตั้ง: **600D-102-PHOTO-UI-v3-FULL-EXPERIMENTAL.zip** รวม autoexec.bin, ML/, ML-SETUP.FIR ต้นฉบับ, ซอร์ส, GPL และคู่มือติดตั้งครั้งแรกภาษาไทย ไม่รวม Canon firmware updater อ่าน [คู่มือติดตั้ง](../../PHOTO_UI_V3_INSTALL_TH.md) ก่อนใช้ และดู [รายละเอียดเมนู/ข้อจำกัด](../../PHOTO_UI_V3.md)

Base: package/600d-photo-ui-v2-full (ca97d4e). Matching source commit: ce1e5cac6c4d5c7d6b072278c8f8e8540e8b9133. Source ZIP is also included inside the Full ZIP under SOURCE/.

Validated: ARM GCC 14.2.1 build; 13 ASan/UBSan behavioral groups; 34 actual ELF/module bindings; retained menu inventory; byte-identical original games; production shutter-counter handler input checks; reproducible Thai bitmaps; ZIP CRC, exact source match, autoexec XOR and installer/payload SHA256. Existing Make recipe and Lua stdio/size warnings remain. No build errors. CONFIG_QEMU=n; QEMU not run.

**ยังไม่ทดสอบ v3 บนกล้องจริง รวมถึงการติดตั้งครั้งแรก** ผล host/build ไม่ยืนยันการบูตหรือการทำงานจริง ภาษาไทยครอบคลุมหน้า Photo UI 48 ข้อความ เมนูย่อย/คำเตือนเดิมยังเป็นอังกฤษ จำนวนชัตเตอร์ต้องรอ property จริง เกมต้องโหลด arkanoid/lua ก่อน ตัว FIR ไม่แก้และไม่ได้ rebuild ไม่เปลี่ยน Picture Style

ตรวจไฟล์จากไดเรกทอรีนี้ด้วย `sha256sum -c SHA256SUMS` ใช้ Full ZIP ไม่ใช่ Code → Download ZIP ของ repository งาน fork ใช้ Codex/LLM ช่วยและไม่ใช่บิลด์ที่ upstream รับรอง
