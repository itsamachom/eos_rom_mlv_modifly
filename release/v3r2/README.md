# v3r2 release preparation

**ยังไม่ได้สร้าง GitHub Release/tag และยังไม่ประกาศเป็น stable** เอกสารนี้เป็นชุดเตรียมเผยแพร่ของ fork เอง ไม่ใช่การส่ง contribution หรือ release ให้ Magic Lantern upstream

เตรียมไว้แล้ว:

- README, LICENSE, THIRD_PARTY_NOTICES, เครดิตต้นทางและการเปิดเผย AI
- release notes ที่ระบุ target/firmware, experimental status และข้อจำกัดจริง
- source commit ที่ตรงกับ payload และผลเทียบ 2,257 ไฟล์กับ upstream ที่ผู้ใช้ระบุ
- รายการไฟล์ที่ fork แก้ไข, วิธี build, คู่มือเกม/ติดตั้ง และการตรวจ checksum
- เครื่องมือจัด staging โดยรักษาไบนารีเดิม และเครื่องมือเผยแพร่ที่ปฏิเสธการ publish เมื่อ gate ยังไม่ผ่าน

ยังติด:

1. การยืนยันซอร์ส/patches/build information และ notices ของ dietlibc/Newlib archives ที่ upstream และ fork นำมาเป็นไบนารี ดู PROVENANCE.md และ READINESS.json การตรงกับ archive ต้นทางไม่ได้ยืนยันว่ามี corresponding source ครบ
2. Proxy ไม่อนุญาต api.github.com/uploads.github.com จึงยังสร้างหรืออัปโหลด GitHub Release ผ่าน API ไม่ได้ บันทึกโดเมนเพิ่มใน environment draft แล้ว ต้อง Review/Save และ Publish ใน Environment settings ก่อน retry ไม่มีการขอให้ส่ง token ในแชต

ไม่เปลี่ยนความเป็นส่วนตัวของ repository, ไม่ merge main, ไม่สร้าง tag ที่อ้างว่า release สำเร็จ และไม่ส่งข้อความไปหา upstream ในงานนี้

```sh
python3 tools/prepare_v3r2_release.py
python3 tools/publish_v3r2_release.py --check
# หลังแก้ gate และตรวจหลักฐานแล้วเท่านั้น:
python3 tools/publish_v3r2_release.py --publish
```

Staging อยู่ /workspace/release-staging/v3r2 โดยค่าเริ่มต้น ชุดนี้ยังไม่ใช่ release-ready ตราบที่ READINESS.json ยังมี blocker การบันทึก network draft ไม่ใช่การเปิดสิทธิ์ runtime หรือการ publish GitHub Release
