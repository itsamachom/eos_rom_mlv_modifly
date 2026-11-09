# Photo UI v3r3 — 600D.102 Experimental

- เลื่อนขึ้น/ลงหรือหมุนวงล้อในรายการกลางได้ต่อเนื่องข้ามหมวด S → F → E → O → V → + → G และวนกลับ S เลื่อนย้อนกลับได้ โดยไม่เปลี่ยนค่าถ่ายภาพหรือเรียก action
- หน้า + เหลือ ภาษา, โมดูล, การตั้งค่า, การแสดงผล, เวอร์ชั่น, ข้อมูลกล้อง และจำนวนชัตเตอร์
- ตัดทางลัด ตรวจสอบระบบ, เสียง และเมนูเดิม Shoot/Focus/Expo/Overlay/Movie ออกจากหน้า +
- เวอร์ชั่นเป็นค่าอ่านอย่างเดียว เช่น Build v3r3 อ่านจาก build_version ที่ build system สร้างจริง ไม่ใช่ข้อความรุ่นที่ใส่ซ้ำในเมนู
- ข้อมูลกล้องอยู่หน้าแรกของ +; จำนวนชัตเตอร์อยู่หน้า 2/2 รุ่น/Canon firmware และตัวนับกลไก/Live View/ผลรวมยังคงเดิม ค่า Live View เป็นตัวนับกลไก ไม่ใช่จำนวนไฟล์ภาพ
- คงชื่อ สำหรับ Timelapse/ถ่ายคร่อม (25px), การแก้คำล็อค/TV AV และการตัดโหมดถือกล้องจากรุ่นก่อน

## กฎสำหรับการออกรุ่นถัดไป

1. เปลี่ยนเลขรุ่นใน scripts/photo-ui-version.txt เพียงแห่งเดียว เช่น v3r4
2. เพิ่มเอกสาร PHOTO_UI_V3R4.md สำหรับรุ่นนั้น
3. สร้าง atlas หากเปลี่ยนคำแปล แล้วรัน bash scripts/build-photo-ui.sh ซึ่งอ่านเลขรุ่นจากไฟล์เดียวกัน
4. รัน host checks ตาม CONTRIBUTING.md และ python3 tests/check_mlu_modes.py
5. เพิ่มไฟล์ซอร์สใหม่เข้า Git index ก่อนรัน python3 tools/package_photo_ui_current.py เพื่อให้ source ZIP รวมไฟล์เหล่านั้นด้วย

เมนูเวอร์ชั่น, binary marker และชื่อแพ็กเกจใช้เลขจากขั้นตอนเดียวกัน Packager ตรวจว่า binary ตรงกับเลขรุ่น และป้องกันการเขียนทับ delivery ของรุ่นก่อน การเพิ่มฟีเจอร์ถัดไปต้องเพิ่มเลขรุ่นก่อน build/package

## การอัปเดตและข้อจำกัด

สำหรับ Canon EOS 600D / Canon firmware 1.0.2 ที่ติดตั้ง ML แล้ว ให้สำรองการ์ดและอัปเดต autoexec.bin กับ ML/ ทั้งชุด ไม่เรียก Firmware Update ซ้ำ อ่าน INSTALL_TH.md และ UPDATE_TH.md ใน Full ZIP

Host ASan/UBSan tests ครอบคลุมการข้ามหมวดด้วยปุ่มและวงล้อทั้งสองทิศ, รายการ + ทั้งเจ็ด, เมนูเวอร์ชั่นแบบ read-only และการเปลี่ยน build string ในไทย/อังกฤษ, ข้อมูลกล้อง/ตัวนับ, ฟอนต์ไทย, MLU migration และ bindings/imports ของโมดูล

รุ่นนี้ยังไม่ได้ทดสอบบนกล้องจริงหรือ QEMU ไม่ใช่ stable และไม่ใช่บิลด์ทางการของ Canon/Magic Lantern การแก้ navigation, version display, build/packaging tools, tests และเอกสารมี Codex/LLM ช่วยพัฒนา ยังมีข้อจำกัดเรื่อง corresponding source ของ inherited dietlibc ตาม release/v3r2/PROVENANCE.md และ READINESS.json; ป้าย Experimental ไม่ได้ปิดประเด็นนี้
