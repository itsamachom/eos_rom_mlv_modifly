# 600D Photo UI v1 — hardware-untested test package

ดาวน์โหลด **600D-102-PHOTO-UI-v1-TEST.zip** ด้วยปุ่ม Download raw file แล้วอ่าน [คู่มือภาษาไทย](../../PHOTO_UI_V1.md) ก่อนนำลงการ์ด ใช้กับ Canon 600D / Canon 1.0.2 ที่ติดตั้ง ML และมีการ์ดบูต ML ได้อยู่แล้วเท่านั้น

ไฟล์สำหรับกล้องมี autoexec.bin และ ML/ ไม่มีตัวติดตั้ง FIR บิลด์นี้เปลี่ยนหน้าหลักเมนูตามแนวทาง PDF และตัดเกม/เมนูเสียง ML แต่แผงปรับค่ารายละเอียดยังใช้ของเดิม ยังไม่ได้ทำหน้าถ่ายภาพใหม่หรือการวัด fps ของการบันทึกจริง

ทดสอบ build ใหม่จากสถานะสะอาดผ่าน ตรวจ ZIP/XOR checksum ผ่าน ทดสอบพฤติกรรมบนเครื่อง 8 กลุ่มผ่าน และตรวจทางเข้ารายการกับ ARM ELF/โมดูล 32 จุดผ่าน ผลเหล่านี้ไม่ยืนยันความปลอดภัยหรือการทำงานบนกล้องจริง

ดู BUILD_INFO.json สำหรับ source commit, ขนาดไฟล์, เวอร์ชัน และ checksum; SHA256SUMS สำหรับตรวจไฟล์ดาวน์โหลด ส่วน **600D-PHOTO-UI-v1-source.zip** เป็นซอร์สตรงกับบิลด์นี้ ไม่ใช่ไฟล์สำหรับคัดลอกลงการ์ด

Known build messages inherited from the baseline: missing optional doc/cam copy ignored by Makefile; grep broken pipe from the tcc_status/cmp pipeline; TCC memory TODO, duplicate module recipes and Lua stdio-size warnings. No build verification or compiler warning flags were disabled. Host tests retain AddressSanitizer/UBSan; LeakSanitizer alone cannot run under the cloud runner's ptrace, and the tests allocate no heap memory.

This is a Codex/LLM-assisted fork experiment, not an upstream-approved release. Corresponding source and original license notices are included. Preserve GPL notices in firmware/COPYING.
