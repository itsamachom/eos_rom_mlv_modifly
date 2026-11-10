# FIRMWARE ADD-ON Thai-Menu v3r5 — Public Experimental

สำหรับ Canon EOS 600D / Canon firmware 1.0.2 เท่านั้น

- เปลี่ยนป้าย “กลไก Live View” เป็น **“โหมด Live View”** โดยไม่เปลี่ยนวิธีอ่านตัวนับ ค่านี้ยังเป็นจำนวนการทำงานกลไก ไม่ใช่จำนวนไฟล์ภาพ Live View โดยตรง
- ผู้ที่ยังไม่มี ML เลือก **FIRST-INSTALL.zip**: รวม autoexec.bin, ML/ และ ML-SETUP.FIR เดิม ไม่ต้องติดตั้ง ML จากแพ็กเกจอื่นก่อน
- ผู้ที่มี ML บนกล้องและการ์ดอยู่แล้วเลือก **UPDATE.zip**: ไม่มี FIR ไม่เรียก Firmware Update ซ้ำเพื่ออัปเดตเมนู
- **Source ZIP** แยกจากไฟล์ลงกล้องทั้งสองชนิด
- หน้าเว็บแสดงรุ่นล่าสุดและลิงก์ผู้พัฒนา Online2easy / Online2hobby ทุกหน้า ไฟล์แจก/คู่มือรุ่นเก่านำออกจาก branch ปัจจุบัน ประวัติ Git และ tag เดิมยังเก็บอยู่

อ่าน INSTALL_TH.md / INSTALL_EN.md ก่อนใช้ โดยเฉพาะการติดตั้งครั้งแรก: Canon firmware ต้องเป็น 1.0.2, ใช้ SD/SDHC ไม่เกิน 32 GB ตามคู่มือต้นทาง, สำรองข้อมูลก่อนฟอร์แมต และรีสตาร์ตเมื่อ installer ขึ้นจอเขียว / Please restart your camera. อย่าค้างในหน้านับถอยหลังถอนการติดตั้ง

ตัวติดตั้ง FIR เป็นไฟล์เดิมที่ตรวจ SHA256 ตรงกับต้นทาง: 7e33d8a2a71ad92c412d291fb0ecb6de0b9404c212571d51fd82f839688070e3 ไม่ได้ rebuild หรือเปลี่ยนการตั้ง boot flag ในโค้ดของรุ่นนี้ **การรวมตัวติดตั้งไม่ใช่ผลทดสอบติดตั้งครั้งแรกบนกล้องจริง** รุ่นนี้ยังไม่ได้ทดสอบบนกล้องจริง/QEMU และไม่ใช่ Stable

Host tests และ ARM build ตรวจคำแปล ฟอนต์ UI/menu/version, ตัวนับ, MLU, เกมและ bindings/imports; packager ตรวจ runtime bytes ของสอง ZIP, CRC/XOR, installer hash/size, Source และ checksum การติดตั้งบนฮาร์ดแวร์จริงยังต้องยืนยันแยกต่างหาก

เครดิต/ใบอนุญาตต้นทางยังอยู่ครบ เอกสาร release/v3r2 เก็บไว้เพราะเป็น provenance/ใบอนุญาตของไลบรารีที่ยังใช้ corresponding source ของ inherited dietlibc ยังยืนยันไม่ครบ โครงการนี้มี Codex/LLM ช่วยพัฒนา ไม่ใช่บิลด์ที่ Canon หรือ Magic Lantern รับรอง

เว็บไซต์: https://itsamachom.github.io/eos_rom_mlv_modifly/

ผู้พัฒนา: [YouTube Online2easy](https://www.youtube.com/@Online2easy) · [Facebook Online2easy](https://www.facebook.com/online2easy) · [Online2hobby Blog](https://online2hobby.blogspot.com/)

รุ่นถัดไป: เปลี่ยน scripts/photo-ui-version.txt และเพิ่มเอกสารรุ่น → build/test → เพิ่มซอร์สเข้า Git index → package_photo_ui_current.py → package_camera_download.py → render_download_pages.py → commit/tag/publish โดยไม่เขียนทับ tag หรือ ZIP ที่เผยแพร่แล้ว
